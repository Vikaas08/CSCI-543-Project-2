# LevelDB: BitWeaving Range Scan Optimization
![Status](https://img.shields.io/badge/Status-Completed-success)
![Language](https://img.shields.io/badge/Language-C++-blue)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Docker-orange)
![Category](https://img.shields.io/badge/Category-Database%20Engine%20Internals-red)

An architectural modification to Google's **LevelDB** storage engine, implementing intra-file **BitWeaving (Order-Preserving Bit-Slicing)** to drastically reduce disk I/O during value-based range scans.

---

## 🚀 Project Overview

Standard LSM-trees natively sort data by key, making value-based range scans highly inefficient as they force the engine to read, decompress, and deserialize every block in the queried range. 

This project modifies the LevelDB core engine to generate and store 32-bit dynamic bitmasks combined with ZoneMaps (Min/Max) for every 64-record cache-aligned block. During a range scan, the engine evaluates these bitmasks in memory, safely bypassing disk I/O entirely for blocks that do not match the query predicate.

**Key Achievements:**
* Up to **89.38% reduction** in disk I/O for high-selectivity queries.
* Up to **10.19x latency speedup**.
* Highly optimized storage footprint (**< 0.1% space overhead**) proven at a scale of 500 million records.

---

## 📍 Code Map: What We Added

Per the project requirements, our modifications successfully hijacked the read/write paths without altering LevelDB's public API. Our implementation is concentrated in the following files:

### 1. The Core Logic Engine
* **`util/bitweave.h`**: We built a header-only mathematical engine containing `BitWeaveBuilder` and `BitWeaveReader`. It utilizes a Hybrid ZoneMap approach, dynamically dividing the local range of a 64-record block into 32 equal bands to generate highly precise bitmasks.

### 2. The Write Path (Compaction)
* **`table/table_builder.cc`**: Intercepted the `TableBuilder::Add()` function to parse string slices into integers. When `TableBuilder::Finish()` is called, our logic bundles the generated bitmasks into a 12-byte payload and writes it to disk as a custom `bitweave.leveldb.BWH` Meta-Index block.

### 3. The Read Path (Query Filtering)
* **`table/table.cc`**: 
  * Modified `Table::Open` to load the BitWeaving metadata into an in-memory `std::unordered_map` for O(1) index lookups.
  * Intercepted `Table::BlockReader` (the final step before Disk/Cache I/O). If our BitWeaving filter returns `false` for a block, we immediately return `NewEmptyIterator()`, completely avoiding decompression and disk access.

### 4. The Evaluation Framework
* **`bitweave_*.cc`**: We initially considered evaluating our BitWeaving implementation using standard frameworks like YCSB Workload E or LevelDB's native db_bench. However, these industry-standard tools treat the storage engine as a black box, measuring only top-level latency and throughput. Because BitWeaving's primary contribution is avoiding disk I/O at the block level, we constructed a native C++ benchmarking suite that mirrors the read-heavy access patterns of YCSB Workload E, while instrumenting the internal engine to accurately report cache utilization, block-skipping rates, and metadata storage overhead."

---

## 🛠 Verification & Benchmarking

To verify the implementation, we have provided a comprehensive native benchmarking suite.

### 1. Build the Engine
```bash
mkdir -p build && cd build
cmake ..
make -j$(nproc)
```
### 2. Verify Mathematical Correctness
Runs unit tests to guarantee 0% false negatives in the bitmask logic, and a 10,000-record integration test to verify the `TableReader` hook.
```bash
./bitweave_test
```
### 3. Run the Evaluation Suite
We built three distinct benchmark binaries to stress-test different system limits:

* **Micro-Benchmarks (Distributions):** Tests Uniform, Skewed, and Bimodal data distributions.
  ```bash
  ./bitweave_benchmark
  ```
* **Real-World Simulation:** Tests realistic access patterns including IoT temperature anomalies, DB query latencies, and CPU spikes.
  ```bash
  ./bitweave_realworld
  ```
* **Macro-Benchmarks (Scalability):** Writes between 1 Million and 500 Million records to disk to verify that the 12-byte metadata payload does not bloat the storage engine footprint.
  ```bash
  ./bitweave_largescale
  ```

> **Note:** Raw execution logs from our evaluation have been exported and saved in the `benchmark_results/` directory at the root of this repository for immediate review.

---

## 🧪 Concurrent Live-Streaming Simulation

To prove our BitWeaving implementation is thread-safe and respects LevelDB's Snapshot isolation, we included a live producer/consumer simulation.

Open two terminals in the `build/` directory:
```bash
# Terminal 1: Continuously writes streaming data (simulates sensor logs)
./bitweave_producer /tmp/live_db

# Terminal 2: Concurrently executes sliding-window temporal range queries
./bitweave_consumer /tmp/live_db
```

---

## 💻 Technical Stack

- **Language:** C++17
- **Base Engine:** Google LevelDB (v1.23.0)
- **Testing:** GoogleTest (GTest), Google Benchmark
- **Build System:** CMake, Make
- **Environment:** Linux / Docker Containerization