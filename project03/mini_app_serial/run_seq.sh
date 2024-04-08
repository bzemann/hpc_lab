#!/bin/bash
#SBATCH --job-name=fisher_seq                # Job name    (default: sbatch)
#SBATCH --output=fisher_seq.out              # Output file (default: slurm-%j.out)
#SBATCH --error=fisher_seq.err               # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                           # Number of tasks
#SBATCH --constraint=EPYC_7763               # Select node with CPU
#SBATCH --cpus-per-task=4                    # Number of CPUs per task
#SBATCH --mem-per-cpu=1024                   # Memory per CPU
#SBATCH --time=20:00:00                      # Wall clock time limit

#load modules
module load gcc
module load python/3.11.6

module list

#compile
make clean
make 

#run fisher
./main

#plot result
python plot.py

#compile
make clean
make 

#run fisher
./main

#plot result
python plot.py
module load python/3.11.6