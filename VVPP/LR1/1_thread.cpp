#include <iostream>
#include <omp.h>

int main() {
    // Установка числа потоков
    omp_set_num_threads(1);
    std::cout << "Number of threads set to: " << omp_get_max_threads() << std::endl;

    
    #pragma omp parallel
    {
        int tid = omp_get_thread_num(); //id текущего
        int nthreads = omp_get_num_threads(); //общего
        #pragma omp critical
        {
            std::cout << "Thread " << tid << " of " << nthreads << std::endl;
        }
        
        if (tid == 0) {
            #pragma omp critical
            std::cout << "Master thread: total threads = " << nthreads << std::endl;
        }
    }
    
    return 0;
}