#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <omp.h>

#include "walltime.h"

int main(int argc, char *argv[]) {
  int N = 2000000000;
  //int N = 20;
  double up = 1.00000001;
  double Sn = 1.00000001;
  int n;

  /* allocate memory for the recursion */
  double *opt = (double *)malloc((N + 1) * sizeof(double));
  if (opt == NULL) {
    perror("failed to allocate problem size");
    exit(EXIT_FAILURE);
  }
  printf("N: %d\n\n", N);
  double time_start = walltime();
  // TODO: YOU NEED TO PARALLELIZE THIS LOOP
  #pragma omp parallel shared(opt) firstprivate(up, N)  
  {
    int t_id = omp_get_thread_num();
    int nthreads = omp_get_num_threads();
    int items_per_thread = (N + 1) / nthreads;
    int t_beg = t_id * items_per_thread;
    int t_end = (t_id == nthreads - 1) ? N + 1 : (t_id + 1) * ((N + 1) / nthreads); 
    double local_up = pow(up, t_beg);
    double sn_local = Sn * local_up;

    for (n = t_beg; n < t_end; ++n) {
      opt[n] = sn_local;
      sn_local *= up;
    }
  } 
 Sn = opt[N];
  
  printf("Parallel RunTime  :  %f seconds\n", walltime() - time_start);
  printf("Final Result Sn   :  %.17g \n", Sn);

  double temp = 0.0;
  for (n = 0; n <= N; ++n) {
    temp += opt[n] * opt[n];
  }
  printf("Result ||opt||^2_2 :  %f\n", temp / (double)N);
  printf("\n");

  return 0;
}
