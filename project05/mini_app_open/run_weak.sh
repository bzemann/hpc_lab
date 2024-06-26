#!/bin/bash
#SBATCH --job-name=fisher_omp-w          # Job name    (default: sbatch)
#SBATCH --output=fisher_omp-weak.out  # Output file (default: slurm-%j.out)
#SBATCH --error=fisher_omp-weak.err  # Error file  (default: slurm-%j.out)
#SBATCH --ntasks=1                     # Number of tasks
#SBATCH --constraint=EPYC_7763         # Select node with CPU
#SBATCH --cpus-per-task=64             # Number of CPUs per task
#SBATCH --mem-per-cpu=1024             # Memory per CPU
#SBATCH --time=10:00:00                # Wall clock time limit

module load gcc
module list

OUTPUT_FILE="weak_time.csv"
echo "Base-Size,Size,Threads,Time" > "$OUTPUT_FILE"

base_sizes=(64 128 256 512 1024 2048)
runs=(1 2 3)
threads=(1 4 16 64)

for run in "${runs[@]}"; do
  base_index=$((run - 1))
  base_size=${base_sizes[$base_index]}

  for ((i=0; i<4; i++)); do
    size_index=$((base_index + i))
    adjusted_size=${base_sizes[$size_index]}
    thread_count=${threads[$i]}

    echo "Run: $run, Base Size: $base_size, Size: $adjusted_size, Threads: $thread_count"

    OMP_NUM_THREADS=$thread_count
    export OMP_NUM_THREADS

    for repeat in {1..21}; do
      output=$(./main $adjusted_size 100 0.005)
      
      # Extracting time information
      if [ "repeat" -ne 1 ]; then
        time=$(echo "$output" | grep -oE 'simulation took [0-9]+\.[0-9]+ seconds' | grep -oE '[0-9]+\.[0-9]+')      
        echo "$base_size,$adjusted_size,$thread_count,$time" >> "$OUTPUT_FILE"
      fi
    done
  done
done
