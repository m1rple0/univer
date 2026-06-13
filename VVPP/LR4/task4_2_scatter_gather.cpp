#include <iostream>
#include <mpi.h>

using namespace std;

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    const int N = 100;
    int* sendbuf = nullptr;
    int recvbuf[N/size];
    int* recv_all = nullptr;
    
    if (rank == 0) {
        sendbuf = new int[N];
        for (int i = 0; i < N; i++) {
            sendbuf[i] = i;
        }
        recv_all = new int[N];
        cout << "Исходный массив: ";
        for (int i = 0; i < N; i += 10) cout << sendbuf[i] << " ";
        cout << endl;
    }
    
    MPI_Scatter(sendbuf, N/size, MPI_INT, 
                recvbuf, N/size, MPI_INT, 
                0, MPI_COMM_WORLD);
    
    for (int i = 0; i < N/size; i++) {
        recvbuf[i] *= 2;
    }
    
    MPI_Gather(recvbuf, N/size, MPI_INT,
               recv_all, N/size, MPI_INT,
               0, MPI_COMM_WORLD);
    
    if (rank == 0) {
        cout << "Преобразованный массив: ";
        for (int i = 0; i < N; i += 10) cout << recv_all[i] << " ";
        cout << endl;
        delete[] sendbuf;
        delete[] recv_all;
    }
    
    MPI_Finalize();
    return 0;
}
