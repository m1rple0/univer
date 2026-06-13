#include <iostream>
#include <mpi.h>
#include <cstring>

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
    
    if (rank == 0) {
        const char* messages[] = {"Короткое сообщение", "Очень длинное сообщение, которое занимает много места"};
        
        for (int i = 0; i < 2; i++) {
            int len = strlen(messages[i]) + 1;
            MPI_Send(messages[i], len, MPI_CHAR, 1, i, MPI_COMM_WORLD);
        }
        
    } else if (rank == 1) {
        MPI_Status status;
        
        for (int i = 0; i < 2; i++) {
            MPI_Probe(MPI_ANY_SOURCE, MPI_ANY_TAG, MPI_COMM_WORLD, &status);
            
            int count;
            MPI_Get_count(&status, MPI_CHAR, &count);
            
            char* buffer = new char[count];
            MPI_Recv(buffer, count, MPI_CHAR, status.MPI_SOURCE, status.MPI_TAG, 
                     MPI_COMM_WORLD, &status);
            
            std::cout << "Получено сообщение от процесса " << status.MPI_SOURCE
                      << " с тегом " << status.MPI_TAG
                      << ", размер " << count << " байт: " << buffer << std::endl;
            
            delete[] buffer;
        }
    }
    
    MPI_Finalize();
    return 0;
}
