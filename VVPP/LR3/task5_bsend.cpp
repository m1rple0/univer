#include <iostream>
#include <mpi.h>
#include <cstdlib>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    if (size < 2) {
        if (rank == 0)
            std::cout << "Запустите с 2+ процессами" << std::endl;
        MPI_Finalize();
        return 1;
    }
    
    int buffer_size = 10000;
    char* buffer = (char*)malloc(buffer_size + MPI_BSEND_OVERHEAD);
    
    MPI_Buffer_attach(buffer, buffer_size + MPI_BSEND_OVERHEAD);
    
    double start_time = MPI_Wtime();
    
    if (rank == 0) {
        int data[1000];
        for (int i = 0; i < 1000; i++) data[i] = i;
        
        MPI_Bsend(data, 1000, MPI_INT, 1, 0, MPI_COMM_WORLD);
        std::cout << "Буферизованная отправка завершена" << std::endl;
        
    } else if (rank == 1) {
        int data[1000];
        MPI_Recv(data, 1000, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        std::cout << "Получено " << data[0] << "..." << data[999] << std::endl;
    }
    
    double end_time = MPI_Wtime();
    
    if (rank == 0) {
        std::cout << "Время: " << end_time - start_time << " сек" << std::endl;
    }
    
    MPI_Buffer_detach(&buffer, &buffer_size);
    free(buffer);
    
    MPI_Finalize();
    return 0;
}
