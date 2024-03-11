const char *dgemm_desc = "Blocked dgemm.";

//#pragma GCC optimize ("-O3,-fast-math")
//#pragma GCC optimize ("-O3")
#pragma GCC optimize ("-O3, -ffast-math, -finline")

#define min(a, b) (((a) < (b)) ? (a) : (b))

/* This routine performs a dgemm operation
 *
 *  C := C + A * B
 *
 * where A, B, and C are lda-by-lda matrices stored in column-major format.
 * On exit, A and B maintain their input values.
 */
void square_dgemm(int n, double *A, double *B, double *C) {
  // blocked matrix multiplication

  //int block_size = 200;
  int block_size = 146;                                                   //opt for L2
  //int block_size = 36                                                   //opt for L1d
  //int block_size = 100
  for (int i = 0; i < n; i += block_size) {
    for (int j = 0; j < n; j += block_size) {
      for (int k = 0; k < n; k += block_size) {
        // block matrix multiplication
        for (int i1 = i; i1 < min(i + block_size, n); i1++) {
          for (int j1 = j; j1 < min(j + block_size, n); j1++) {
            double b = B[i1 + j1 * n];
            for (int k1 = k; k1 < min(k + block_size, n); k1++) {
              C[k1 + j1 * n] += A[k1 + i1 * n] * b;
            }
          }
        }
      }
    }
  }
}
