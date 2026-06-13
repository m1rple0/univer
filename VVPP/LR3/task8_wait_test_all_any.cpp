#include <iostream>
#include <mpi.h>

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    if (size < 3) {
        if (rank == 0) {
            std::cout << "Запустите с 3+ процессами" << std::endl;
        }
        MPI_Finalize();
        return 1;
    }
    
    const int num_ops = 2;
    MPI_Request requests[num_ops];
    int data[num_ops];
    
    if (rank == 0) {
        std::cout << "Демонстрация MPI_Waitall" << std::endl;
        
        for (int i = 0; i < num_ops; i++) {
            data[i] = (i + 1) * 100;
            MPI_Isend(&data[i], 1, MPI_INT, i + 1, 0, MPI_COMM_WORLD, &requests[i]);
        }
        
        MPI_Waitall(num_ops, requests, MPI_STATUSES_IGNORE);
        std::cout << "Все отправки завершены" << std::endl;
        
    } else if (rank == 1) {
        int val;
        MPI_Recv(&val, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        std::cout << "Процесс 1: получено " << val << std::endl;
        
    } else if (rank == 2) {
        int val;
        MPI_Recv(&val, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        std::cout << "Процесс 2: получено " << val << std::endl;
    }
    
    MPI_Barrier(MPI_COMM_WORLD);
    
    if (rank == 0) {
        std::cout << "\nДемонстрация MPI_Waitany" << std::endl;
        
        for (int i = 0; i < num_ops; i++) {
            data[i] = (i + 1) * 200;
            MPI_Isend(&data[i], 1, MPI_INT, i + 1, 1, MPI_COMM_WORLD, &requests[i]);
        }
        
        int completed = 0;
        while (completed < num_ops) {
            int index;
            MPI_Waitany(num_ops, requests, &index, MPI_STATUS_IGNORE);
            std::cout << "Завершена отправка процессу " << (index + 1) << std::endl;
            completed++;
        }
    }
    
    if (rank == 1 || rank == 2) {
        int val;
        MPI_Recv(&val, 1, MPI_INT, 0, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
        std::cout << "Процесс " << rank << ": получено " << val << std::endl;
    }
    
    MPI_Barrier(MPI_COMM_WORLD);
    
    if (rank == 0) {
        std::cout << "\nДемонстрация MPI_Testany" << std::endl;
        
        for (int i = 0; i < num_ops; i++) {
            data[i] = (i + 1) * 300;
            MPI_Isend(&data[i], 1, MPI_INT, i + 1, 2, MPI_COMM_WORLD, &requests[i]);
        }
        
        int completed = 0;
        int attempts = 0;
        while (completed < num_ops) {
            int index, flag;
            MPI_Testany(num_ops, requests, &index, &flag, MPI_STATUS_IGNORE);
            attempts++;
            if (flag) {
                std::cout << "Завершена отправка процессу " << (index + 1) 
                          << " (попытка " << attempts << ")" << std::endl;
                completed++;
            }
        }
        std::cout << "Всего попыток: " << attempts << std::endl;
    }
    
    if (rank == 1 || rank == 2) {
        int val;
        MPI_Recv(&val, 1, MPI_INT, 0, 2, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    }
    
    MPI_Finalize();
    return 0;
}
