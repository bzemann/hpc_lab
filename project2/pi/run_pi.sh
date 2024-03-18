#!/bin/bash
#SBATCH --job-name=pi_calc
#SBATCH --output=pi-%j.out
#SBATCH --error=pi-%j.err
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem-per-cpu=1024
#SBATCH --constraint=EPYC_7763
#SBATCH --time=01:00:00

module load gcc

make

echo "serial"
./pi_serial | tee serial.data
echo
echo "omp critical"
./pi_omp_critical | tee critical.data
echo
echo "omp reduction"
./pi_omp_reduction | tee reduction.data

 
