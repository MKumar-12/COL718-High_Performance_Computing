# COL718 : High Performance Computing

This repository contains the codebase for assignments completed during the course structure of HPC (DIWALI-24). 
These assignments were completed as part of the COL718 course at IIT Delhi under the supervision of Prof. Kolin Paul.
They involve simulation, analysis, and optimization of computational tasks using the GEM5 simulator.

---

## Assignment 1a - Matrix Multiplication Performance Analysis

**Objective:** Analyze the performance of matrix multiplication on GEM5 by varying hardware parameters.

### Tasks:
- Implement matrix multiplication and simulate on GEM5.
- **Parameters:**
  - **CPU Models:** AtomicSimpleCPU, TimingSimpleCPU, DerivO3CPU.
  - **CPU Frequencies:** 600 MHz to 3.3 GHz (steps of 200 MHz).
  - **Memory Configurations:** DDR3, DDR4, DDR5, LPDDR5 variants.
- **Analysis:** Measure execution time, CPI, and evaluate the effect of different CPU models, frequencies, and memory configurations.

---

## Assignment 1b - Branch Prediction in GEM5

**Objective:** Study the impact of branch prediction strategies on blocked matrix multiplication performance.

### Tasks:
- Implement blocked matrix multiplication with a 30x30 matrix and 3x3 blocks.
- **Parameters:**
  - **CPU Models:** TimingSimpleCPU, DerivO3CPU.
  - **Branch Predictors:** BiModeBP, LocalBP, TAGE, TournamentBP.
  - **Fixed Configurations:** CPU frequency (2 GHz), DDR4 memory.
- **Analysis:** Evaluate branch prediction accuracy and performance metrics (e.g., branch taken/not taken).

---

## Assignment 2 - Cache Performance Analysis

**Objective:** Analyze cache behavior and its effect on matrix multiplication performance.

### Tasks:
- Simulate three matrix multiplication algorithms: `ijk`, `ikj`, and blocked MM (75x75 matrices, block size 15).
- **Parameters:**
  - **CPU Models:** TimingSimpleCPU, DerivO3CPU.
  - **Cache Configurations:** Vary L1/L2 sizes, associativity, and latency.
  - **Fixed Configurations:** CPU frequency (2 GHz), DDR4 memory.
- **Analysis:** Measure cache miss rates, execution time, and performance differences across configurations.

---

## Assignment 3 - Custom Instruction for GEM5

**Objective:** Implement a custom instruction for binomial coefficient calculation (nCr) in GEM5.

### Tasks:
- Add a custom instruction in the RISC-V ISA for binomial coefficient computation.
- Compare performance for evaluating binomial expansions `(A+X)^n` with and without the custom instruction.
- **Parameters:**
  - **Architecture:** RISC-V.
  - **Analysis:** Performance gain with custom instruction for varying values of `n`.
