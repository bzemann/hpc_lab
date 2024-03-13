#include <stdio.h>
#include <omp.h> // OpenMP

int main(int argc, char *argv[]) {
  // Get some OpenMP info & report collected info
  int nthreads = 0;
  int tid = 0;
#pragma omp parallel private(nthreads, tid)
  {
    nthreads = omp_get_num_threads();
    tid = omp_get_thread_num();
    printf("Hello world from thread %3d out of %d\n", tid, nthreads);
  }
  return 0;
}
