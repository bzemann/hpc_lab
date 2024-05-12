//******************************************
// operators.cpp
// based on min-app code written by Oliver Fuhrer, MeteoSwiss
// modified by Ben Cumming, CSCS
// *****************************************

// Description: Contains simple operators which can be used on 2/3d-meshes

#include "data.h"
#include "mpi.h"
#include "operators.h"
#include "stats.h"
#include <iostream>

namespace operators {

// compute the diffusion-reaction stencils
// s_old is the population concentration at time step k-1, s_new at k,
// and f is the residual (see Eq. (7) in Project 3).
void diffusion(data::Field const& s_old, data::Field const& s_new,
               data::Field& f) {
    using data::options;
    using data::domain;

    using data::bndE;
    using data::bndW;
    using data::bndN;
    using data::bndS;

    using data::buffE;
    using data::buffW;
    using data::buffN;
    using data::buffS;

    double alpha = options.alpha;
    double beta = options.beta;

    int nx = domain.nx;
    int ny = domain.ny;
    int iend  = nx - 1;
    int jend  = ny - 1;

    // exchange the ghost cells using non-blocking point-to-point
    //       communication
    int rank;
    MPI_Comm_rank(domain.comm_cart, &rank);
    MPI_Request request_north_send, request_south_send, request_east_send, request_west_send;
    int error = 0; 

    for(int i = 0; i < nx; i++){
            buffN[i] = s_new(i, ny - 1);
    }

    //Send north row to north neighbour
    MPI_Isend(buffN.data(), nx, MPI_DOUBLE, domain.neighbour_north, 0, domain.comm_cart, &request_north_send);
    //Receive south row from south neighbour
    MPI_Recv(bndS.data(), nx, MPI_DOUBLE, domain.neighbour_south, 0, domain.comm_cart, MPI_STATUS_IGNORE);

    for(int i = 0; i < nx; i++){
            buffS[i] = s_new(i, 0);
    }

    //Send south row to south neighbour
    MPI_Isend(buffS.data(), nx, MPI_DOUBLE, domain.neighbour_south, 0, domain.comm_cart, &request_south_send);
    //Receive north row from north neighbour
    MPI_Recv(bndN.data(), nx, MPI_DOUBLE, domain.neighbour_north, 0, domain.comm_cart, MPI_STATUS_IGNORE);

    for(int j = 0; j < nx; j++){
            buffE[j] = s_new(nx - 1, j);
    }

    //Send East column to east neighbour
    MPI_Isend(buffE.data(), nx, MPI_DOUBLE, domain.neighbour_east, 0, domain.comm_cart, &request_east_send);
    //Receive west column from west neighbour
    MPI_Recv(bndW.data(), nx, MPI_DOUBLE, domain.neighbour_west, 0, domain.comm_cart, MPI_STATUS_IGNORE);

    for(int j = 0; j < nx; j++){
            buffW[j] = s_new(0, j);
    }

    //Send west column to west neighbour
    MPI_Isend(buffW.data(), nx, MPI_DOUBLE, domain.neighbour_west, 0, domain.comm_cart, &request_west_send);
    //Receive east column from east neighbour
    MPI_Recv(bndE.data(), nx, MPI_DOUBLE, domain.neighbour_east, 0, domain.comm_cart, MPI_STATUS_IGNORE);

    // the interior grid points
    for (int j=1; j < jend; j++) {
        for (int i=1; i < iend; i++) {
            f(i,j) = -(4. + alpha) * s_new(i,j)     // central point
                   + s_new(i-1,j) + s_new(i+1,j)    // east and west
                   + s_new(i,j-1) + s_new(i,j+1)    // north and south
                   + alpha * s_old(i,j)
                   + beta * s_new(i,j) * (1.0 - s_new(i,j));
        }
    }

    error = MPI_Wait(&request_east_send, MPI_STATUS_IGNORE);
    if(error != 0){
        std::cout << "Error in MPI communication\n";
        MPI_Abort(MPI_COMM_WORLD, 1);        
    }

    error = MPI_Wait(&request_west_send, MPI_STATUS_IGNORE);
    if(error != 0){
        std::cout << "Error in MPI communication\n";
        MPI_Abort(MPI_COMM_WORLD, 1);        
    }

    // east boundary
    {
        int i = nx - 1;
        for (int j = 1; j < jend; j++) {
            f(i,j) = -(4. + alpha) * s_new(i,j)
                   + s_new(i-1,j) + bndE[j]
                   + s_new(i,j-1) + s_new(i,j+1)
                   + alpha * s_old(i,j)
                   + beta * s_new(i,j) * (1.0 - s_new(i,j));
        }
    }

    // west boundary
    {
        int i = 0;
        for (int j = 1; j < jend; j++) {
            f(i,j) = -(4. + alpha) * s_new(i,j)
                   + bndW[j]      + s_new(i+1,j)
                   + s_new(i,j-1) + s_new(i,j+1)
                   + alpha * s_old(i,j)
                   + beta * s_new(i,j) * (1.0 - s_new(i,j));
        }
    }

    error = MPI_Wait(&request_north_send, MPI_STATUS_IGNORE);
    if(error != 0){
        std::cout << "Error in MPI communication\n";
        MPI_Abort(MPI_COMM_WORLD, 1);        
    }

    error = MPI_Wait(&request_south_send, MPI_STATUS_IGNORE);
    if(error != 0){
        std::cout << "Error in MPI communication\n";
        MPI_Abort(MPI_COMM_WORLD, 1);        
    }

    // north boundary (plus NE and NW corners)
    {
        int j = ny - 1;

        {
            int i = 0; // NW corner
            f(i,j) = -(4. + alpha) * s_new(i,j)
                   + bndW[j]      + s_new(i+1,j)
                   + s_new(i,j-1) + bndN[i]
                   + alpha * s_old(i,j)
                   + beta * s_new(i,j) * (1.0 - s_new(i,j));
        }

        // north boundary
        for (int i = 1; i < iend; i++) {
            f(i,j) = -(4. + alpha) * s_new(i,j)
                   + s_new(i-1,j) + s_new(i+1,j)
                   + s_new(i,j-1) + bndN[i]
                   + alpha * s_old(i,j)
                   + beta * s_new(i,j) * (1.0 - s_new(i,j));
        }

        {
            int i = nx - 1; // NE corner
            f(i,j) = -(4. + alpha) * s_new(i,j)
                   + s_new(i-1,j) + bndE[j]
                   + s_new(i,j-1) + bndN[i]
                   + alpha * s_old(i,j)
                   + beta * s_new(i,j) * (1.0 - s_new(i,j));
        }
    }

    // south boundary (plus SW and SE corners)
    {
        int j = 0;
        {
            int i = 0; // SW corner
            f(i,j) = -(4. + alpha) * s_new(i,j)
                   + bndW[j] + s_new(i+1,j)
                   + bndS[i] + s_new(i,j+1)
                   + alpha * s_old(i,j)
                   + beta * s_new(i,j) * (1.0 - s_new(i,j));
        }

        // south boundary
        for (int i = 1; i < iend; i++) {
            f(i,j) = -(4. + alpha) * s_new(i,j)
                   + s_new(i-1,j) + s_new(i+1,j)
                   + bndS[i]      + s_new(i,j+1)
                   + alpha * s_old(i,j)
                   + beta * s_new(i,j) * (1.0 - s_new(i,j));
        }

        {
            int i = nx - 1; // SE corner
            f(i,j) = -(4. + alpha) * s_new(i,j)
                   + s_new(i-1,j) + bndE[j]
                   + bndS[i]      + s_new(i,j+1)
                   + alpha * s_old(i,j)
                   + beta * s_new(i,j) * (1.0 - s_new(i,j));
        }
    }

    // Accumulate the flop counts
    // 8 ops total per point
    stats::flops_diff += 12 * (nx - 2) * (ny - 2) // interior points
                      +  11 * (nx - 2  +  ny - 2) // NESW boundary points
                      +  11 * 4;                  // corner points
}

}
