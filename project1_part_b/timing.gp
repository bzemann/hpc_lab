set title "nxn matrix multiplication on single-core AMD EPYC 7763"
set xlabel "Matrix size (n)"
set ylabel "Performance (GFlops/s)"
set grid
set logscale y 10

set terminal pdf
set output "timing.pdf"

plot "timing_basic_dgemm.data"   using 2:4 title "Naive dgemm"     \
                                 with linespoints,                 \
     "timing_blocked_dgemm.data" using 2:4 title "Blocked dgemm"   \
                                 with linespoints,                 \
     "timing_blas_dgemm.data"    using 2:4 title "Ref. BLAS dgemm" \
                                 with linespoints
