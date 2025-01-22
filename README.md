# nccl_goal_generator

## 1. Introduction

**nccl_goal_generator** is a toolchain for **tracing and parsing [NCCL](https://github.com/NVIDIA/nccl) communication** data, producing a compiled `goal` file that can be fed into [LogGOPSim](https://github.com/spcl/LogGOPSim) for large-scale network simulation.

This toolchain includes:

1. **NCCL Tracer** – intercepts and records NCCL calls and events (via [nccl_nvtx_v2.20.5-1](https://github.com/ZhiyiHu1999/nccl_nvtx_v2.20.5-1) and [Nsight Systems](https://developer.nvidia.com/nsight-systems)).
2. **Trace Parser** – converts the collected NCCL trace into a `goal` file compatible with [LogGOPSim](https://github.com/spcl/LogGOPSim).
3. **Sample scripts and examples** – show how to enable tracing in GPU applications, as well as how to process and visualize the resulting data.

> **Disclaimer**: This project is **not** affiliated with or endorsed by [NVIDIA](https://www.nvidia.com/).
> **NCCL** and **NVTX** remain the property of NVIDIA or its affiliates.
> This toolchain simply extends and integrates these libraries to enable custom tracing and simulation workflows.

---

## 2. Features & Workflow

1. **Tracing NCCL Communication**

   - During distributed GPU execution, insert tracing hooks (e.g., via [nccl_nvtx](https://github.com/ZhiyiHu1999/nccl_nvtx_v2.20.5-1)) to record all major NCCL calls along with timestamps.
   - Optionally pair with [Nsight Systems](https://developer.nvidia.com/nsight-systems) to gather additional performance data.
2. **Trace Parsing & Goal File Generation**

   - Once the GPU job completes, a raw NCCL trace file (e.g., JSON, log) is produced.
   - Our parser (or script) reads this trace and outputs a LogGOPSim-compatible `goal` file.
3. **Offline Network Simulation with LogGOPSim**

   - Pass the resulting `goal` file to [LogGOPSim](https://github.com/spcl/LogGOPSim) to simulate large-scale network topologies and evaluate performance bottlenecks, scalability, bandwidth usage, and more.
   - Compare simulation outputs to real-world measurements to refine your network design or distribution strategy.

---

## 3. Dependencies & Installation

### 3.1 Cloning this Repository

To clone this repository along with its submodules, use:

```bash
git clone --recursive https://github.com/ZhiyiHu1999/nccl_goal_generator
cd nccl_goal_generator
```

### 3.2 Install Required Dependencies

1. **nccl_nvtx_v2.20.5-1** (NCCL with  NVTX annotations)

   - [Repository](https://github.com/ZhiyiHu1999/nccl_nvtx_v2.20.5-1)
   - Used as a submodule.
   - To install:

   ```bash
   cd third_party/nccl_nvtx
   bash make_ault.sh
   ```
2. **Nsight Systems**

    - For profiling, post-processing, and parsing nccl traces, the tracer should work with [Nsight Systems](https://developer.nvidia.com/nsight-systems)
    - Recommanded Version: `Nsight Systems 2024.5.1`
    - To install:

    ```bash
    wget https://developer.nvidia.com/downloads/assets/tools/secure/nsight-systems/2024_5/NsightSystems-linux-cli-public-2024.5.1.113-3461954.rpm
    rpm2cpio NsightSystems-linux-cli-public-2024.5.1.113-3461954.rpm | cpio -idmv

    ## To verify the installation:
    nsys --version
    ## A successful installation should output like:
    NVIDIA Nsight Systems version 2020.4.3.7-10543b6

    ## To verify the installation:
    which nsys
    ## A successful installation should output like:
    /usr/local/bin/nsys
    ```
3. **LogGOPSim**

   - [Repository](https://github.com/spcl/LogGOPSim)
   - Used as a submodule.
   - Consumes the `goal` file generated for network simulation.
4. **Graphviz**

   - [Graphviz website](https://graphviz.org/).
   - For goal file visualization.
   - To install:

   ```bash
   wget https://gitlab.com/api/v4/projects/4207231/packages/generic/graphviz-releases/12.2.1/rocky_8.9_graphviz-12.2.1-cmake.rpm
   mkdir -p ~/graphviz
   rpm2cpio rocky_8.9_graphviz-12.2.1-cmake.rpm | cpio -idmv -D ~/graphviz

   echo 'export PATH=~/graphviz/usr/bin:$PATH' >> ~/.bashrc
   echo 'export LD_LIBRARY_PATH=~/graphviz/usr/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
   source ~/.bashrc
   ```
