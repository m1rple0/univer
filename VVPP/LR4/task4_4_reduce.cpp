#include <iostream>
#include <mpi.h>

using namespace std;

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    const int N = 1000;
    int* data = new int[N];
    
    for (int i = 0; i < N; i++) {
        data[i] = (rank + 1) * (i % 10);
    }
    
    int localMax = data[0];
    for (int i = 1; i < N; i++) {
        if (data[i] > localMax) localMax = data[i];
    }
    
    int globalMax;
    MPI_Reduce(&localMax, &globalMax, 1, MPI_INT, MPI_MAX, 0, MPI_COMM_WORLD);
    
    if (rank == 0) {
        cout << "=== MPI_Reduce (MAX) ===" << endl;
        cout << "Глобальный максимум: " << globalMax << endl;
    }
    
    int localSum = 0;
    for (int i = 0; i < N; i++) localSum += data[i];
    
    int globalSum;
    MPI_Allreduce(&localSum, &globalSum, 1, MPI_INT, MPI_SUM, MPI_COMM_WORLD);
    
    if (rank == 0) {
        cout << "\n=== MPI_Allreduce (SUM) ===" << endl;
    }
    cout << "Процесс " << rank << ": глобальная сумма = " << globalSum << endl;
    
    int* sendbuf = new int[size];
    int* recvbuf = new int[1];
    int* recvcounts = new int[size];
    
    for (int i = 0; i < size; i++) {
        sendbuf[i] = rank * 10 + i;
        recvcounts[i] = 1;
    }
    
    MPI_Reduce_scatter(sendbuf, recvbuf, recvcounts, MPI_INT, MPI_SUM, MPI_COMM_WORLD);
    
    if (rank == 0) {
        cout << "\n=== MPI_Reduce_scatter ===" << endl;
    }
    cout << "Процесс " << rank << " получил сумму: " << recvbuf[0] << endl;
    
    delete[] data;
    delete[] sendbuf;
    delete[] recvbuf;
    delete[] recvcounts;
    
    MPI_Finalize();
    return 0;
}
