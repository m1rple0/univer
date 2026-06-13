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
    
    char mode = 's';
    if (rank == 0) {
        std::cout << "Выберите режим: s (стандартный MPI_Send) или S (синхронный MPI_Ssend): ";
        std::cin >> mode;
        
        for (int i = 1; i < size; i++) {
            MPI_Send(&mode, 1, MPI_CHAR, i, 0, MPI_COMM_WORLD);
        }
    } else {
        MPI_Recv(&mode, 1, MPI_CHAR, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    }
    
    int data = 42;
    double start_time = MPI_Wtime();
    
    for (int i = 0; i < 1000; i++) {
        if (rank == 0) {
            if (mode == 's') {
                MPI_Send(&data, 1, MPI_INT, 1, 1, MPI_COMM_WORLD);
            } else {
                MPI_Ssend(&data, 1, MPI_INT, 1, 1, MPI_COMM_WORLD);
            }
        } else if (rank == 1) {
            MPI_Recv(&data, 1, MPI_INT, 0, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        }
    }
    
    double end_time = MPI_Wtime();
    
    if (rank == 0) {
        std::cout << "Режим: " << (mode == 's' ? "MPI_Send" : "MPI_Ssend") 
                  << ", время: " << end_time - start_time << " сек" << std::endl;
    }
    
    MPI_Finalize();
    return 0;
}
