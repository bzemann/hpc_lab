#include <stdio.h>
#include <stdlib.h>

#include <sys/time.h>
#include <time.h>
#include <unistd.h>

#include "consts.h"
#include "pngwriter.h"
#include "walltime.h"

int main(int argc, char **argv) {
  //png_data *pPng = png_create(IMAGE_WIDTH, IMAGE_HEIGHT);

  double x, y, x2, y2, cx, cy;

  double fDeltaX = (MAX_X - MIN_X) / (double)IMAGE_WIDTH;
  double fDeltaY = (MAX_Y - MIN_Y) / (double)IMAGE_HEIGHT;

  long nTotalIterationsCount = 0;

  long i, j;

  double time_start = walltime();
  
  //calculation serial
  cy = MIN_Y;
  for (j = 0; j < IMAGE_HEIGHT; j++) {
    cx = MIN_X;
    for (i = 0; i < IMAGE_WIDTH; i++) {
      x = cx;
      y = cy;
      x2 = x * x;
      y2 = y * y;
      // compute the orbit z, f(z), f^2(z), f^3(z), ...
      // count the iterations until the orbit leaves the circle |z|=2.
      // stop if the number of iterations exceeds the bound MAX_ITERS.
      int n = 0;
      for(; n < MAX_ITERS; ++n){
        if(x2 + y2 >= 2.0 * 2.0) break;
        y = 2 * x * y + cy;
        x = x2 - y2 + cx;
        
        x2 = x * x;
        y2 = y * y;
        
        ++nTotalIterationsCount;               
      }               
      // n indicates if the point belongs to the mandelbrot set
      // plot the number of iterations at point (i, j)
      int c = ((long)n * 255) / MAX_ITERS;
      //png_plot(pPng, i, j, c, c, c);
      cx += fDeltaX;
    }
    cy += fDeltaY;
    //precentage of outer loop completed, only for when runned locally
    /*if(j % (IMAGE_HEIGHT / 10) == 0){
      printf("procent: %g\n", (j * 100 / (double)IMAGE_HEIGHT));
    }*/    
  }
  
  
  double time_end = walltime();

  // print benchmark data
  printf("Total time:                 %g seconds\n",
         (time_end - time_start));
  printf("Image size:                 %ld x %ld = %ld Pixels\n",
         (long)IMAGE_WIDTH, (long)IMAGE_HEIGHT,
         (long)(IMAGE_WIDTH * IMAGE_HEIGHT));
  printf("Total number of iterations: %ld\n", nTotalIterationsCount);
  printf("Avg. time per pixel:        %g seconds\n",
         (time_end - time_start) / (double)(IMAGE_WIDTH * IMAGE_HEIGHT));
  printf("Avg. time per iteration:    %g seconds\n",
         (time_end - time_start) / (double)nTotalIterationsCount);
  printf("Iterations/second:          %g\n",
         nTotalIterationsCount / (time_end - time_start));
  // assume there are 8 floating point operations per iteration
  printf("MFlop/s:                    %g\n",
         nTotalIterationsCount * 8.0 / (time_end - time_start) * 1.e-6);

  //png_write(pPng, "mandel.png");
  return 0;
}
