from mandelbrot_task import *
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpi4py import MPI # MPI_Init and MPI_Finalize automatically called
import numpy as np
import sys
import time
from typing import List, Tuple, Dict

# some parameters
MANAGER = 0       # rank of manager
TAG_TASK      = 1 # task       message tag
TAG_TASK_DONE = 2 # tasks done message tag
TAG_DONE      = 3 # done       message tag

def manager(comm, tasks):
    """
    The manager.

    Parameters
    ----------
    comm : mpi4py.MPI communicator
        MPI communicator
    tasks : list of objects with a do_task() method perfroming the task
        List of tasks to accomplish

    Returns
    -------
    a list of completed tasks

    """
    size = comm.Get_size()
    n_tasks = len(tasks)
    n_finished_tasks = 0
    finished_tasks = []
    TasksDoneByWorker = np.zeros(size, dtype=int)

    print(len(tasks))

    for i in range(1,size):
        if tasks:
            comm.send(tasks.pop(), dest=i, tag=TAG_TASK)

    while n_finished_tasks < n_tasks:
        if comm.iprobe(source=MPI.ANY_SOURCE, tag=TAG_TASK_DONE):
            worker, finished_task = comm.recv(source=MPI.ANY_SOURCE, tag=TAG_TASK_DONE)
            finished_tasks.append(finished_task)
            TasksDoneByWorker[worker] += 1
            n_finished_tasks += 1
            if tasks:
                comm.send(tasks.pop(), dest=worker, tag=TAG_TASK)

    for i in range(1, size):
        comm.send(None, dest=i, tag=TAG_DONE)

    return finished_tasks, TasksDoneByWorker



def worker(comm):
    """
    The worker.

    Parameters
    ----------
    comm : mpi4py.MPI communicator
        MPI communicator
    """
    my_rank = comm.Get_rank()
    while True:
        if comm.iprobe(source=MANAGER, tag=TAG_DONE):
            comm.recv(source=MANAGER, tag=TAG_DONE)
            break
        elif comm.iprobe(source=MANAGER, tag=TAG_TASK):
            task = comm.recv(source=MANAGER, tag=TAG_TASK)
            task.do_work()
            comm.send([my_rank, task], dest=MANAGER, tag=TAG_TASK_DONE)
    


def readcmdline(rank):
    """
    Read command line arguments

    Parameters
    ----------
    rank : int
        Rank of calling MPI process

    Returns
    -------
    nx : int
        number of gridpoints in x-direction
    ny : int
        number of gridpoints in y-direction
    ntasks : int
        number of tasks
    """
    # report usage
    if len(sys.argv) != 4:
        if rank == MANAGER:
            print("Usage: manager_worker nx ny ntasks")
            print("  nx     number of gridpoints in x-direction")
            print("  ny     number of gridpoints in y-direction")
            print("  ntasks number of tasks")
        sys.exit()

    # read nx, ny, ntasks
    nx = int(sys.argv[1])
    if nx < 1:
        sys.exit("nx must be a positive integer")
    ny = int(sys.argv[2])
    if ny < 1:
        sys.exit("ny must be a positive integer")
    ntasks = int(sys.argv[3])
    if ntasks < 1:
        sys.exit("ntasks must be a positive integer")

    return nx, ny, ntasks


if __name__ == "__main__":

    # get COMMON WORLD communicator, size & rank
    comm    = MPI.COMM_WORLD
    size    = comm.Get_size()
    my_rank = comm.Get_rank()

    # report on MPI environment
    if my_rank == MANAGER:
        print(f"MPI initialized with {size:5d} processes")

    # read command line arguments
    nx, ny, ntasks = readcmdline(my_rank)

    # start timer
    timespent = - time.perf_counter()

    # trying out ... YOUR MANAGER-WORKER IMPLEMENTATION HERE ...
    x_min = -2.
    x_max  = +1.
    y_min  = -1.5
    y_max  = +1.5
    M = mandelbrot(x_min, x_max, nx, y_min, y_max, ny, ntasks)
    tasks = M.get_tasks()
    if my_rank == MANAGER:
        tasks, TasksDoneByWorker = manager(comm, tasks)
        m = M.combine_tasks(tasks)
        
        plt.imshow(m.T, cmap="gray", extent=[x_min, x_max, y_min, y_max])
        plt.savefig("mandelbrot.png")
    else:
        worker(comm)

    # stop timer
    timespent += time.perf_counter()

    # inform that done
    if my_rank == MANAGER:
        print(f"Run took {timespent:f} seconds")
        for i in range(size):
            if i == MANAGER:
                continue
            print(f"Process {i:5d} has done {TasksDoneByWorker[i]:10d} tasks")
        print("Done.")
