#!/bin/bash
#SBATCH --job-name=mandel_seq         # Job name    (default: sbatch)
#SBATCH --output=mandel_seq-8192.out  # Output file (default: slurm-%j.out)
#SBATCH --error=mandel_seq-8192.err   # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                    # Number of tasks
#SBATCH --constraint=EPYC_7763        # Select node with CPU
#SBATCH --cpus-per-task=1             # Number of CPUs per task
#SBATCH --mem-per-cpu=1024            # Memory per CPU
#SBATCH --time=01:00:00               # Wall clock time limit

#load modules
module load gcc

module list

make clean
make

#run mandel sequential
./mandel_seq
