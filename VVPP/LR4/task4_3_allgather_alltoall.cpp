#include <iostream>
#include <mpi.h>

using namespace std;

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    int myValue = rank * 10;
    int* allValues = new int[size];
    
    MPI_Allgather(&myValue, 1, MPI_INT, allValues, 1, MPI_INT, MPI_COMM_WORLD);
    
    if (rank == 0) {
        cout << "=== MPI_Allgather ===" << endl;
        cout << "Собраны значения: ";
        for (int i = 0; i < size; i++) cout << allValues[i] << " ";
        cout << endl;
    }
    
    MPI_Barrier(MPI_COMM_WORLD);
    
    int* sendbuf = new int[size];
    int* recvbuf = new int[size];
    
    for (int i = 0; i < size; i++) {
        sendbuf[i] = rank * 100 + i;
    }
    
    MPI_Alltoall(sendbuf, 1, MPI_INT, recvbuf, 1, MPI_INT, MPI_COMM_WORLD);
    
    if (rank == 0) {
        cout << "\n=== MPI_Alltoall ===" << endl;
    }
    
    cout << "Процесс " << rank << " получил: ";
    for (int i = 0; i < size; i++) cout << recvbuf[i] << " ";
    cout << endl;
    
    delete[] allValues;
    delete[] sendbuf;
    delete[] recvbuf;
    
    MPI_Finalize();
    return 0;
}
