#include "data.h"
#include "mpi.h"

#include <iostream>
#include <cmath>



namespace data {

// fields that hold the solution
Field y_new;
Field y_old;

// fields that hold the boundary points
Field bndN;
Field bndE;
Field bndS;
Field bndW;

// buffers used during boundary halo communication
Field buffN;
Field buffE;
Field buffS;
Field buffW;

// global domain and local sub-domain
Discretization options;
SubDomain      domain;

void SubDomain::init(int mpi_rank, int mpi_size,
                     Discretization& discretization) {
    //determine the number of sub-domains in the x and y dimensions
    //       using MPI_Dims_create
    int dims[2] = {discretization.nx, discretization.nx};
    MPI_Dims_create(mpi_size, 2, dims);
    ndomy = dims[0];
    ndomx = dims[1];


    //create a 2D non-periodic Cartesian topology using MPI_Cart_create
    int periods[2] = {0, 0};
    MPI_Cart_create(MPI_COMM_WORLD, 2, dims, periods, 0, &(this->comm_cart));

    //retrieve coordinates of the rank in the topology using
    int coords[2] = {0, 0};
    MPI_Cart_coords(this->comm_cart, mpi_rank, 2, coords);
    domy = coords[0] + 1;
    domx = coords[1] + 1;

    // TODO: set neighbours for all directions using MPI_Cart_shift
    MPI_Cart_shift(this->comm_cart, 0, -1, &(this->neighbour_north), &(this->neighbour_south));

    // get bounding box
    nx = discretization.nx / ndomx;
    ny = discretization.nx / ndomy;
    startx = (domx-1)*nx+1;
    starty = (domy-1)*ny+1;

    nx = domx == ndomx ? discretization.nx - startx + 1: nx;
    ny = domy == ndomy ? discretization.nx - starty + 1: ny;
    
    endx = startx + nx -1;
    endy = starty + ny -1;

    // get total number of grid points in this sub-domain
    N = nx*ny;

    rank = mpi_rank;
    size = mpi_size;
}

// print domain decomposition information to stdout
void SubDomain::print() {
    for (int irank = 0; irank < size; irank++) {
        if (irank == rank) {
            std::cout << "rank " << rank << " / " << size
                      << " : (" << domx << ", " << domy << ")"
                      << " neigh N:S " << neighbour_north
                      << ":"           << neighbour_south
                      << " neigh E:W " << neighbour_east
                      << ":"           << neighbour_west
                      << " local dims " << nx << " x " << ny
                      << std::endl;
        }
        MPI_Barrier(MPI_COMM_WORLD);
    }
}

}
