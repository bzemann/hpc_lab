CC     ?= gcc
CFLAGS  = -O2 -fopenmp

all: pi_serial pi_omp_critical pi_omp_reduction

pi_serial: pi_serial.o walltime.o
	$(CC) $(CFLAGS) $^ -o $@

pi_serial.o: pi_serial.c walltime.h
	$(CC) -c $(CFLAGS) $<

pi_omp_critical: pi_omp_critical.o walltime.o
	$(CC) $(CFLAGS) $^ -o $@

pi_omp_critical.o: pi_omp_critical.c walltime.h
	$(CC) -c $(CFLAGS) $<

pi_omp_reduction: pi_omp_reduction.o walltime.o
	$(CC) $(CFLAGS) $^ -o $@

pi_omp_reduction.o: pi_omp_reduction.c walltime.h
	$(CC) -c $(CFLAGS) $<

walltime.o: walltime.c walltime.h
	$(CC) -c $(CFLAGS) $<

.PHONY: clean
clean:
	$(RM) *.o pi_serial pi_omp_critical pi_omp_reduction *.data
