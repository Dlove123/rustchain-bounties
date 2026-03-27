#pragma once

/**
 * NUMA-Aware Model Sharding for POWER8 llama.cpp
 * Bounty #2277 - 250 RTC
 * 
 * Intelligent per-layer NUMA placement for IBM POWER8 S824
 * 512GB RAM across 4 NUMA nodes
 */

#include <numa.h>
#include <numaif.h>
#include <stdint.h>
#include <stdbool.h>

// NUMA node configuration for POWER8 S824
#define NUMA_NODE_COUNT 4
#define NUMA_NODE_0 0  // Heavy/General (core knowledge)
#define NUMA_NODE_1 1  // Science/Tech domain
#define NUMA_NODE_2 2  // Creative/Long CTX
#define NUMA_NODE_3 3  // Niche/History

// Transformer layer types
typedef enum {
    LAYER_TYPE_INPUT,      // Input embeddings
    LAYER_TYPE_ATTENTION,  // Self-attention layers
    LAYER_TYPE_FFN,        // Feed-forward networks
    LAYER_TYPE_NORM,       // Layer normalization
    LAYER_TYPE_OUTPUT      // Output head
} layer_type_t;

// NUMA routing policy
typedef struct {
    int numa_node;           // Target NUMA node
    layer_type_t layer_type; // Layer type
    int layer_start;         // Start layer index
    int layer_end;           // End layer index
    size_t memory_size;      // Estimated memory size
} numa_routing_t;

/**
 * Initialize NUMA subsystem
 * Returns 0 on success, -1 on failure
 */
static inline int numa_init_system(void) {
    if (numa_available() < 0) {
        return -1;
    }
    
    // Set interleaved memory allocation as default
    struct bitmask *nodes = numa_all_nodes_ptr;
    if (!nodes) {
        return -1;
    }
    
    numa_set_interleave_mask(nodes);
    return 0;
}

/**
 * Allocate memory on specific NUMA node
 * 
 * @param size Memory size in bytes
 * @param node Target NUMA node
 * @return Pointer to allocated memory, NULL on failure
 */
static inline void* numa_alloc_on_node(size_t size, int node) {
    struct bitmask *nodemask = numa_bitmask_setall(numa_all_nodes_ptr);
    if (!nodemask) {
        return NULL;
    }
    
    numa_bitmask_clearall(nodemask);
    numa_bitmask_setbit(nodemask, node);
    
    void* ptr = numa_alloc_onnode(size, node);
    numa_free_nodemask(nodemask);
    
    return ptr;
}

/**
 * Move memory pages to target NUMA node
 * 
 * @param addr Memory address
 * @param len Memory length
 * @param node Target NUMA node
 * @return 0 on success, -1 on failure
 */
static inline int numa_move_pages(void* addr, size_t len, int node) {
    long page_size = sysconf(_SC_PAGESIZE);
    long num_pages = (len + page_size - 1) / page_size;
    
    // Array of page addresses
    void** pages = malloc(num_pages * sizeof(void*));
    if (!pages) {
        return -1;
    }
    
    for (long i = 0; i < num_pages; i++) {
        pages[i] = (char*)addr + (i * page_size);
    }
    
    // Move pages to target node
    int status;
    int err = numa_move_pages(0, num_pages, pages, NULL, &status, 0);
    
    free(pages);
    return err;
}

/**
 * Get optimal NUMA node for transformer layer
 * 
 * Strategy:
 * - Early layers (0-8): Node 0 - General knowledge
 * - Attention layers: Node 1 - Compute intensive
 * - FFN layers: Node 2 - Memory intensive
 * - Late layers: Node 3 - Output preparation
 * 
 * @param layer_idx Layer index
 * @param total_layers Total number of layers
 * @param layer_type Layer type
 * @return Optimal NUMA node
 */
