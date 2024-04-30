/*******************************************************************************
* MPI-IO demo: Given a number of grid points in x and y direction, it creates
*              a domain distribution over the MPI processes, allocates and
*              initializes (to the rank) the local portion of the grid on each
*              process, and writes the grid in a single file using MPI-IO.
*******************************************************************************/
#include <mpi.h> // MPI
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Structs to hold domain decomposition
typedef struct {
  int nx, ny; // global grid points in x and y dimension of domain
} Domain;
typedef struct {
  // local grid points in x and y dimension of sub-domain
  int nx, ny;
  // MPI info
  int size, rank;
  // MPI Cartesian topology
  MPI_Comm comm_cart;
  // the i and j bounding box of this sub-domain
  int startx, starty;
  int endx, endy;
} SubDomain;

// Read command line arguments
void readcmdline(Domain* domain, int argc, char* argv[]) {
  if (argc < 3) {
    printf("Usage: main nx ny\n");
    printf("  nx, ny number of grid points in x-direction and "
                    "y-direction, respectively\n");
    exit(1);
  }

  // Read nx
  domain->nx = atoi(argv[1]);
  if (domain->nx < 1) {
    fprintf(stderr, "nx must be positive integer\n");
    exit(-1);
  }

  // Read ny
  domain->ny = atoi(argv[2]);
  if (domain->ny < 1) {
    fprintf(stderr, "ny must be positive integer\n");
    exit(-1);
  }
}

// Domain decomposition
void decomp1d(int n, int size, int rank, int* s, int* e) {
  int n_local = n / size;
  int deficit = n % size;
  *s = rank * n_local;
  *s = *s + ((rank < deficit) ? rank : deficit);
  if (rank < deficit) ++n_local;
  *e = *s + n_local - 1;
  if (*e > n || rank == size - 1) *e = n - 1;
}
void domain_decomposition(Domain const* domain, int size, int rank,
                          SubDomain* subdomain) {
  // Set size and rank
  subdomain->size = size;
  subdomain->rank = rank;
  // Determine the number of sub-domains in the x and y dimensions
  int dims[2] = {0, 0};
  MPI_Dims_create(size, 2, dims);
  // Create a 2D non-periodic Cartesian topology
  int periods[2] = {0, 0};
  MPI_Cart_create(MPI_COMM_WORLD, 2, dims, periods, 0, &subdomain->comm_cart);
  // Retrieve coordinates of the rank in the topology
  int coords[2];
  MPI_Cart_coords(subdomain->comm_cart, rank, 2, coords);
  // Decompose domain into sub-domains according Cartesian topology
  decomp1d(domain->nx, dims[0], coords[0], &subdomain->startx,
           &subdomain->endx);
  subdomain->nx = subdomain->endx - subdomain->startx + 1;
  decomp1d(domain->ny, dims[1], coords[1], &subdomain->starty,
           &subdomain->endy);
  subdomain->ny = subdomain->endy - subdomain->starty + 1;
  // Print
  printf("[Process %2d (%2d, %2d)] global dims: %d x %d; "
                                  "local dims: %d x %d (%d:%d, %d:%d);\n",
         rank, coords[0], coords[1],
         domain->nx, domain->ny,
         subdomain->nx, subdomain->ny,
         subdomain->startx, subdomain->endx,
         subdomain->starty, subdomain->endy);
}

// Output using MPI-IO
void output(char fname[], Domain const* domain, SubDomain const* subdomain,
            double* data) {
  // Generate *.bin file name
  char* fname_bin = (char*) malloc((strlen(fname) + 1 + 4)*sizeof(char));
  strcpy(fname_bin, fname);
  strcat(fname_bin, ".bin");

  // Open file
  MPI_File filehandle;
  MPI_File_open(MPI_COMM_WORLD, fname_bin, MPI_MODE_CREATE | MPI_MODE_WRONLY,
                MPI_INFO_NULL, &filehandle);

  // Create sub-array type (each process writes its sub-domain part into the
  // file containing (full!) domain)
  // Note the row-major order storage format (C order)
  int sizes[2]    = {domain->nx, domain->ny};
  int subsizes[2] = {subdomain->nx, subdomain->ny};
  int start[2]    = {subdomain->startx, subdomain->starty};
  MPI_Datatype filetype;
  MPI_Type_create_subarray(2, sizes, subsizes, start, MPI_ORDER_C, MPI_DOUBLE,
                           &filetype);
  MPI_Type_commit(&filetype);

  // Set view and write file
  MPI_Offset disp = 0;
  MPI_File_set_view(filehandle, disp, MPI_DOUBLE, filetype, "native",
                    MPI_INFO_NULL);
  MPI_File_write_all(filehandle, data, subdomain->nx*subdomain->ny, MPI_DOUBLE,
                     MPI_STATUS_IGNORE);

  // Free file type
  MPI_Type_free(&filetype);

  // Close file
  MPI_File_close(&filehandle);

  // Write BOV header file
  // (see format details here https://visit-sphinx-github-user-manual.readthedocs.io/en/develop/data_into_visit/BOVFormat.html#the-bov-file-format)
  if ( subdomain->rank == 0 ) {
    // Generate *.bov file name
    char* fname_bov = (char*) malloc((strlen(fname) + 1 + 4)*sizeof(char));
    strcpy(fname_bov, fname);
    strcat(fname_bov, ".bov");
    // Write BOV header file
    FILE* fp = fopen(fname_bov, "w+");
    free(fname_bov);
    fprintf(fp, "TIME: %f\n", 0.);
    fprintf(fp, "DATA_FILE: %s\n", fname_bin);
    fprintf(fp, "DATA_SIZE: %d %d %d\n", domain->nx, domain->ny, 1);
    fprintf(fp, "DATA_FORMAT: DOUBLE\n");
    fprintf(fp, "DATA_ENDIAN: LITTLE\n");
    fprintf(fp, "VARIABLE: data\n");
    fprintf(fp, "CENTERING: nodal\n");
    fprintf(fp, "BRICK_ORIGIN: %f %f %f\n", 0., 0., 0.);
    fprintf(fp, "BRICK_SIZE: %f %f %f\n", (double)domain->nx - 1.,
            (double)domain->ny - 1., 1.);
    fclose(fp);
  }

  // Free
  free(fname_bin);
}

// main
int main(int argc, char* argv[]) {
  // Read command line arguments
  Domain domain;
  readcmdline(&domain, argc, argv);

  // Initialize MPI and get info
  int size, rank;
  MPI_Init(&argc, &argv);
  MPI_Comm_size(MPI_COMM_WORLD, &size);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);

  // Domain decomposition
  SubDomain subdomain;
  domain_decomposition(&domain, size, rank, &subdomain);

  // Allocate and initialize (to this process' rank) array holding local
  // (to this process) portion of the grid
  // Note the row-major order storage format (C order)
  double* data = (double*) calloc(subdomain.nx*subdomain.ny, sizeof(double));
  for (int i = 0; i < subdomain.nx; i++) {
    for (int j = 0; j < subdomain.ny; j++) {
      data[i*subdomain.ny + j] = rank;
    }
  }

  // Output data using MPI-IO
  output("output", &domain, &subdomain, data);

  // Free
  free(data);

  // Free MPI Cart communicator
  if (subdomain.comm_cart!=NULL) MPI_Comm_free(&subdomain.comm_cart);

  // Finalize MPI
  MPI_Finalize();

  return 0;
}
