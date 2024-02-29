#!/bin/bash
#SBATCH --job-name=slurm_job_two      # Job name    (default: sbatch)
#SBATCH --output=slurm_job_two-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=slurm_job_two-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --nodes=2                     # Number of nodes
#SBATCH --ntasks=2                    # Number of tasks
#SBATCH --cpus-per-task=1             # Number of CPUs per task
#SBATCH --mem-per-cpu=1024            # Memory per CPU
#SBATCH --time=00:01:00               # Wall clock time limit

# load some modules & list loaded modules
module load gcc
module list

# print CPU model
lscpu | grep "Model name"

# run (srun: run job on cluster with provided resources/allocation)
srun hostname
