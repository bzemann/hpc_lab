CC     = gcc-13
CFLAGS = -O3 -fopenmp
HDR_DEPS = ../walltime.h
SRC_DEPS = ../walltime.c

all: quicksort_seq quicksort_par

quicksort_par: quicksort_par.o walltime.o
	$(CC) $(CFLAGS) $^ -o $@

quicksort_seq: quicksort_seq.o walltime.o
	$(CC) $(CFLAGS) $^ -o $@

quicksort_par.o: quicksort_par.c $(HDR_DEPS)
	$(CC) -c $(CFLAGS) $<

quicksort_seq.o: quicksort_seq.c $(HDR_DEPS)
	$(CC) -c $(CFLAGS) $<

walltime.o: $(SRC_DEPS) $(HDR_DEPS)
	$(CC) -c $(CFLAGS) $<

.PHONY: clean
clean:
	$(RM) *.o quicksort quicksort_par