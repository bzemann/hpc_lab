#!/bin/bash
#SBATCH --job-name=hist_seq      # Job name
#SBATCH --output=hist_seq-%j.out # Output file
#SBATCH --error=hist_seq-%j.err  # Error file
#SBATCH --ntasks=1               # Number of tasks
#SBATCH --constraint=EPYC_7763   # Select node with CPU
#SBATCH --cpus-per-task=4        # Number of CPUs per task
#SBATCH --mem-per-cpu=1024       # Memory per CPU
#SBATCH --time=00:05:00          # Wall clock time limit

# Load some modules & list loaded modules
module load gcc
module list

# Compile
make clean
make

# Run
./hist_seq
