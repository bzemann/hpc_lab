#!/bin/bash

#SBATCH --constraint=EPYC_7763
#SBATCH --nodes=32
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=1
#SBATCH --error=scaling.err
#SBATCH --output=scaling.out
#SBATCH --time=24:00:00

module load gcc openmpi python
source /cluster/home/grafrap/5/hpc_python/project05_venv/bin/activate

# Define the domain size
domain_width=4001
domain_height=4001

# Define the number of tasks for each workload
workload_1_tasks=50
workload_2_tasks=100

# Files to store results
results_file_50="results_50_tasks.csv"
results_file_100="results_100_tasks.csv"
echo "Num Workers,Time Taken" > "$results_file_50" # Initialize CSV file with header for 50 tasks
echo "Num Workers,Time Taken" > "$results_file_100" # Initialize CSV file with header for 100 tasks

# Loop through the number of workers from 2 to 32
for num_workers in {2..32}; do
  for repeat in {1..51}; do
    echo "Running with $num_workers workers..."

    # Run the program for 50 tasks and capture output
    output=$(srun --ntasks=$num_workers --constraint=EPYC_7763 --nodes=$num_workers python3 manager_worker.py $domain_width $domain_height $workload_1_tasks)
    # Parse time taken from output
    time_taken=$(echo "$output" | grep "Run took" | awk '{print $3}')
    # Append results to CSV for 50 tasks
    echo "$num_workers,$time_taken" >> "$results_file_50"

    # Run the program for 100 tasks and capture output
    output=$(srun --ntasks=$num_workers --constraint=EPYC_7763 --nodes=$num_workers python3 manager_worker.py $domain_width $domain_height $workload_2_tasks)
    # Parse time taken from output
    time_taken=$(echo "$output" | grep "Run took" | awk '{print $3}')
    # Append results to CSV for 100 tasks
    echo "$num_workers,$time_taken" >> "$results_file_100"
  done
done
