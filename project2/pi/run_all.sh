#!/bin/bash
#SBATCH --job-name=omp_scaling    # Job name    (default: sbatch)
#SBATCH --output=pi-scaling.out   # Output file (default: slurm-%j.out)
#SBATCH --error=pi-scaling.err    # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=128       # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=01:00:00           # Wall clock time limit

# Load some modules
module load gcc
module load python/3.11.6

module list

# Compile
make clean
make

python run_all.py
