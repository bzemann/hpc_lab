#!/bin/bash
#SBATCH --job-name=hello_mpi      # Job name    (default: sbatch)
#SBATCH --output=hello_mpi-%j.out # Output file (default: slurm-%j.out)
#SBATCH --error=hello_mpi-%j.err  # Error file  (default: slurm-%j.out)
#SBATCH --nodes=4                 # Number of nodes
#SBATCH --ntasks=4                # Number of tasks
#SBATCH --ntasks-per-node=1       # Number of tasks per node
#SBATCH --constraint=EPYC_7763    # Select node with CPU
#SBATCH --cpus-per-task=1         # Number of CPUs per task
#SBATCH --mem-per-cpu=1024        # Memory per CPU
#SBATCH --time=00:05:00           # Wall clock time limit

# Load some modules & list loaded modules
module load gcc openmpi
module list

# Compile
make clean
make

# Run the program with 4 MPI processes on 4 different nodes
mpirun ./hello_mpi
