#include <iostream>
#include <mpi.h>
#include <omp.h>

int main(int argc, char** argv) {
    int provided;
    MPI_Init_thread(&argc, &argv, MPI_THREAD_MULTIPLE, &provided);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    std::string level;
    switch(provided) {
        case MPI_THREAD_SINGLE:   level = "MPI_THREAD_SINGLE"; break;
        case MPI_THREAD_FUNNELED: level = "MPI_THREAD_FUNNELED"; break;
        case MPI_THREAD_SERIALIZED: level = "MPI_THREAD_SERIALIZED"; break;
        case MPI_THREAD_MULTIPLE: level = "MPI_THREAD_MULTIPLE"; break;
        default: level = "UNKNOWN";
    }
    
    std::cout << "Процесс " << rank << ": уровень поддержки = " << level << std::endl;
    
    #pragma omp parallel
    {
        int thread_num = omp_get_thread_num();
        int is_main;
        MPI_Is_thread_main(&is_main);
        
        #pragma omp critical
        std::cout << "  Процесс " << rank << ", поток " << thread_num 
                  << (is_main ? " (главный)" : " (не главный)") << std::endl;
    }
    
    MPI_Finalize();
    return 0;
}
