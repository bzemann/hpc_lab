#!/bin/bash
#SBATCH --job-name=fisher_scaling            # Job name    (default: sbatch)
#SBATCH --output=fisher_strong-scaling.out   # Output file (default: slurm-%j.out)
#SBATCH --error=fisher_strong-scaling.err    # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                           # Number of tasks
#SBATCH --constraint=EPYC_7763               # Select node with CPU
#SBATCH --cpus-per-task=32                   # Number of CPUs per task
#SBATCH --mem-per-cpu=1024                   # Memory per CPU
#SBATCH --time=10:00:00                      # Wall clock time limit

#load modules
module load gcc
module load python/3.11.6

module list

#compile code
make clean
make

#run strong scaling
python strong_scaling.py
python plot.py
