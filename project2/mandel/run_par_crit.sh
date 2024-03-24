#!/bin/bash
#SBATCH --job-name=mandel_crit        # Job name    (default: sbatch)
#SBATCH --output=mandel_crit-.out     # Output file (default: slurm-%j.out)
#SBATCH --error=mandel_crit-.err      # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                    # Number of tasks
#SBATCH --constraint=EPYC_7763        # Select node with CPU
#SBATCH --cpus-per-task=64            # Number of CPUs per task
#SBATCH --mem-per-cpu=1024            # Memory per CPU
#SBATCH --time=01:00:00               # Wall clock time limit

#load modules
module load gcc

module list

make clean
make

#run mandel parallel with critical
./mandel_par_crit