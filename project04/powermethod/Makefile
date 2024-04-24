CC      = mpicc
CFLAGS  = -O3 # Useful flags for debgging -Wall -g -fsanitize=address
LDFLAGS = -lm # -fsanitize=address

all: powermethod_rows

powermethod_rows: powermethod_rows.o walltime.o
	$(CC) $(LDFLAGS) $^ -o $@

powermethod_rows.o: powermethod_rows.c
	$(CC) -c $(CFLAGS) $<

walltime.o: walltime.c walltime.h
	$(CC) -c $(CFLAGS) $<

.PHONY: clean
clean:
	$(RM) *.o powermethod_rows
