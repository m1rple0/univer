#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <chrono>
#include <cstring>
#include <iomanip>
#include <omp.h>

using namespace std;
using namespace chrono;

struct Record {
    int id;
    char category[32];
    double value;
    int flag;
};

int main() {
    int sizes[] = {20, 1000000, 5000000, 10000000};
    const char* categories[] = {"Electronics", "Clothing", "Food", "Books"};
    double threshold = 50.0;
    int thread_counts[] = {1, 2, 4, 8};
    
    cout << "========== OPENMP VERSION ==========" << endl;
    cout << "N,Threads,Time(ms)" << endl;
    
    for (int size_idx = 0; size_idx < 4; size_idx++) {
        int N = sizes[size_idx];
        
        // Генерация данных
        vector<Record> data(N);
        for (int i = 0; i < N; i++) {
            data[i].id = i;
            strcpy(data[i].category, categories[rand() % 4]);
            data[i].value = (rand() % 10000) / 100.0;
            data[i].flag = rand() % 2;
        }
        
        // Для N=20 показываем исходные данные один раз
        if (N == 20) {
            cout << "\n=== ИСХОДНЫЕ ДАННЫЕ (N=20) ===" << endl;
            cout << left << setw(5) << "ID" << setw(15) << "Category" << setw(10) << "Value" << "Flag" << endl;
            cout << "----------------------------------------" << endl;
            for (int i = 0; i < N; i++) {
                cout << left << setw(5) << data[i].id 
                     << setw(15) << data[i].category 
                     << setw(10) << data[i].value 
                     << data[i].flag << endl;
            }
        }
        
        // Тестирование с разным числом потоков
        for (int t = 0; t < 4; t++) {
            int num_threads = thread_counts[t];
            omp_set_num_threads(num_threads);
            
            auto start = high_resolution_clock::now();
            
            vector<unordered_map<string, pair<double, int>>> local(num_threads);
            vector<vector<Record>> local_filtered(num_threads);  // для отфильтрованных записей
            
            #pragma omp parallel
            {
                int tid = omp_get_thread_num();
                
                #pragma omp for schedule(static, 1000)
                for (int i = 0; i < N; i++) {
                    if (data[i].flag == 1 && data[i].value > threshold) {
                        string cat(data[i].category);
                        local[tid][cat].first += data[i].value;
                        local[tid][cat].second++;
                        
                        if (N == 20) {
                            local_filtered[tid].push_back(data[i]);
                        }
                    }
                }
            }
            
            // Слияние результатов
            unordered_map<string, pair<double, int>> global;
            vector<Record> global_filtered;
            
            for (int i = 0; i < num_threads; i++) {
                for (auto& p : local[i]) {
                    global[p.first].first += p.second.first;
                    global[p.first].second += p.second.second;
                }
                // Собираем отфильтрованные записи
                global_filtered.insert(global_filtered.end(), 
                                       local_filtered[i].begin(), 
                                       local_filtered[i].end());
            }
            
            auto end = high_resolution_clock::now();
            double time_ms = duration_cast<milliseconds>(end - start).count();
            
            // Для N=20 показываем результаты для 1 потока
            if (N == 20 && num_threads == 1) {
                cout << "\n=== ОТФИЛЬТРОВАННЫЕ ДАННЫЕ (flag=1 и value>50) ===" << endl;
                cout << left << setw(5) << "ID" << setw(15) << "Category" << setw(10) << "Value" << "Flag" << endl;
                cout << "----------------------------------------" << endl;
                for (const auto& rec : global_filtered) {
                    cout << left << setw(5) << rec.id 
                         << setw(15) << rec.category 
                         << setw(10) << rec.value 
                         << rec.flag << endl;
                }
                
                cout << "\n=== РЕЗУЛЬТАТЫ АГРЕГАЦИИ ===" << endl;
                cout << left << setw(15) << "Category" << setw(10) << "SUM" << setw(10) << "COUNT" << setw(10) << "AVG" << endl;
                cout << "----------------------------------------" << endl;
                for (auto& p : global) {
                    double avg = p.second.second > 0 ? p.second.first / p.second.second : 0;
                    cout << left << setw(15) << p.first 
                         << setw(10) << fixed << setprecision(2) << p.second.first
                         << setw(10) << p.second.second
                         << setw(10) << fixed << setprecision(2) << avg << endl;
                }
                cout << "\n";
            }
            
            cout << N << "," << num_threads << "," << time_ms << endl;
        }
    }
    
    return 0;
}