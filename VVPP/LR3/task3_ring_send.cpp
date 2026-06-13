#include <iostream>
#include <mpi.h>

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
    
    int value;
    double start_time = 0, end_time = 0;
    
    if (rank == 0) {
        value = 100;
        start_time = MPI_Wtime();
        
        MPI_Send(&value, 1, MPI_INT, 1, 0, MPI_COMM_WORLD);
        MPI_Recv(&value, 1, MPI_INT, size - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        
        end_time = MPI_Wtime();
        std::cout << "Значение вернулось: " << value << std::endl;
        std::cout << "Время передачи по кругу: " << end_time - start_time << " сек" << std::endl;
        
    } else {
        MPI_Recv(&value, 1, MPI_INT, rank - 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        value += rank;
        MPI_Send(&value, 1, MPI_INT, (rank + 1) % size, 0, MPI_COMM_WORLD);
    }
    
    MPI_Finalize();
    return 0;
}
