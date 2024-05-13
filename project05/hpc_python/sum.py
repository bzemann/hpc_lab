from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()

# sum with allreduce
sum_ = np.array(rank)
result = comm.allreduce(sum_)
print(f"Sum of ranks with allreduce on processor {rank} is {result}")

comm.Barrier()
