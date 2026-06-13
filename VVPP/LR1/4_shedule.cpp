#include <iostream>
#include <vector>
#include <omp.h>

const size_t N = 100000000;
const int NUM_THREADS = 4;

int main() {
    std::cout << "Array size: " << N << " elements" << std::endl;
    std::cout << "Number of threads: " << NUM_THREADS << std::endl;
    
    omp_set_num_threads(NUM_THREADS);
    std::vector<float> arr(N, 1.0f);
    float sum;
    double start, end;
    
    // 1. Static (default) //Итерации делятся на блоки ДО выполнения цикла
    sum = 0.0f;
    start = omp_get_wtime();
    #pragma omp parallel for reduction(+:sum) schedule(static)
    for (size_t i = 0; i < N; ++i) {
        sum += arr[i];
    }
    end = omp_get_wtime();
    std::cout << "\n1. Static (default): " << (end - start) << " s" << std::endl;
    
    // 2. Static, chunk=1000
    sum = 0.0f;
    start = omp_get_wtime();
    #pragma omp parallel for reduction(+:sum) schedule(static, 1000)
    for (size_t i = 0; i < N; ++i) {
        sum += arr[i];
    }
    end = omp_get_wtime();
    std::cout << "2. Static (chunk=1000): " << (end - start) << " s" << std::endl;
    
    // 3. Static, chunk=100000
    sum = 0.0f;
    start = omp_get_wtime();
    #pragma omp parallel for reduction(+:sum) schedule(static, 100000)
    for (size_t i = 0; i < N; ++i) {
        sum += arr[i];
    }
    end = omp_get_wtime();
    std::cout << "3. Static (chunk=100000): " << (end - start) << " s" << std::endl;
    
    // 4. Dynamic, chunk=1000  //Итерации выдаются потокам ПО МЕРЕ выполнения.
    sum = 0.0f;
    start = omp_get_wtime();
    #pragma omp parallel for reduction(+:sum) schedule(dynamic, 1000)
    for (size_t i = 0; i < N; ++i) {
        sum += arr[i];
    }
    end = omp_get_wtime();
    std::cout << "4. Dynamic (chunk=1000): " << (end - start) << " s" << std::endl;
    
    // 5. Dynamic, chunk=100000
    sum = 0.0f;
    start = omp_get_wtime();
    #pragma omp parallel for reduction(+:sum) schedule(dynamic, 100000)
    for (size_t i = 0; i < N; ++i) {
        sum += arr[i];
    }
    end = omp_get_wtime();
    std::cout << "5. Dynamic (chunk=100000): " << (end - start) << " s" << std::endl;
    
    // 6. Guided, chunk=1000   //Размер блоков экспоненциально изменяется
    sum = 0.0f;
    start = omp_get_wtime();
    #pragma omp parallel for reduction(+:sum) schedule(guided, 1000)
    for (size_t i = 0; i < N; ++i) {
        sum += arr[i];
    }
    end = omp_get_wtime();
    std::cout << "6. Guided (chunk=1000): " << (end - start) << " s" << std::endl;
    
    // 7. Guided, chunk=100000
    sum = 0.0f;
    start = omp_get_wtime();
    #pragma omp parallel for reduction(+:sum) schedule(guided, 100000)
    for (size_t i = 0; i < N; ++i) {
        sum += arr[i];
    }
    end = omp_get_wtime();
    std::cout << "7. Guided (chunk=100000): " << (end - start) << " s" << std::endl;
    
    return 0;
}