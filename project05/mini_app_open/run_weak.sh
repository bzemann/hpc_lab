#!/bin/bash
#SBATCH --job-name=fisher_omp          # Job name    (default: sbatch)
#SBATCH --output=fisher_omp-weak.out   # Output file (default: slurm-%j.out)
#SBATCH --error=fisher_omp-weak.err    # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                     # Number of tasks
#SBATCH --constraint=EPYC_7763         # Select node with CPU
#SBATCH --cpus-per-task=64             # Number of CPUs per task
#SBATCH --mem-per-cpu=1024             # Memory per CPU
#SBATCH --time=10:00:00                # Wall clock time limit

module load gcc
module list

make clean
make

OUTPUT_FILE="weak_time.csv"
echo "Base Size,Size,Threads,Time" > "$OUTPUT_FILE"

base_sizes=(64 128 256)
runs=(1 2 3)
threads=(1 4 16 64)

for run in "${runs[@]}"; do
  # Determine the base size for the current run
  if [ $run -eq 1 ]; then
    base_size=${base_sizes[0]}  # First run starts with the first base size
  else
    base_size=${base_sizes[$((run - 1))]}  # Subsequent runs start with the next base size
  fi

  for size in "${base_sizes[@]}"; do
    multiplier=$((2 ** $run))
    adjusted_size=$((size * multiplier))

    # Select the appropriate thread count based on run and size
    thread_index=$((run - 1))  # Thread index starts from 0 for the first run
    thread_count=${threads[$thread_index]}

    echo "Run: $run, Base Size: $base_size, Size: $adjusted_size, Threads: $thread_count"

    OMP_NUM_THREADS=$thread_count
    export OMP_NUM_THREADS

    for repeat in {1..20}; do
      output=$(./main $adjusted_size 100 0.005)
      
      # Extracting time information
      time=$(echo "$output" | awk '/simulation took/ {print $4}')
      echo "$base_size,$adjusted_size,$thread_count,$time" >> "$OUTPUT_FILE"
    done
  done
done
