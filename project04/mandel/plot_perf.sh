#!/bin/bash

module load gcc /4.8.5
module load gcc/6.3.0
module load gcc/8.2.0
module load gnuplot/5.2.0

LD_LIBRARY_PATH=LD_LIBRARY_PATH:/apps/gcc/gcc-6.1.0/lib64 gnuplot perf.gp
