#!/bin/bash -l

#SBATCH --nodes=64
#SBATCH --ntasks=64                     # Number of tasks
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --output=fisher_mpi-weak.out  # Output file (default: slurm-%j.out)
#SBATCH --error=fisher_mpi-weak.err  # Error file  (default: slurm-%j.out)
#SBATCH --constraint=EPYC_7763         # Select node with CPU
#SBATCH --time=10:00:00                # Wall clock time limit

module list

OUTPUT_FILE="mpi-weak_time.csv"
echo "Base-Size,Size,Threads,Time" > "$OUTPUT_FILE"

base_sizes=(64 128 256 512 1024 2048)
runs=(1 2 3)
procs=(1 4 16 64)

for run in "${runs[@]}"; do
  base_index=$((run - 1))
  base_size=${base_sizes[$base_index]}

  for ((i=0; i<4; i++)); do
    size_index=$((base_index + i))
    adjusted_size=${base_sizes[$size_index]}
    proc_count=${procs[$i]}

    echo "Run: $run, Base Size: $base_size, Size: $adjusted_size, Threads: $proc_count"

    OMP_NUM_THREADS=$proc_count
    export OMP_NUM_THREADS

    for repeat in {1..21}; do
      output=$(mpirun -np $p ./main $adjusted_size 100 0.005)
      
      # Extracting time information
      time=$(echo "$output" | grep -oE 'simulation took [0-9]+\.[0-9]+ seconds' | grep -oE '[0-9]+\.[0-9]+')      
      echo "$base_size,$adjusted_size,$proc_count,$time" >> "$OUTPUT_FILE"
      if [ "$repeat" -ne 1 ]; then
        echo "$base_size,$adjusted_size,$proc_count,$time" >> "$OUTPUT_FILE"
      fi
    done
  done
done
