CC     = gcc
#CPATH = /opt/homebrew/Cellar/libpng/1.6.43/include
#LIBRARY_PATH = /opt/homebrew/Cellar/libpng/1.6.43/lib 
CFLAGS  = -O3 -fopenmp -I$(CPATH)
LDFLAGS = -O3 -fopenmp -L$(LIBRARY_PATH) -lpng

all: mandel_seq mandel_par_crit

mandel_par_crit: mandel_par_crit.o pngwriter.o walltime.o
	$(CC) $(LDFLAGS) $^ -o $@

mandel_seq: mandel_seq.o pngwriter.o walltime.o
	$(CC) $(LDFLAGS) $^ -o $@
	
mandel_par_crit.o: mandel_par_crit.c consts.h pngwriter.h walltime.h
	$(CC) -c $(CFLAGS) $<

mandel_seq.o: mandel_seq.c consts.h pngwriter.h walltime.h
	$(CC) -c $(CFLAGS) $<

pngwriter.o: pngwriter.c pngwriter.h
	$(CC) -c $(CFLAGS) $<

walltime.o: walltime.c walltime.h
	$(CC) -c $(CFLAGS) $<

.PHONY: clean clean-o
clean:
	$(RM) *.o mandel_seq mandel_par_crit *.png
	
clean-o: 
	$(RM) *.o mandel_seq mandel_par_crit
