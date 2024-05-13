#!/bin/bash -l

#SBATCH --nodes=64
#SBATCH --ntasks=64
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --output=fisher_mpi-strong.out # Output file (default: slurm-%j.out)
#SBATCH --error=fisher_mpi-strong.err  # Error file  (default: slurm-%j.out)
#SBATCH --constraint=EPYC_7763         # Select node with CPU
#SBATCH --time=15:00:00                # Wall clock time limit

module load gcc openmpi
module list

make clean
make

OUTPUT_FILE="mpi-strong_time.csv"
echo "Size,Threads,Time" > "$OUTPUT_FILE"

procs=(1 2 4 8 16)
sizes=(64 128 256 512 1024)

for s in "${sizes[@]}"; do
  echo "Size: $s"
  for p in "${procs[@]}"; do
    OMP_NUM_THREADS=$p
    export OMP_NUM_THREADS
    echo "num threads: $p"
    for repeat in {1..21}; do
      #SBATCH --nodes=$p
      #SBATCH --ntasks=$p
      output=$(mpirun -np $p ./main $s 100 0.005)
      time=$(echo "$output" | grep -oE 'simulation took [0-9]+\.[0-9]+ seconds' | grep -oE '[0-9]+\.[0-9]+')      
      if [ "$repeat" -ne 1 ]; then
        echo "$s,$p,$time" >> "$OUTPUT_FILE"
      fi
    done
  done
done
