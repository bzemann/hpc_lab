#!/bin/bash
#SBATCH --job-name=fisher_omp          # Job name    (default: sbatch)
#SBATCH --output=fisher_omp-strong.out # Output file (default: slurm-%j.out)
#SBATCH --error=fisher_omp-strong.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                     # Number of tasks
#SBATCH --constraint=EPYC_7763         # Select node with CPU
#SBATCH --cpus-per-task=48             # Number of CPUs per task
#SBATCH --mem-per-cpu=1024             # Memory per CPU
#SBATCH --time=06:00:00                # Wall clock time limit

module load gcc
module list

make clean
make

OUTPUT_FILE="strong_time.csv"
echo "Size,Threads,Time" > "$OUTPUT_FILE"

threads=(1 2 4 8 16)
sizes=(64 128 256 512 1024)

for s in "${sizes[@]}"; do
  echo "Size: $s"
  for t in "${threads[@]}"; do
    OMP_NUM_THREADS=$t
    export OMP_NUM_THREADS
    echo "num threads: $t"
    for repeat in {1..20}; do
      output=$(./main $s 100 0.005)
      time=$(echo "$output" | grep -oE 'simulation took [0-9]+\.[0-9]+ seconds' | grep -oE '[0-9]+\.[0-9]+')      
      echo "$s,$t,$time" >> "$OUTPUT_FILE"
    done
  done
done
