#include <iostream>
#include <vector>
#include <omp.h>

const size_t N = 100000000; 
const double VALUE = 1.0;   

int main() {
    std::cout << "Array size: " << N << " elements" << std::endl;
    std::cout << "Each element value: " << VALUE << std::endl;
    std::cout << "Expected sum: " << N * VALUE << std::endl;
    
    // Выделяем и заполняем массив
    std::vector<double> arr(N, VALUE);  
    
    double start, end;
    double sum;
    double expected = N * VALUE;
    
    // 1. Последовательный вариант
    sum = 0.0;
    start = omp_get_wtime();
    for (size_t i = 0; i < N; ++i) {
        sum += arr[i];
    }
    end = omp_get_wtime();
    std::cout << "\n1. Sequential:" << std::endl;
    std::cout << "   Sum = " << sum << " (expected: " << expected << ")" << std::endl;
    std::cout << "   Time = " << (end - start) << " s" << std::endl;
    
    // 2. Reduction
    sum = 0.0;
    start = omp_get_wtime();
    #pragma omp parallel for reduction(+:sum) //каждый поток создает локальную sum
    for (size_t i = 0; i < N; ++i) {
        sum += arr[i];
    }
    end = omp_get_wtime(); //автоматически объединяет результат
    std::cout << "\n2. Reduction:" << std::endl;
    std::cout << "   Sum = " << sum << " (expected: " << expected << ")" << std::endl;
    std::cout << "   Time = " << (end - start) << " s" << std::endl;
    
    // 3. Atomic
    sum = 0.0;
    start = omp_get_wtime();
    #pragma omp parallel for
    for (size_t i = 0; i < N; ++i) {
        #pragma omp atomic        // сложение атомарно, постоянная синхронизация
        sum += arr[i];
    }
    end = omp_get_wtime();
    std::cout << "\n3. Atomic:" << std::endl;
    std::cout << "   Sum = " << sum << " (expected: " << expected << ")" << std::endl;
    std::cout << "   Time = " << (end - start) << " s" << std::endl;
    
    // 4. Critical
    sum = 0.0;
    start = omp_get_wtime();
    #pragma omp parallel for           // защищаеи всю операцию
    for (size_t i = 0; i < N; ++i) {   // потоки в очереди
        #pragma omp critical
        sum += arr[i];
    }
    end = omp_get_wtime();
    std::cout << "\n4. Critical:" << std::endl;
    std::cout << "   Sum = " << sum << " (expected: " << expected << ")" << std::endl;
    std::cout << "   Time = " << (end - start) << " s" << std::endl;
    
    // 5. Sections (ручное разделение)
    sum = 0.0;
    start = omp_get_wtime();
    int nthreads = omp_get_max_threads();
    
    #pragma omp parallel    //каждый поток обрабатывает свой блок
    {
        int tid = omp_get_thread_num();
        size_t block_size = N / nthreads;
        size_t start_idx = tid * block_size;
        size_t end_idx = (tid == nthreads - 1) ? N : start_idx + block_size;
        double local_sum = 0.0;
        
        for (size_t i = start_idx; i < end_idx; ++i) {
            local_sum += arr[i];
        }
        
        #pragma omp atomic    //для сложения атомарно
        sum += local_sum;
    }
    end = omp_get_wtime();
    std::cout << "\n5. Sections:" << std::endl;
    std::cout << "   Sum = " << sum << " (expected: " << expected << ")" << std::endl;
    std::cout << "   Time = " << (end - start) << " s" << std::endl;
    
    // 6. Pairwise (сдваивание) ((через массив))
    sum = 0.0;
    start = omp_get_wtime();
    std::vector<double> partial_sums(nthreads, 0.0);
    
    #pragma omp parallel       // сохраняет частичные суммы в массив
    {
        int tid = omp_get_thread_num();
        size_t block_size = N / nthreads;
        size_t start_idx = tid * block_size;
        size_t end_idx = (tid == nthreads - 1) ? N : start_idx + block_size;
        double local_sum = 0.0;
        
        for (size_t i = start_idx; i < end_idx; ++i) {
            local_sum += arr[i];
        }
        partial_sums[tid] = local_sum;    // последовательно
    }
    
    for (int i = 0; i < nthreads; ++i) {
        sum += partial_sums[i];
    }
    end = omp_get_wtime();
    std::cout << "\n6. Pairwise (сдваивание):" << std::endl;
    std::cout << "   Sum = " << sum << " (expected: " << expected << ")" << std::endl;
    std::cout << "   Time = " << (end - start) << " s" << std::endl;
    
    
    return 0;
}