static inline int numa_get_layer_node(int layer_idx, int total_layers, layer_type_t layer_type) {
    // Early layers - general knowledge
    if (layer_idx < total_layers / 4) {
        return NUMA_NODE_0;
    }
    
    // Late layers - output preparation
    if (layer_idx >= 3 * total_layers / 4) {
        return NUMA_NODE_3;
    }
    
    // Middle layers - route by type
    switch (layer_type) {
        case LAYER_TYPE_ATTENTION:
            return NUMA_NODE_1;  // Compute intensive
        case LAYER_TYPE_FFN:
            return NUMA_NODE_2;  // Memory intensive
        case LAYER_TYPE_NORM:
        case LAYER_TYPE_INPUT:
        case LAYER_TYPE_OUTPUT:
        default:
            return NUMA_NODE_0;  // Default to node 0
    }
}

/**
 * Setup NUMA routing table for model
 * 
 * @param total_layers Total number of transformer layers
 * @param routing Output routing table
 * @param routing_size Size of routing table
 * @return Number of routing entries
 */
static inline int numa_setup_routing(int total_layers, numa_routing_t* routing, int routing_size) {
    if (!routing || routing_size < 4) {
        return -1;
    }
    
    int entry = 0;
    
    // Input embeddings
    routing[entry++] = (numa_routing_t){
        .numa_node = NUMA_NODE_0,
        .layer_type = LAYER_TYPE_INPUT,
        .layer_start = 0,
        .layer_end = 0,
        .memory_size = 0  // Will be calculated
    };
    
    // Transformer layers
    int layers_per_quarter = total_layers / 4;
    
    for (int q = 0; q < 4; q++) {
        int start = q * layers_per_quarter;
        int end = (q + 1) * layers_per_quarter;
        
        routing[entry++] = (numa_routing_t){
            .numa_node = q,
            .layer_type = LAYER_TYPE_ATTENTION,
            .layer_start = start,
            .layer_end = end,
            .memory_size = 0
        };
    }
    
    // Output head
    routing[entry++] = (numa_routing_t){
        .numa_node = NUMA_NODE_3,
        .layer_type = LAYER_TYPE_OUTPUT,
        .layer_start = total_layers - 1,
        .layer_end = total_layers,
        .memory_size = 0
    };
    
    return entry;
}

/**
 * Bind current thread to NUMA node
 * 
 * @param node Target NUMA node
 * @return 0 on success, -1 on failure
 */
static inline int numa_bind_thread(int node) {
    struct bitmask* cpumask = numa_node_to_cpus(node);
    if (!cpumask) {
        return -1;
    }
    
    int err = numa_sched_setaffinity(0, cpumask);
    numa_free_cpumask(cpumask);
    
    return err;
}

/**
 * Get NUMA node memory info
 * 
 * @param node NUMA node index
 * @param free_mem Output: free memory in bytes
 * @param total_mem Output: total memory in bytes
 * @return 0 on success, -1 on failure
 */
static inline int numa_get_node_memory(int node, size_t* free_mem, size_t* total_mem) {
    if (node < 0 || node >= numa_num_configured_nodes()) {
        return -1;
    }
    
    // Get memory info from sysfs
    char path[256];
    snprintf(path, sizeof(path), "/sys/devices/system/node/node%d/meminfo", node);
    
    FILE* f = fopen(path, "r");
    if (!f) {
        return -1;
    }
    
    char line[256];
    while (fgets(line, sizeof(line), f)) {
        unsigned long value;
        if (sscanf(line, "MemTotal: %lu kB", &value) == 1) {
            if (total_mem) *total_mem = value * 1024;
        } else if (sscanf(line, "MemFree: %lu kB", &value) == 1) {
            if (free_mem) *free_mem = value * 1024;
        }
    }
    
    fclose(f);
    return 0;
}

/**
 * Test NUMA awareness
 * 
 * @return true if NUMA is available and configured
 */
static inline bool numa_test_awareness(void) {
    // Check if NUMA is available
    if (numa_available() < 0) {
        return false;
    }
    
    // Check if we have multiple nodes
    if (numa_num_configured_nodes() < 2) {
        return false;
    }
    
    // Test allocation on different nodes
    for (int i = 0; i < numa_num_configured_nodes(); i++) {
        void* ptr = numa_alloc_on_node(4096, i);
        if (!ptr) {
            return false;
        }
        numa_free(ptr, 4096);
    }
    
    return true;
}
