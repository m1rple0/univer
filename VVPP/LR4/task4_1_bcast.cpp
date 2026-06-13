#include <iostream>
#include <mpi.h>

using namespace std;

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    int data;
    
    if (rank == 0) {
        data = 42;
        cout << "Процесс 0 рассылает значение: " << data << endl;
    }
    
    MPI_Bcast(&data, 1, MPI_INT, 0, MPI_COMM_WORLD);
    
    cout << "Процесс " << rank << " получил: " << data << endl;
    
    MPI_Finalize();
    return 0;
}
