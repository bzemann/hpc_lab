#include <mpi.h> // MPI
#include <stdio.h>

int main(int argc, char *argv[]) {

  // Initialize MPI and get info
  int size, rank, len;
  char pname[MPI_MAX_PROCESSOR_NAME];
  MPI_Init(&argc, &argv);
  MPI_Comm_size(MPI_COMM_WORLD, &size);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  MPI_Get_processor_name(pname, &len);

  // Report collected info
  printf("Hello world from rank %d out of %d on %s\n", rank, size, pname);

  // Finalize MPI
  MPI_Finalize();

  return 0;
}
