#include <iostream>
#include <vector>
#include <cstdlib>
#include <fstream>
#include <string>
#include <omp.h>

using namespace std;

long long filter_and_sum_openmp(const vector<int>& data, int key, 
                                 int num_threads, int chunk_size = 0) {
    long long sum = 0;
    omp_set_num_threads(num_threads);
    
    if (chunk_size == 0) {
        #pragma omp parallel for reduction(+:sum)
        for (int i = 0; i < (int)data.size(); i++) {
            if (data[i] % key == 0) {
                sum += data[i];
            }
        }
    } else {
        #pragma omp parallel for reduction(+:sum) schedule(static, chunk_size)
        for (int i = 0; i < (int)data.size(); i++) {
            if (data[i] % key == 0) {
                sum += data[i];
            }
        }
    }
    
    return sum;
}

vector<int> generate_array(int size, int seed = 42) {
    vector<int> arr(size);
    srand(seed);
    for (int i = 0; i < size; i++) {
        arr[i] = rand() % 1000;
    }
    return arr;
}

int main() {
    int sizes[] = {10000000, 50000000, 100000000, 200000000};
    int key = 13;
    int threads[] = {1, 2, 4, 8};
    int chunks[] = {0, 1000, 10000, 100000};
    
    ofstream results_file("results_openmp.csv");
    results_file << "N,threads,chunk_size,time_seconds,speedup,efficiency,result" << endl;
    
    cout << "OpenMP" << endl;
    
    // Загружаем последовательные времена
    double seq_times[4] = {0};
    ifstream seq_file("results_sequential.csv");
    if (!seq_file.is_open()) {
        cout << "ОШИБКА? сначал sequential" << endl;
        return 1;
    }
    
    string line;
    getline(seq_file, line); // пропускаем заголовок
    
    for (int i = 0; i < 4; i++) {
        if (getline(seq_file, line)) {
            // Разбираем строку: N,time_seconds,sum_result
            size_t pos1 = line.find(',');
            size_t pos2 = line.find(',', pos1 + 1);
            
            string time_str = line.substr(pos1 + 1, pos2 - pos1 - 1);
            seq_times[i] = stod(time_str);
        }
    }
    seq_file.close();
    
    for (int sz = 0; sz < 4; sz++) {
        int N = sizes[sz];
        double T_seq = seq_times[sz];
        
        cout << "РАЗМЕР: " << N << " записей" << endl;
        cout << "Последовательное время: " << T_seq << " сек" << endl;
        
        cout << "Генерация данных... ";
        vector<int> data = generate_array(N);
        cout << "Готово" << endl << endl;
        
        cout << "Потоки\tБлок\tВремя(с)\tУскорение\tЭффективность" << endl;
        
        
        for (int t = 0; t < 4; t++) {
            int p = threads[t];
            for (int c = 0; c < 4; c++) {
                int chunk = chunks[c];
                
                double start = omp_get_wtime();
                long long result = filter_and_sum_openmp(data, key, p, chunk);
                double end = omp_get_wtime();
                
                double T_par = end - start;
                double speedup = T_seq / T_par;
                double efficiency = speedup / p;
                
                cout << p << "\t";
                if (chunk == 0) cout << "авто";
                else cout << chunk;
                cout << "\t" << T_par << "\t" << speedup << "\t\t" << efficiency << endl;
                
                results_file << N << "," << p << "," << chunk << ","
                             << T_par << "," << speedup << "," << efficiency << ","
                             << result << endl;
            }
        }
        cout << endl;
    }
    
    results_file.close();
    
    return 0;
}