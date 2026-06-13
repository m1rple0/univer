#include <iostream>
#include <mpi.h>
#include <unistd.h>

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
    
    int data = 42;
    MPI_Request request;
    MPI_Status status;
    
    if (rank == 0) {
        std::cout << "Процесс 0: запускаем неблокирующую отправку" << std::endl;
        MPI_Isend(&data, 1, MPI_INT, 1, 0, MPI_COMM_WORLD, &request);
        
        std::cout << "Процесс 0: делаем другую работу..." << std::endl;
        sleep(1);
        
        MPI_Wait(&request, &status);
        std::cout << "Процесс 0: отправка завершена" << std::endl;
        
    } else if (rank == 1) {
        sleep(0.5);
        
        MPI_Irecv(&data, 1, MPI_INT, 0, 0, MPI_COMM_WORLD, &request);
        
        int flag = 0;
        while (!flag) {
            MPI_Test(&request, &flag, &status);
            if (!flag) {
                std::cout << "Процесс 1: ждём данные..." << std::endl;
                sleep(1);
            }
        }
        
        std::cout << "Процесс 1: получено значение " << data << std::endl;
    }
    
    MPI_Finalize();
    return 0;
}
