#!/bin/bash
#SBATCH --job-name=matrixmult
#SBATCH --output=matrixmult-%j.out
#SBATCH --error=matrixmult-%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --constraint=EPYC_7763
#SBATCH --time=00:20:00

# load some modules & list loaded modules
module load gcc openblas
module list

# set some environment variables
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1

# compile
make clean
make

echo "==== benchmark-naive ======================"
./benchmark-naive | tee timing_basic_dgemm.data
echo
echo "==== benchmark-blas ======================="
./benchmark-blas | tee timing_blas_dgemm.data
echo
echo "==== benchmark-blocked ===================="
./benchmark-blocked | tee timing_blocked_dgemm.data

echo
echo "==== plot results ========================="
gnuplot timing.gp
