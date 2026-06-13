#include <iostream>
#include <omp.h>

int main() {
    omp_set_num_threads(4);
    
    // Пример 1: без ordered  Порядок вывода зависит от планировщика OpenMP
    std::cout << "\n1. Without ordered:" << std::endl;
    #pragma omp parallel for
    for (int i = 0; i < 10; ++i) {
        #pragma omp critical
        std::cout << "   Iteration " << i << " from thread " << omp_get_thread_num() << std::endl;
    }
    
    // Пример 2: с ordered по порядку: 0,1,2,3
    std::cout << "\n2. With ordered:" << std::endl;
    std::cout << "   (iterations are executed in sequential order)" << std::endl;
    #pragma omp parallel for ordered
    for (int i = 0; i < 10; ++i) {
        #pragma omp ordered
        std::cout << "   Iteration " << i << " from thread " << omp_get_thread_num() << std::endl;
    }
    
    // Замер времени с вычислительной нагрузкой
    std::cout << "\n3. Performance:" << std::endl;
    
    const int ITERATIONS = 1000;
    const int WORKLOAD = 100000; // Количество итераций для имитации работы
    
    double start, end;
    volatile int result = 0; // volatile

    // Без ordered
    start = omp_get_wtime();
    #pragma omp parallel for
    for (int i = 0; i < ITERATIONS; ++i) {
        int local_sum = 0;
        for (int j = 0; j < WORKLOAD; ++j) {
            local_sum += j;
        }
        #pragma omp atomic
        result += local_sum;
    }
    end = omp_get_wtime();
    std::cout << "   Without ordered: " << (end - start) << " s" << std::endl;
    
    result = 0;
    
    // С ordered
    start = omp_get_wtime();
    #pragma omp parallel for ordered
    for (int i = 0; i < ITERATIONS; ++i) {
        int local_sum = 0;
        for (int j = 0; j < WORKLOAD; ++j) {
            local_sum += j;
        }
        #pragma omp ordered
        {
            #pragma omp atomic
            result += local_sum;
        }
    }
    end = omp_get_wtime();
    std::cout << "   With ordered:    " << (end - start) << " s" << std::endl;
    
    
    return 0;
}