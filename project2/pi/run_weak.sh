#!/bin/bash
#SBATCH --job-name=weak_omp       # Job name    (default: sbatch)
#SBATCH --output=pi-weak.out      # Output file (default: slurm-%j.out)
#SBATCH --error=pi-weak.err       # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                # Number of tasks
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=128       # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=01:00:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc
module list

# Compile
make clean
make

# Run the program for OMP_NUM_THREADS equal to 1, 2, 4, 8, ..., 64, 128
for ((i=0; i<=7; i++))
do
  OMP_NUM_THREADS=$((2**i))
  echo "Running with OMP_NUM_THREADS=$OMP_NUM_THREADS"
  export OMP_NUM_THREADS
  N=$((OMP_NUM_THREADS*1000000))
  echo "pi_serial"
  ./pi_serial ${N}
  echo "pi_omp_critical"
  ./pi_omp_critical ${N}
  echo "pi_omp_reduction"
  ./pi_omp_reduction ${N}
done
