CC     ?= gcc
CFLAGS  = -fopenmp

hello_omp: hello_omp.c
	$(CC) $(CFLAGS) $^ -o $@

.PHONY: clean
clean:
	$(RM) hello_omp
