#!/bin/bash -l
#
#SBATCH --job-name="deepspeed_example"
#SBATCH --time=02:00:00
#SBATCH --partition=amdrtx
#SBATCH --nodelist=ault[43-44]
#SBATCH --ntasks-per-node=1
#SBATCH --gpus-per-task=2
#SBATCH --mem=200G
#SBATCH --output=deepspeed_example.%j.o
#SBATCH --error=deepspeed_example.%j.e
#SBATCH --account=g34

module load openmpi/4.1.1
module load cuda/11.8.0
module load rdma-core/34.0
module load gcc/10.2.0

srun nvidia-smi -L

# export NCCL_DEBUG=INFO ## For debug
# export NCCL_TOPO_DUMP_FILE="/tmp/results/Topology_Intra_Node.txt" ## NCCL_PARAM(TopoDumpFileRank, "TOPO_DUMP_FILE_RANK", 0);
# export NCCL_GRAPH_DUMP_FILE="/tmp/results/Graph.txt" ## NCCL_PARAM(GraphDumpFileRank, "GRAPH_DUMP_FILE_RANK", 0);

rm -rf "$HOME/DeepSpeedExamples/training/HelloDeepSpeed/experiment_deepspeed"
mkdir -p "$HOME/DeepSpeedExamples/training/HelloDeepSpeed/experiment_deepspeed"
# pip install -r requirements.txt

export LD_PRELOAD=$HOME/nccl_goal_generator/third_party/nccl_nvtx/nccl/build/lib/libnccl.so


# srun bash ../example/run_ds.sh
nccl_goal_generator --training_script ../example/run_ds.sh --results_dir ../example/results --config_node_gpu ../example/node_gpu_config.yaml
# nccl_goal_generator --training_script ../example/run_ds.sh --results_dir ../example/results