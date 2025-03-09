#!/bin/bash -l
#SBATCH --job-name="npkit-benchmark"
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=1        # Do not change
#SBATCH --gpus-per-node=1          # number of gpus per node
#SBATCH --partition=normal
#SBATCH --account=a-g34
#SBATCH --mem=200G
#SBATCH --time=02:20:00            # total run time limit (HH:MM:SS)
#SBATCH --output=npkit_benchmark.%j.o
#SBATCH --error=npkit_benchmark.%j.e

rm -rf "./results"
mkdir -p "./results"

rm npkit_data_summary_LL.json

rm -rf "./plots"
mkdir -p "./plots"

export WORK_ROOT=/users/zhu/nccl_goal_generator/npkit_benchmark/clariden/LL

srun --mpi=pmi2 --environment=megatron bash -c '
    if [ "$SLURM_NODEID" -eq 0 ]; then
        export MPI_ROOT=/usr/local/mpi
        export NCCL_ROOT=/users/zhu/nccl_goal_generator/third_party/nccl_npkit/nccl/build
        export LD_LIBRARY_PATH=/users/zhu/nccl_goal_generator/third_party/nccl_npkit/nccl/build/lib:$LD_LIBRARY_PATH
        export WORK_ROOT=/users/zhu/nccl_goal_generator/npkit_benchmark/clariden/LL

        nvcc -I${MPI_ROOT}/include -L${MPI_ROOT}/lib -lmpi -I${NCCL_ROOT}/include -L${NCCL_ROOT}/lib -lnccl $WORK_ROOT/example_allreduce.cu -o $WORK_ROOT/example_allreduce
        echo "nvcc compile successful"
    fi
'

wait

for index in $(seq 0 9); do
    iteration_dir="$WORK_ROOT/results/${index}"
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
        srun --mpi=pmi2 --environment=megatron bash -c "
            export NCCL_ALGO=Ring
            export NCCL_PROTO=LL
            # export NCCL_DEBUG=INFO

            export MPI_ROOT=/usr/local/mpi
            export NCCL_ROOT=/users/zhu/nccl_goal_generator/third_party/nccl_npkit/nccl/build
            export LD_LIBRARY_PATH=/users/zhu/nccl_goal_generator/third_party/nccl_npkit/nccl/build/lib:$LD_LIBRARY_PATH
            export WORK_ROOT=/users/zhu/nccl_goal_generator/npkit_benchmark/clariden/LL

            $WORK_ROOT/example_allreduce $size | tee $npkit_result_dir/log.txt
        "

        python3 npkit_dependency_trace_generator.py --npkit_dump_dir=$npkit_dump_dir \
                                        --npkit_event_header_path="/users/zhu/nccl_goal_generator/third_party/nccl_npkit/nccl/src/include/npkit/npkit_event.h" \
                                        --output_dir=$npkit_trace_dir

        rm -rf $npkit_dump_dir
        rm -rf $npkit_result_dir

        # Update size for the next iteration
        size=$((size * 2))
    done
done

python3 get_npkit_statistics.py 

python3 summary.py 

srun --mpi=pmi2 --environment=megatron bash -c '
    export WORK_ROOT=/users/zhu/nccl_goal_generator/npkit_benchmark/clariden/LL

    if [ "$SLURM_NODEID" -eq 0 ]; then
        pip install seaborn
        python3 $WORK_ROOT/plot.py -i $WORK_ROOT/npkit_data_summary_LL.json
        cp -r ./plots $WORK_ROOT
    fi
'
