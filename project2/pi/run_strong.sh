#!/bin/bash
#SBATCH --job-name=strong_omp     # Job name    (default: sbatch)
#SBATCH --output=pi-strong.out    # Output file (default: slurm-%j.out)
#SBATCH --error=pi-strong.err     # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=32       # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=01:00:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc
module list

# Compile
make clean
make

# Run the program for OMP_NUM_THREADS equal to 1, 2, 4, 8, ..., 64, 128
for ((i=0; i<=5; i++))
do
  OMP_NUM_THREADS=$((2**i))
  echo "Running with OMP_NUM_THREADS=$OMP_NUM_THREADS"
  echo "pi_serial"
  export OMP_NUM_THREADS
  ./pi_serial
  echo "pi_omp_critical"
  ./pi_omp_critical
  echo "pi_omp_reduction"
  ./pi_omp_reduction
done
