#!/bin/bash -l

#SBATCH --nodes=64
#SBATCH --ntasks=64
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --output=weak_times-median.out
#SBATCH --error=weak_times-median.err
#SBATCH --time=10:00:00
#SBATCH --constraint=EPYC_7763

make clean 
module load gcc openmpi
make

OUTPUT_FILE="weak_time-median.csv"
echo "Num-processes,Time" > "$OUTPUT_FILE"
#array of num MPI processes
procs=(1 2 4 8 16 32 64)
sizes=(1 1.414 2 2.828 4 5.657 8)

for i in "${!procs[@]}"; do
  echo "num MPI processses: $p"
  for repeat in {1..52}; do
    p=${procs[$i]}
    s=$(echo "${sizes[$i]} * 1000" | bc)
    output=$(mpirun -np $p ./powermethod_rows 3 $s 3000 -1e-6) 
    time=$(echo "$output" | grep -o "in [0-9]*\.[0-9]* second(s)" | awk '{print $2}')
    echo "$p,$time" >> "$OUTPUT_FILE"
  done
done

echo "DONE"
