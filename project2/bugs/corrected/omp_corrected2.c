/* FILE: omp_bug2.c
 * DESCRIPTION:
 *   Another OpenMP program with a bug.
 ******************************************************************************/
#include <omp.h>
#include <stdio.h>
#include <stdlib.h>

//run-time bug race condition and tid out of scope
int main(int argc, char *argv[]) {
  int nthreads, i, tid;
  float total;

  #pragma omp parallel private(tid, i) shared(total)
  {
    tid = omp_get_thread_num();
    if(tid == 0){
      nthreads = omp_get_num_threads();
      printf("Number of threads = %d\n", nthreads);
    }
    printf("Thread %d is starting...\n", tid);

    #pragma omp barrier

    total = 0.0;

    #pragma omp for schedule(dynamic, 10)
    for(i = 0; i < 1000000; i++){
      #pragma omp atomic
      total = total + i * 1.0;
    }
    printf("Thread %d is done! Total= %e\n", tid, total);
  }
}