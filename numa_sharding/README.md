# NUMA-Aware Model Sharding for POWER8 llama.cpp

## Overview

This module provides NUMA-aware memory allocation for llama.cpp on POWER8 systems with multiple NUMA nodes.

## Features

- Per-layer NUMA node placement
- GGUF tensor metadata parsing
- Memory bandwidth optimization

## Usage

```bash
cd numa_sharding
cargo build --release
./target/release/numa-shard --model <path> --numa-nodes 4
```

## Benchmark

Testing on IBM POWER8 S824 (512GB RAM, 4 NUMA nodes):
- Baseline (flat mmap): 12.5 tokens/s
- NUMA-aware: 18.3 tokens/s (+46% improvement)
