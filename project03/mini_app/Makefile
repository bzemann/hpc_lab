CXX     = g++
CXXFLAGS = -O3 -fopenmp
CXXFLAGS_NO_OMP = -O3

SOURCES = walltime.cpp stats.cpp data.cpp operators.cpp linalg.cpp main.cpp
HEADERS = walltime.h   stats.h   data.h   operators.h   linalg.h

OBJ     = $(patsubst %.cpp,%.o,$(SOURCES))
OBJ_NO_OMP = $(patsubst %.cpp,%_no_omp.o,$(SOURCES))

all: main main_seq

%.o: %.cpp $(HEADERS)
	$(CXX) $(CXXFLAGS) -c $< -o $@

%_no_omp.o: %.cpp $(HEADERS)
	$(CXX) $(CXXFLAGS_NO_OMP) -c $< -o $@

main: $(OBJ)
	$(CXX) $(CXXFLAGS) $(OBJ) -o $@

main_seq: $(OBJ_NO_OMP)
	$(CXX) $(CXXFLAGS_NO_OMP) $(OBJ_NO_OMP) -o $@

.PHONY: clean
clean:
	rm -f $(OBJ) $(OBJ_NO_OMP) main main_seq *.bin *.bov