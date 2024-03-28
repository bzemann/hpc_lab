cmake_minimum_required(VERSION 3.10)
project(mini_app)

# Set the C++ standard you want to use (change this if you wish)
set(CMAKE_CXX_STANDARD 17)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(OpenMP_C_LIB_NAMES "omp")
set(OpenMP_CXX_LIB_NAMES "omp")
set(OpenMP_C_FLAGS "-Xpreprocessor -fopenmp -I/opt/homebrew/Cellar/libomp/18.1.1/include")
set(OpenMP_CXX_FLAGS "-Xpreprocessor -fopenmp -I/opt/homebrew/Cellar/libomp/18.1.1/include")
set(OpenMP_omp_LIBRARY "/opt/homebrew/Cellar/libomp/18.1.1/lib/libomp.dylib")

# Find OpenMP
find_package(OpenMP)

if(OPENMP_FOUND)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
endif()

# Set the optimization level to O3
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3")

# Add all the source files in the current directory to the project
file(GLOB SOURCES "*.cpp")

add_executable(mini_app ${SOURCES})

if(OpenMP_CXX_FOUND)
    target_link_libraries(mini_app PUBLIC OpenMP::OpenMP_CXX)
endif()