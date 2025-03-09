#!/bin/bash -l
#SBATCH --job-name="npkit_benchmark_example_allreduce"
#SBATCH --time=02:10:00
#SBATCH --partition=amdrtx
#SBATCH --nodelist=ault[41,42]
#SBATCH --ntasks-per-node=2
#SBATCH --gpus-per-task=1
#SBATCH --output=example_allreduce.%j.o
#SBATCH --error=example_allreduce.%j.e
#SBATCH --account=g34

module load openmpi/4.1.1
module load cuda/11.8.0

srun nvidia-smi -L

rm -rf "./results"
mkdir -p "./results"

export NCCL_ALGO=Ring
export NCCL_PROTO=Simple
# export NCCL_DEBUG=INFO
export MPI_ROOT=/apps/ault/spack/opt/spack/linux-centos8-zen/gcc-8.4.1/openmpi-4.1.1-epxpvnwjl2smjwuwqg67h2wrmdxw6nhj
export NCCL_ROOT=/users/zhu/nccl_goal_generator/third_party/nccl_npkit/nccl/build
export LD_LIBRARY_PATH=/users/zhu/nccl_goal_generator/third_party/nccl_npkit/nccl/build/lib:$LD_LIBRARY_PATH

nvcc -I${MPI_ROOT}/include -L${MPI_ROOT}/lib -lmpi -I${NCCL_ROOT}/include -L${NCCL_ROOT}/lib -lnccl example_allreduce.cu -o example_allreduce

for index in $(seq 0 9); do
    iteration_dir="./results/${index}"
    mkdir -p $iteration_dir

    size=$((1))
    while [ $size -le $((4 * 1024 * 1024)) ]; do
        size_dir="${iteration_dir}/${size}"
        mkdir -p $size_dir

        export NPKIT_RUN_DIR="${size_dir}/npkit_run"
        mkdir -p $NPKIT_RUN_DIR

        # Update NPKit environment variables
        npkit_dump_dir="${NPKIT_RUN_DIR}/npkit_dump"  # Path to NPKit dump directory
        npkit_trace_dir="${NPKIT_RUN_DIR}/npkit_trace"  # Path to NPKit post-process directory
        npkit_result_dir="${NPKIT_RUN_DIR}/npkit_result"  # Path to NPKit result directory
        export NPKIT_DUMP_DIR="${npkit_dump_dir}"  # Path to generate dump files

        # Create directories for NPKit
        rm -rf $npkit_dump_dir
        rm -rf $npkit_trace_dir
        rm -rf $npkit_result_dir
        mkdir -p $npkit_dump_dir
        mkdir -p $npkit_trace_dir
        mkdir -p $npkit_result_dir

        # Run experiment and capture logs
        srun ./example_allreduce $size | tee $npkit_result_dir/log.txt

        # Process NPKit trace
        python3 npkit_dependency_trace_generator.py --npkit_dump_dir=$npkit_dump_dir \
                                        --npkit_event_header_path="/users/zhu/nccl_goal_generator/third_party/nccl_npkit/nccl/src/include/npkit/npkit_event.h" \
                                        --output_dir=$npkit_trace_dir

        # Update size for the next iteration
        size=$((size * 2))
    done
done

python3 get_npkit_statistics.py 

python3 summary.py 

python3 plot.py