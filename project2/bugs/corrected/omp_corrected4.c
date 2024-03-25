/******************************************************************************
 * FILE: omp_bug4.c
 * DESCRIPTION:
 *   This very simple program causes a segmentation fault.
 ******************************************************************************/
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>
#define N 1048

//run-time bug a is on the stack and is private, should be on the heap
int main(int argc, char *argv[]) {
  int nthreads, tid, i, j;
  double **a;
  a = (double **)malloc(N * sizeof(double *));
  for (i = 0; i < N; i++){
    a[i] = (double *)malloc(N * sizeof(double));
  }
  /* Fork a team of threads with explicit variable scoping */
  #pragma omp parallel shared(nthreads) private(i, j, tid, a)
  {
    /* Obtain/print thread info */
    tid = omp_get_thread_num();
    if (tid == 0) {
      nthreads = omp_get_num_threads();
      printf("Number of threads = %d\n", nthreads);
    }
    printf("Thread %d starting...\n", tid);

    /* Each thread works on its own private copy of the array */
    for (i = 0; i < N; i++)
      for (j = 0; j < N; j++)
        a[i][j] = tid + i + j;

    /* For confirmation */
    printf("Thread %d done. Last element= %f\n", tid, a[N - 1][N - 1]);
    for (i = 0; i < N; i++){
      free(a[i]);
    }
    free(a);
  } /* All threads join master thread and disband */
}