#!/bin/bash
#SBATCH --job-name=mem_job_two        # Job name    (default: sbatch)
#SBATCH --output=mem_job_two-%j.out   # Output file (default: slurm-%j.out)
#SBATCH --error=mem_job_two-%j.err    # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                    # Number of tasks
#SBATCH --cpus-per-task=1             # Number of CPUs per task
#SBATCH --mem-per-cpu=1024            # Memory per CPU
#SBATCH --time=00:01:00               # Wall clock time limit
#SBATCH --constraint=EPYC_7763        # select cpu's from Euler VII phase two

#get cache sizes
lscpu

#get mem info
cat /proc/meminfo

#create mem figure
hwloc-ls --whole-system --no-io -f --of fig AMD_EPCY_7763.fig
