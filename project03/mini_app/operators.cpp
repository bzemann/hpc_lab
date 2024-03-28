//******************************************
// operators.f90
// based on min-app code written by Oliver Fuhrer, MeteoSwiss
// modified by Ben Cumming, CSCS
// *****************************************

// Description: Contains simple operators which can be used on 3d-meshes

#include "operators.h"
#include "data.h"
#include "stats.h"

namespace operators {

// input: s, gives updated solution for f
// only handles interior grid points, as boundary points are fixed
// those inner grid points neighbouring a boundary point, will in the following
// be referred to as boundary points and only those grid points
// only neighbouring non-boundary points are called inner grid points
void diffusion(data::Field const &s_old, data::Field const &s_new,
               data::Field &f) {
  using data::options;

  using data::bndE;
  using data::bndN;
  using data::bndS;
  using data::bndW;

  double alpha = options.alpha;
  double beta = options.beta;

  int nx = options.nx;
  int iend = nx - 1;
  int jend = nx - 1;

// assumption: data is double data, a cacheline has 64 bytes <=> 8 doubles
// assure that 2 threads cannot share the same cacheline
#pragma omp parallel for schedule(static, 8) 
  for (int i = 1; i < iend; i++) {
    for (int j = 1; j < jend; j++) {
      f(i, j) = -(4. + alpha) * s_new(i, j) + s_new(i - 1, j) +
                s_new(i + 1, j) + s_new(i, j - 1) + s_new(i, j + 1) +
                beta * s_new(i, j) * (1. - s_new(i, j)) + alpha * s_old(i, j);
    }
  }

  // east boundary
#pragma omp parallel
  {
    {
      int i = nx - 1;
#pragma omp for schedule(dynamic) 
      for (int j = 1; j < jend; j++) {
        f(i, j) = -(4. + alpha) * s_new(i, j) + s_new(i - 1, j) + bndE[j] +
                  s_new(i, j - 1) + s_new(i, j + 1) + alpha * s_old(i, j) +
                  beta * s_new(i, j) * (1.0 - s_new(i, j));
      }
    }

    // west boundary
    {
      int i = 0;
#pragma omp for schedule(dynamic) 
      for (int j = 1; j < jend; j++) {
        f(i, j) = -(4. + alpha) * s_new(i, j) + bndW[j] + s_new(i + 1, j) +
                  s_new(i, j - 1) + s_new(i, j + 1) + alpha * s_old(i, j) +
                  beta * s_new(i, j) * (1.0 - s_new(i, j));
      }
    }

    // north boundary (plus NE and NW corners)
    {
      int j = nx - 1;

#pragma omp task
      {
        int i = 0; // NW corner
        f(i, j) = -(4. + alpha) * s_new(i, j) + bndW[j] + s_new(i + 1, j) +
                  s_new(i, j - 1) + bndN[i] + alpha * s_old(i, j) +
                  beta * s_new(i, j) * (1.0 - s_new(i, j));
      }

      // north boundary
#pragma omp for schedule(dynamic) 
      for (int i = 1; i < iend; i++) {
        f(i, j) = -(4. + alpha) * s_new(i, j) + s_new(i - 1, j) +
                  s_new(i + 1, j) + s_new(i, j - 1) + bndN[i] +
                  alpha * s_old(i, j) +
                  beta * s_new(i, j) * (1.0 - s_new(i, j));
      }

#pragma omp task
      {
        int i = nx - 1; // NE corner
        f(i, j) = -(4. + alpha) * s_new(i, j) + s_new(i - 1, j) + bndE[j] +
                  s_new(i, j - 1) + bndN[i] + alpha * s_old(i, j) +
                  beta * s_new(i, j) * (1.0 - s_new(i, j));
      }
    }

    // south boundary (plus SW and SE corners)
    {
      int j = 0;
#pragma omp task
      {
        int i = 0; // SW corner
        f(i, j) = -(4. + alpha) * s_new(i, j) + bndW[j] + s_new(i + 1, j) +
                  bndS[i] + s_new(i, j + 1) + alpha * s_old(i, j) +
                  beta * s_new(i, j) * (1.0 - s_new(i, j));
      }

      // south boundary
#pragma omp for schedule(dynamic) 
      for (int i = 1; i < iend; i++) {
        f(i, j) = -(4. + alpha) * s_new(i, j) + s_new(i - 1, j) +
                  s_new(i + 1, j) + bndS[i] + s_new(i, j + 1) +
                  alpha * s_old(i, j) +
                  beta * s_new(i, j) * (1.0 - s_new(i, j));
      }

#pragma omp task
      {
        int i = nx - 1; // SE corner
        f(i, j) = -(4. + alpha) * s_new(i, j) + s_new(i - 1, j) + bndE[j] +
                  bndS[i] + s_new(i, j + 1) + alpha * s_old(i, j) +
                  beta * s_new(i, j) * (1.0 - s_new(i, j));
      }
    }
  }
  // Accumulate the flop counts
  // 8 ops total per point
  stats::flops_diff += 12 * (nx - 2) * (nx - 2) // interior points
                       + 11 * (nx - 2 + nx - 2) // NESW boundary points
                       + 11 * 4;                // corner points
}

} // namespace operators
