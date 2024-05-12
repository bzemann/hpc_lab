#include "walltime.h"
#ifdef GETTIMEOFDAY
#include <sys/time.h> /* struct timeval, gettimeofday */
#else
#include <time.h> /* struct timespec, clock_gettime, CLOCK_MONOTONIC */
#endif

double walltime() {
#ifdef GETTIMEOFDAY
  struct timeval t;
  gettimeofday(&t, NULL);
  return 1. * t.tv_sec + 1.e-6 * t.tv_usec;
#else
  struct timespec t;
  clock_gettime(CLOCK_MONOTONIC, &t);
  return 1. * t.tv_sec + 1.e-9 * t.tv_nsec;
#endif
}
