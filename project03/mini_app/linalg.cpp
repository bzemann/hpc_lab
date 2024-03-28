// linear algebra subroutines
// Ben Cumming @ CSCS

#include <iostream>

#include <cmath>
#include <cstdio>
#include <omp.h>

#include "linalg.h"
#include "operators.h"
#include "stats.h"
#include "data.h"

namespace linalg {

bool cg_initialized = false;
Field r;
Field Ap;
Field p;
Field v;
Field fv;

using namespace operators;
using namespace stats;
using data::Field;

// initialize temporary storage fields used by the cg solver
// I do this here so that the fields are persistent between calls
// to the CG solver. This is useful if we want to avoid malloc/free calls
// on the device for the OpenACC implementation (feel free to suggest a better
// method for doing this)
void cg_init(int nx) {
    Ap.init(nx,nx);
    r.init(nx,nx);
    p.init(nx,nx);
    v.init(nx,nx);
    fv.init(nx,nx);

    cg_initialized = true;
}

////////////////////////////////////////////////////////////////////////////////
//  blas level 1 reductions
////////////////////////////////////////////////////////////////////////////////

// computes the inner product of x and y
// x and y are vectors on length N
double hpc_dot(Field const& x, Field const& y, const int N) {
    double result = 0;

    for (int i = 0; i < N; i++) {
        result += x[i] * y[i];
    }

    return result;
}

// computes the 2-norm of x
// x is a vector on length N
double hpc_norm2(Field const& x, const int N) {
    double result = 0;
    result = hpc_dot(x, x, N);
    return sqrt(result);
}

// sets entries in a vector to value
// x is a vector on length N
// value is a scalar
void hpc_fill(Field& x, const double value, const int N) {
    for(int i = 0; i < N; i++){
        x[i] = value;
    }
}

////////////////////////////////////////////////////////////////////////////////
//  blas level 1 vector-vector operations
////////////////////////////////////////////////////////////////////////////////

// computes y := alpha*x + y
// x and y are vectors on length N
// alpha is a scalar
void hpc_axpy(Field& y, const double alpha, Field const& x, const int N) {
    for(int i = 0; i < N; i++){
        y[i] += x[i] * alpha;
    }
}

// computes y = x + alpha*(l-r)
// y, x, l and r are vectors of length N
// alpha is a scalar
void hpc_add_scaled_diff(Field& y, Field const& x, const double alpha,
                         Field const& l, Field const& r, const int N) {
    for(int i = 0; i < N; i++){
        y[i] = x[i] + alpha * (l[i] - r[i]);
    }
}

// computes y = alpha*(l-r)
// y, l and r are vectors of length N
// alpha is a scalar
void hpc_scaled_diff(Field& y, const double alpha, Field const& l,
                     Field const& r, const int N) {
    for(int i = 0; i < N; i++){
        y[i] = alpha * (l[i] - r[i]);
    }
}

// computes y := alpha*x
// alpha is scalar
// y and x are vectors on length n
void hpc_scale(Field& y, const double alpha, Field const& x, const int N) {
    for(int i = 0; i < N; i++){
        y[i] = alpha * x[i];
    }
}

// computes linear combination of two vectors y := alpha*x + beta*z
// alpha and beta are scalar
// y, x and z are vectors on length n
void hpc_lcomb(Field& y, const double alpha, Field const& x, const double beta,
               Field const& z, const int N) {
    for(int i = 0; i < N; i++){
        y[i] = alpha * x[i] + beta * z[i];
    }
}

// copy one vector into another y := x
// x and y are vectors of length N
void hpc_copy(Field& y, Field const& x, const int N) {
    for(int i = 0; i < N; i++){
        y[i] = x[i];
    }
}

// conjugate gradient solver
// solve the linear system J_{f}(y_old, y_new) \delta y = f(y_old, y_new)
// the Jacobian matrix J_{f} is implicit in the objective function for the
// diffusion equation (a simple finite difference approximation is used)
// ON ENTRY deltay contains the initial guess for the solution
// ON EXIT  deltay contains the solution
void hpc_cg(Field& deltay, Field const& y_old, Field const& y_new,
            Field const& f, const int maxiters, const double tol,
            bool& success) {
    // this is the dimension of the linear system that we are to solve
    using data::options;
    int N = options.N;
    int nx = options.nx;

    if (!cg_initialized) cg_init(nx);

    // epslion value use for matrix-vector approximation
    double eps     = 1.e-4;
    double eps_inv = 1. / eps;

    // initialize to zero
    hpc_fill(fv, 0.0, N);

    // tha Jacobian times deltay matrix vector multiplication is approximated
    // with J*deltay = 1/epsilon * ( f(y_new+epsilon*deltay) - f(y_new) )

    // v = y_new + epsilon*deltay
    hpc_lcomb(v, 1.0, y_new, eps, deltay, N);

    // fv = f(v)
    diffusion(y_old, v, fv);

    // r = b - A*x = f(y_new) - J*deltay
    // where A*x = (f(v) - f)/eps
    hpc_add_scaled_diff(r, f, -eps_inv, fv, f, N);

    // p = r
    hpc_copy(p, r, N);

    // r_old_inner = <r,r>
    double r_old_inner = hpc_dot(r, r, N), r_new_inner = r_old_inner;

    // check for convergence
    success = false;
    if (sqrt(r_old_inner) < tol) {
        success = true;
        return;
    }

    int iter;
    for(iter=0; iter<maxiters; iter++) {
        // Ap = A*p
        hpc_lcomb(v, 1.0, y_new, eps, p, N);
        diffusion(y_old, v, fv);
        hpc_scaled_diff(Ap, eps_inv, fv, f, N);

        // alpha = r_old_inner / p'*Ap
        double alpha = r_old_inner / hpc_dot(p, Ap, N);

        // x += alpha*p
        hpc_axpy(deltay, alpha, p, N);

        // r -= alpha*Ap
        hpc_axpy(r, -alpha, Ap, N);

        // find new norm
        r_new_inner = hpc_dot(r, r, N);

        // test for convergence
        if (sqrt(r_new_inner) < tol) {
            success = true;
            break;
        }

        // p = r + r_new_inner.r_old_inner * p
        hpc_lcomb(p, 1.0, r, r_new_inner / r_old_inner, p, N);

        r_old_inner = r_new_inner;
    }
    stats::iters_cg += iter + 1;

    if (!success) std::cerr << "ERROR: CG failed to converge" << std::endl;

}

} // namespace linalg
