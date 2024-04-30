from mpi4py import MPI

# get comm, size, rank & host name
comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
proc = MPI.Get_processor_name()

# hello world!
print(f"Hello world from processor {proc}, rank {rank} out of {size} "
      f"processes")
