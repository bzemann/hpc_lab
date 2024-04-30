#ifndef DATA_H
#define DATA_H
#include <cassert>

namespace data {
// define some helper types that can be used to pass simulation
// data around without haveing to pass individual parameters
// global domain (i.e., full domain size)
struct Discretization {
    int nx;       // grid points in x and y dimension
    int nt;       // number of time steps
    int N;        // total number of grid points
    double dt;    // time step size
    double dx;    // distance between grid points
    double alpha; // dx^2/(D*dt)
    double beta;  // R*dx^2/D
};

// local domain (i.e., sub-domain of each process)
struct SubDomain {
    // initialize a sub-domain
    void init(int, int, Discretization&);

    // print sub-domain information
    void print();

    // i and j dimensions of the global decomposition
    int ndomx;
    int ndomy;

    // the i and j index of this sub-domain
    int domx;
    int domy;

    // the i and j bounding box of this sub-domain
    int startx;
    int starty;
    int endx;
    int endy;

    // the rank of neighbouring domains
    int neighbour_north;
    int neighbour_east;
    int neighbour_south;
    int neighbour_west;

    // mpi info
    int size;
    int rank;
    // MPI_Comm comm_cart; // TODO: Save Cartesian topology communicator here
                           //       and don't forget to free it

    // grid points in x and y dimension of this sub-domain
    int nx;
    int ny;

    // total number of grid points of this sub-domain
    int N;
};

// thin wrapper around a pointer that can be accessed as either a 2D or 1D array
// Field has dimension xdim * ydim in 2D, or length=xdim*ydim in 1D
class Field {
    public:
    // default constructor
    Field() : ptr_(0), xdim_(0), ydim_(0) { }
    // constructor
    Field(int xdim, int ydim) : xdim_(xdim), ydim_(ydim) {
        #ifdef DEBUG
        assert(xdim>0 && ydim>0);
        #endif
        ptr_ = new double[xdim*ydim];
        // initialize
        fill(0.);
    }

    // destructor
    ~Field() { free(); }

    void init(int xdim, int ydim) {
        #ifdef DEBUG
        assert(xdim>0 && ydim>0);
        #endif
        free();
        ptr_ = new double[xdim*ydim];
        #ifdef DEBUG
        assert(xdim>0 && ydim>0);
        #endif
        xdim_ = xdim;
        ydim_ = ydim;
        // initialize
        fill(0.);
    }

    double*       data()       { return ptr_; }
    const double* data() const { return ptr_; }

    // access via (i,j) pair
    inline double&       operator() (int i, int j)        {
        #ifdef DEBUG
        assert(i>=0 && i<xdim_ && j>=0 && j<ydim_);
        #endif
        return ptr_[i+j*xdim_];
    }
    inline double const& operator() (int i, int j) const  {
        #ifdef DEBUG
        assert(i>=0 && i<xdim_ && j>=0 && j<ydim_);
        #endif
        return ptr_[i+j*xdim_];
    }

    // access as a 1D field
    inline double      & operator[] (int i) {
        #ifdef DEBUG
        assert(i>=0 && i<xdim_*ydim_);
        #endif
        return ptr_[i];
    }
    inline double const& operator[] (int i) const {
        #ifdef DEBUG
        assert(i>=0 && i<xdim_*ydim_);
        #endif
        return ptr_[i];
    }

    int xdim()   const { return xdim_; }
    int ydim()   const { return ydim_; }
    int length() const { return xdim_*ydim_; }

    private:

    // set to a constant value
    void fill(double val) {
        for (int i=0; i<xdim_*ydim_; ++i) {
            ptr_[i] = val;
        }
    }

    void free() {
        if (ptr_) delete[] ptr_;
        ptr_ = 0;
    }

    double* ptr_;
    int xdim_;
    int ydim_;
};

// fields that hold the solution
extern Field y_new, y_old; // 2d

// fields that hold the boundary values
extern Field bndN, bndE, bndS, bndW; // 1d

// buffers used in boundary exchange
extern Field buffN, buffE, buffS, buffW;

extern Discretization options;
extern SubDomain      domain;

}

#endif /* DATA_H */
