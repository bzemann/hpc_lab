cmake_minimum_required(VERSION 3.10)
project(mini_app)

# Set the C++ standard you want to use (change this if you wish)
set(CMAKE_CXX_STANDARD 17)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Specify the compiler
set(CMAKE_CXX_COMPILER "g++-13")

# Set the optimization level to O3 and enable OpenMP
set(CMAKE_CXX_FLAGS "-O3 -fopenmp")

# Add the libomp paths
link_directories("/opt/homebrew/opt/libomp/lib")
include_directories("/opt/homebrew/opt/libomp/include")

# Add all the source files to the project
set(SOURCES walltime.cpp stats.cpp data.cpp operators.cpp linalg.cpp main.cpp)

# Create the executable
add_executable(main ${SOURCES})