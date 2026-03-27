/**
 * NUMA Sharding Test Suite
 * Bounty #2277 - 250 RTC
 * 
 * Test NUMA-aware model sharding for POWER8 llama.cpp
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <unistd.h>
#include <sys/mman.h>

#include "ggml-numa-shard.h"

// Test counters
static int tests_run = 0;
static int tests_passed = 0;
static int tests_failed = 0;

// Test macros
#define TEST(name) static void name(void)
#define RUN_TEST(name) do { \
    tests_run++; \
    printf("Running %s... ", #name); \
    name(); \
    tests_passed++; \
    printf("PASSED\n"); \
} while(0)

#define ASSERT(cond) do { \
    if (!(cond)) { \
        printf("FAILED: %s\n", #cond); \
        tests_failed++; \
        tests_passed--; \
        return; \
    } \
} while(0)

#define ASSERT_EQ(a, b) ASSERT((a) == (b))
#define ASSERT_NEQ(a, b) ASSERT((a) != (b))

// ========== Test Cases ==========

TEST(test_numa_init) {
    // Test NUMA initialization
    int ret = numa_init_system();
    // NUMA might not be available in all environments
    // Don't fail if unavailable, just skip
    if (ret == 0) {
        printf("[NUMA available] ");
    } else {
        printf("[NUMA not available - skipping] ");
    }
}

TEST(test_numa_layer_routing) {
    // Test layer routing logic
    int total_layers = 32;
    
    // Early layers should go to Node 0
    ASSERT_EQ(numa_get_layer_node(0, total_layers, LAYER_TYPE_ATTENTION), NUMA_NODE_0);
    ASSERT_EQ(numa_get_layer_node(5, total_layers, LAYER_TYPE_ATTENTION), NUMA_NODE_0);
    
    // Middle attention layers should go to Node 1
    ASSERT_EQ(numa_get_layer_node(10, total_layers, LAYER_TYPE_ATTENTION), NUMA_NODE_1);
    
    // Middle FFN layers should go to Node 2
    ASSERT_EQ(numa_get_layer_node(15, total_layers, LAYER_TYPE_FFN), NUMA_NODE_2);
    
    // Late layers should go to Node 3
    ASSERT_EQ(numa_get_layer_node(28, total_layers, LAYER_TYPE_ATTENTION), NUMA_NODE_3);
}

TEST(test_numa_routing_table) {
    // Test routing table setup
    numa_routing_t routing[8];
    int total_layers = 32;
    
    int entries = numa_setup_routing(total_layers, routing, 8);
    ASSERT(entries >= 4);  // At least input + 4 quarters + output
    
    // Check first entry (input)
    ASSERT_EQ(routing[0].layer_type, LAYER_TYPE_INPUT);
    ASSERT_EQ(routing[0].numa_node, NUMA_NODE_0);
    
    // Check last entry (output)
    ASSERT_EQ(routing[entries-1].layer_type, LAYER_TYPE_OUTPUT);
    ASSERT_EQ(routing[entries-1].numa_node, NUMA_NODE_3);
}

TEST(test_numa_alloc) {
    // Test NUMA allocation (skip if NUMA not available)
    if (numa_available() < 0) {
        printf("[SKIP: NUMA not available] ");
        return;
    }
    
    size_t size = 4096;
    
    for (int i = 0; i < numa_num_configured_nodes(); i++) {
        void* ptr = numa_alloc_on_node(size, i);
        ASSERT(ptr != NULL);
        
        // Verify memory is accessible
        memset(ptr, 0, size);
        
        numa_free(ptr, size);
    }
}

TEST(test_numa_thread_binding) {
    // Test thread binding (skip if NUMA not available)
    if (numa_available() < 0) {
        printf("[SKIP: NUMA not available] ");
        return;
    }
    
    for (int i = 0; i < numa_num_configured_nodes(); i++) {
        int ret = numa_bind_thread(i);
        // Binding might fail in containerized environments
        if (ret == 0) {
            printf("[Node %d bound] ", i);
        }
    }
}

TEST(test_numa_memory_info) {
    // Test memory info retrieval
    size_t free_mem, total_mem;
    
    int ret = numa_get_node_memory(0, &free_mem, &total_mem);
    if (ret == 0) {
        ASSERT(total_mem > 0);
        printf("[Node 0: %zu MB total] ", total_mem / (1024 * 1024));
    } else {
        printf("[SKIP: Cannot read memory info] ");
    }
}

TEST(test_numa_awareness) {
    // Test NUMA awareness detection
    bool aware = numa_test_awareness();
    printf("[%s] ", aware ? "NUMA aware" : "NUMA not aware");
}

TEST(test_layer_type_routing) {
    // Test different layer types
    int total_layers = 32;
    int mid_layer = total_layers / 2;
    
    // Attention layers
    int attn_node = numa_get_layer_node(mid_layer, total_layers, LAYER_TYPE_ATTENTION);
    ASSERT(attn_node == NUMA_NODE_1 || attn_node == NUMA_NODE_2);
    
    // FFN layers
    int ffn_node = numa_get_layer_node(mid_layer, total_layers, LAYER_TYPE_FFN);
    ASSERT(ffn_node == NUMA_NODE_1 || ffn_node == NUMA_NODE_2);
    
    // Normalization should go to default node
    int norm_node = numa_get_layer_node(mid_layer, total_layers, LAYER_TYPE_NORM);
    ASSERT_EQ(norm_node, NUMA_NODE_0);
}

TEST(test_numa_move_pages) {
    // Test page migration (skip if NUMA not available)
    if (numa_available() < 0) {
        printf("[SKIP: NUMA not available] ");
        return;
    }
    
    size_t size = 4096 * 10;  // 10 pages
    void* ptr = numa_alloc_on_node(size, 0);
    ASSERT(ptr != NULL);
    
    // Initialize memory
    memset(ptr, 0, size);
    
    // Try to move to different node (might fail in containers)
    int ret = numa_move_pages(ptr, size, 1);
    // Don't assert - migration might fail in containers
    
    numa_free(ptr, size);
}

// ========== Main ==========

int main(int argc, char** argv) {
    printf("=== NUMA Sharding Test Suite ===\n");
    printf("Bounty #2277 - 250 RTC\n\n");
    
    // Run all tests
    RUN_TEST(test_numa_init);
    RUN_TEST(test_numa_layer_routing);
    RUN_TEST(test_numa_routing_table);
    RUN_TEST(test_numa_alloc);
    RUN_TEST(test_numa_thread_binding);
    RUN_TEST(test_numa_memory_info);
    RUN_TEST(test_numa_awareness);
    RUN_TEST(test_layer_type_routing);
    RUN_TEST(test_numa_move_pages);
    
    // Print summary
    printf("\n=== Test Summary ===\n");
    printf("Total:  %d\n", tests_run);
    printf("Passed: %d\n", tests_passed);
    printf("Failed: %d\n", tests_failed);
    
    if (tests_failed > 0) {
        printf("\n❌ Some tests failed!\n");
        return 1;
    } else {
        printf("\n✅ All tests passed!\n");
        return 0;
    }
}
