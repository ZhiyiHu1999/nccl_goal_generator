#!/bin/bash -l
#SBATCH --job-name="check-env"
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1        # Do not change
#SBATCH --partition=normal
#SBATCH --account=a-g34
#SBATCH --time=00:10:00            # total run time limit (HH:MM:SS)
#SBATCH --output=check_env.%j.o
#SBATCH --error=check_env.%j.e

srun --mpi=pmi2 --environment=megatron bash -c '
    echo "Check mpirun location"
    which mpirun

    echo "Check mpicc location"
    which mpicc

    echo "Check nvcc location"
    which nvcc
'