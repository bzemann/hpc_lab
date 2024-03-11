const char *dgemm_desc = "Blocked dgemm.";

//#pragma GCC optimize ("O3,fast-math")
//#pragma GCC optimize ("O3")
#pragma GCC optimize ("O3,fast-math,inline")

#define min(a, b) (((a) < (b)) ? (a) : (b))

/* This routine performs a dgemm operation
 *
 *  C := C + A * B
 *
 * where A, B, and C are lda-by-lda matrices stored in column-major format.
 * On exit, A and B maintain their input values.
 */
void square_dgemm(int n, double *restrict A, double *restrict B, double *restrict C) {
  // blocked matrix multiplication

  //int block_size = 200;
  //int block_size1 = 146;                                                   //opt for L2
  //int block_size2 = 36;                                                   //opt for L1d
  //int block_size = 100;
  //for(int i = 0; i < n; i += block_size1){
  //  for(int j = 0; j < n; j += block_size1){
  //    for(int k = 0; k < n; k += block_size1){
  //      //blocking
  //      for (int i1 = i; i1 < min(i + block_size1, n); i1++) {
  //        for (int j1 = j; j1 < min(j + block_size1, n); j1++) {
  //          double b = B[i1 + j1 * n];
  //          for (int k1 = k; k1 < min(k + block_size1, n); k1++) {
  //            C[k1 + j1 * n] += A[k1 + i1 * n] * b;
  //          }
  //        }
  //      }
  //    }
  //  }
  //}

  //tried to implement two level blocking, but currently it isn't working correctly

  //for (int i = 0; i < n; i += block_size1) {
  //  for (int j = 0; j < n; j += block_size1) {
  //    for (int k = 0; k < n; k += block_size1) {
  //      // block matrix multiplication
  //      //blocking for L2
  //      for(int i1 = i; i1 < min(i + block_size1, n); i1 += block_size2){
  //        for(int j1 = j; j1 < min(j + block_size1, n); j1 += block_size2){
  //          for(int k1 = k; k1 < min(k + block_size1, n); k1 += block_size2){
  //            //blocking for L1
  //            for(int i2 = i1; i2 < min(i1 + block_size2, n); i2++){
  //              for(int j2 = j1; j2 < min(j1 + block_size2, n); j2++){
  //                double b = B[i2 + j2 * n];
  //                for(int k2 = k1; k2 < min(k1 + block_size2, n); k2++){
  //                  C[k2 + j2 * n] += A[k2 + i2 * n] * b;
  //                }
  //              }
  //            }
  //          }
  //        }
  //      }
  //    }
  //  }
  //}

  for(int i = 0; i < n; i++){
      for(int j = 0; j < n; j++){
          double b = B[i + j * n];
          for(int k = 0; k < n; k++){
              C[k + j * n] += A[k + i * n] * b;
          }
      }
  }
}
