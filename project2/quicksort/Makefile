CC     = gcc-13
CFLAGS = -O3 -fopenmp

all: quicksort

quicksort: quicksort.o walltime.o
	$(CC) $(CFLAGS) $^ -o $@

quicksort.o: quicksort.c walltime.h
	$(CC) -c $(CFLAGS) $<

walltime.o: walltime.c walltime.h
	$(CC) -c $(CFLAGS) $<

.PHONY: clean
clean:
	$(RM) *.o quicksort
