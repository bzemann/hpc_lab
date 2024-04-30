CXX      = mpicc
CXXFLAGS = -Wall

mpi_io: mpi_io.c
	$(CXX) -Wall $< -o $@

.PHONY: clean
clean:
	$(RM) mpi_io $(OBJ) output.*
