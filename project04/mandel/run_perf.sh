#!/bin/bash -l

#SBATCH --nodes=16
#SBATCH --ntasks=16
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --output=job.out
#SBATCH --error=job.err
#SBATCH --time=01:20:00

#offset added to x coordinate so that gnuplot does not overlap the bars
offset=0 

rm -f perf.data
for np in 1 2 4 8 16
do
    echo "Computing Mandelbrot set with $np processes..."
    mpirun -np $np ./mandel_mpi > tmp.txt

    for i in `seq 0 $((np-1))`
    do
        t=$(cat tmp.txt | grep "\[Process $i\] Total time" | cut -d ":" -f2 | cut -d " " -f2)
        idx=$(echo $i + $offset | bc -l)
        printf "$np $idx $t \n" >> perf.data
    done
    rm tmp.txt

    offset=$(echo $offset + 0.2 | bc -l)
    printf "\n\n" >> perf.data
done

echo "Done."
