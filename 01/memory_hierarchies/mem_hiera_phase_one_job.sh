#!/bin/bash
#SBATCH --job-name=slurm_job_one      # Job name    (default: sbatch)
#SBATCH --output=slurm_job_one-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=slurm_job_one-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                    # Number of tasks
#SBATCH --cpus-per-task=1             # Number of CPUs per task
#SBATCH --mem-per-cpu=1024            # Memory per CPU
#SBATCH --time=01:00:00               # Wall clock time limit
#SBATCH --constraint=EPCY_7H12        # select cpu's from Euler VII phase one

#get cache sizes
lscpu

#get mem info
cat /proc/meminfo

#create mem figure
hwloc-ls --whole-system --no-io -f --of fig AMD_EPCY_7H12.fig