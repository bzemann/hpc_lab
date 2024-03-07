const char *dgemm_desc = "Blocked dgemm.";

/* This routine performs a dgemm operation
 *
 *  C := C + A * B
 *
 * where A, B, and C are lda-by-lda matrices stored in column-major format.
 * On exit, A and B maintain their input values.
 */
void square_dgemm(int n, double *A, double *B, double *C) {
  // TODO: Implement the blocking optimization
  //       (The following is a placeholder naive three-loop dgemm)
  // column by column matrix multiplication
  //   for (int i = 0; i < n; ++i) {
  //     for (int j = 0; j < n; ++j) {
  //       for(int k = 0; k < n; ++k) {
  //         C[k+j*n] += A[k+i*n] * B[i+j*n];
  //       }
  //     }
  //   }
  // }

  // blocked matrix multiplication
  int block_size = 146;
  for (int i = 0; i < n; i += block_size) {
    for (int j = 0; j < n; j += block_size) {
      for (int k = 0; k < n; k += block_size) {
        // block matrix multiplication
        for (int i1 = i; i1 < i + block_size; i1++) {
          for (int j1 = j; j1 < j + block_size; j1++) {
            double b = B[i1 + j1 * n];
            for (int k1 = k; k1 < k + block_size; k1++) {
              C[k1 + j1 * n] += A[k1 + i1 * n] * b;
            }
          }
        }
      }
    }
  }
}
