#load required moduels
module load gcc

ARRAY_SIZE_ONE=9600000
ARRAY_SIZE_TWO=19200000

#Euler VII p1
gcc -O3 -march=native -DSTREAM_TYPE=double -DSTREAM_ARRAY_SIZE=${ARRAY_SIZE_ONE} -DNTIMES=20 stream.c -o stream_1
sbatch --constraint=EPYC_7H12 --mem-per-cpu=2G --output=stream_1.out --wrap "./stream_1"

#Euler VII p2
gcc -O3 -march=native -DSTREAM_TYPE=double -DSTREAM_ARRAY_SIZE=${ARRAY_SIZE_TWO} -DNTIMES=20 stream.c -o stream_2
sbatch --constraint=EPYC_7763 --mem-per-cpu=2G --output=stream_2.out --wrap "./stream_2"