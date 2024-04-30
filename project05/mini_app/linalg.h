// linear algebra subroutines
// Ben Cumming @ CSCS

#ifndef LINALG_H
#define LINALG_H

#include "data.h"

namespace linalg {

using data::Field;

extern bool cg_initialized;
extern Field r, Ap, p, v, fv;

// initialize temporary storage fields used by the cg solver
// I do this here so that the fields are persistent between calls
// to the CG solver. This is useful if we want to avoid malloc/free calls
// on the device for the OpenACC implementation (feel free to suggest a
// better method for doing this)
void cg_init(const int N);

////////////////////////////////////////////////////////////////////////////////
//  blas level 1 reductions
////////////////////////////////////////////////////////////////////////////////

// computes the inner product of x and y
// x and y are vectors on length N
double hpc_dot(Field const& x, Field const& y);

// computes the 2-norm of x
// x is a vector on length N
double hpc_norm2(Field const& x);

// sets entries in a vector to value
// x is a vector on length N
// value is th
void hpc_fill(Field& x, const double value);

////////////////////////////////////////////////////////////////////////////////
//  blas level 1 vector-vector operations
////////////////////////////////////////////////////////////////////////////////

// computes y := alpha*x + y
// x and y are vectors on length N
// alpha is a scalar
void hpc_axpy(Field& y, const double alpha, Field const& x);

// computes y = x + alpha*(l-r)
// y, x, l and r are vectors of length N
// alpha is a scalar
void hpc_add_scaled_diff(Field& y, Field const& x, const double alpha,
                         Field const& l, Field const& r);

// computes y = alpha*(l-r)
// y, l and r are vectors of length N
// alpha is a scalar
void hpc_scaled_diff(Field& y, const double alpha, Field const& l,
                     Field const& r);

// computes y := alpha*x
// alpha is scalar
// y and x are vectors on length n
void hpc_scale(Field& y, const double alpha, Field const& x);

// computes linear combination of two vectors y := alpha*x + beta*z
// alpha and beta are scalar
// y, x and z are vectors on length n
void hpc_lcomb(Field& y, const double alpha, Field const& x, const double beta,
               Field const& z);

// copy one vector into another y := x
// x and y are vectors of length N
void hpc_copy(Field& y, Field const& x);

// conjugate gradient solver
// solve the linear system J_{f}(y_old, y_new) \delta y = f(y_old, y_new)
// the Jacobian matrix J_{f} is implicit in the objective function for the
// diffusion equation (a simple finite difference approximation is used)
// ON ENTRY deltay contains the initial guess for the solution
// ON EXIT  deltay contains the solution
void hpc_cg(Field& deltay, Field const& y_old, Field const& y_new,
            Field const& f, const int maxiters, const double tol,
            bool& success);

}

#endif /* LINALG_H */
