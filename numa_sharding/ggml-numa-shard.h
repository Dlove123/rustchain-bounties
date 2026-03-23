#ifndef GGML_NUMA_SHARD_H
#define GGML_NUMA_SHARD_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

// NUMA layer router configuration
struct ggml_numa_config {
    int numa_nodes;           // Number of NUMA nodes
    size_t node_memory_gb;    // Memory per node in GB
    bool enable_sharding;     // Enable NUMA sharding
};

// Parse GGUF tensor metadata and assign to NUMA nodes
int ggml_numa_parse_gguf(const char* model_path, struct ggml_numa_config* config);

// Allocate tensor on specific NUMA node
void* ggml_numa_alloc(size_t size, int node_id);

// Free NUMA allocated memory
void ggml_numa_free(void* ptr, size_t size);

#ifdef __cplusplus
}
#endif

#endif // GGML_NUMA_SHARD_H
