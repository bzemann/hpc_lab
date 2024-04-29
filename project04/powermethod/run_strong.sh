#!/bin/bash -l

#SBATCH --nodes=64
#SBATCH --ntasks=64
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --output=strong_times-median.out
#SBATCH --error=strong_times-median.err
#SBATCH --time=23:00:00
#SBATCH --constraint=EPYC_7763

make clean 
module load gcc openmpi
make

OUTPUT_FILE="strong_time-median.csv"
echo "Num-processes,Time" > "$OUTPUT_FILE"
#array of num MPI processes
procs=(1 2 4 8 16 32 64)

for p in "${procs[@]}"; do
  echo "num MPI processses: $p"
  for repeat in {1..60}; do
    output=$(mpirun -np $p ./powermethod_rows 3 10000 3000 -1e-6) 
    time=$(echo "$output" | grep -o "in [0-9]*\.[0-9]* second(s)" | awk '{print $2}')
    echo "$p,$time" >> "$OUTPUT_FILE"
  done
done

echo "DONE"
