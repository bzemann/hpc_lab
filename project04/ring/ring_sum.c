#include <mpi.h> // MPI
#include <stdio.h>

int main(int argc, char *argv[]) {

  // Initialize MPI, get size and rank
  int size, rank;
  MPI_Init(&argc, &argv);
  MPI_Comm_size(MPI_COMM_WORLD, &size);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);

  // IMPLEMENT: Ring sum algorithm
  int sum = 0; // initialize sum
  int buf[size];
  buf[0] = rank;
  sum += rank;
  for(int i = 1; i < size; i++){
    MPI_Send(&buf[i-1], 1, MPI_INT, (rank + 1) % size, 69, MPI_COMM_WORLD);
    MPI_Recv(&buf[i], 1, MPI_INT, (rank - 1) % size, 69, MPI_COMM_WORLD, MPI_STATUSES_IGNORE);
    sum += buf[i];
  }
  printf("Process %i: Sum = %i\n", rank, sum);
  
  // Finalize MPI
  MPI_Finalize();

  return 0;
}
