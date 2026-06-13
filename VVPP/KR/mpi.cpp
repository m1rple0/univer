#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <cstring>
#include <iomanip>
#include <mpi.h>

using namespace std;

struct Record {
    int id;
    char category[32];
    double value;
    int flag;
};

struct Packet {
    char category[32];
    double sum;
    int count;
};

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    int sizes[] = {20, 1000000, 5000000, 10000000};
    const char* categories[] = {"Electronics", "Clothing", "Food", "Books"};
    double threshold = 50.0;
    
    if (rank == 0) {
        cout << "========== MPI VERSION ==========" << endl;
    }
    
    for (int size_idx = 0; size_idx < 4; size_idx++) {
        int N = sizes[size_idx];
        
        int local_n = N / size;
        vector<Record> local_data(local_n);
        
        // Генерация данных (только на процессе 0)
        vector<Record> all_data;
        
        if (rank == 0) {
            all_data.resize(N);
            for (int i = 0; i < N; i++) {
                all_data[i].id = i;
                strcpy(all_data[i].category, categories[rand() % 4]);
                all_data[i].value = (rand() % 10000) / 100.0;
                all_data[i].flag = rand() % 2;
            }
            
            // Для N=20 показываем исходные данные
            if (N == 20) {
                cout << "\n=== ИСХОДНЫЕ ДАННЫЕ (N=20) ===" << endl;
                cout << left << setw(5) << "ID" << setw(15) << "Category" << setw(10) << "Value" << "Flag" << endl;
                cout << "----------------------------------------" << endl;
                for (int i = 0; i < N; i++) {
                    cout << left << setw(5) << all_data[i].id 
                         << setw(15) << all_data[i].category 
                         << setw(10) << fixed << setprecision(2) << all_data[i].value 
                         << all_data[i].flag << endl;
                }
            }
        }
        
        // Рассылка данных (используем MPI_Scatter для простоты)
        vector<Record> recv_buffer(local_n);
        MPI_Scatter(all_data.data(), local_n * sizeof(Record), MPI_BYTE,
                    recv_buffer.data(), local_n * sizeof(Record), MPI_BYTE,
                    0, MPI_COMM_WORLD);
        
        MPI_Barrier(MPI_COMM_WORLD);
        double start_time = MPI_Wtime();
        
        // Локальная агрегация
        unordered_map<string, pair<double, int>> local_result;
        
        for (int i = 0; i < local_n; i++) {
            if (recv_buffer[i].flag == 1 && recv_buffer[i].value > threshold) {
                string cat(recv_buffer[i].category);
                local_result[cat].first += recv_buffer[i].value;
                local_result[cat].second++;
            }
        }
        
        // Собираем все результаты на процессе 0
        // Сначала каждый процесс отправляет количество своих категорий
        int local_count = local_result.size();
        vector<int> counts(size);
        MPI_Gather(&local_count, 1, MPI_INT, counts.data(), 1, MPI_INT, 0, MPI_COMM_WORLD);
        
        // Каждый процесс упаковывает свои данные
        vector<pair<string, pair<double, int>>> flat_result(local_result.begin(), local_result.end());
        
        // Отправляем данные на процесс 0
        if (rank == 0) {
            // Сначала добавляем свои данные
            unordered_map<string, pair<double, int>> global_result = local_result;
            
            // Принимаем данные от других процессов
            for (int p = 1; p < size; p++) {
                int other_count = counts[p];
                for (int j = 0; j < other_count; j++) {
                    Packet pkt;
                    MPI_Recv(&pkt, sizeof(Packet), MPI_BYTE, p, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                    string cat(pkt.category);
                    global_result[cat].first += pkt.sum;
                    global_result[cat].second += pkt.count;
                }
            }
            
            double end_time = MPI_Wtime();
            double time_ms = (end_time - start_time) * 1000;
            
            // Для N=20 показываем результаты
            if (N == 20) {
                // Собираем отфильтрованные записи для вывода
                vector<Record> all_filtered;
                
                // Сначала добавляем свои отфильтрованные записи
                for (int i = 0; i < local_n; i++) {
                    if (recv_buffer[i].flag == 1 && recv_buffer[i].value > threshold) {
                        all_filtered.push_back(recv_buffer[i]);
                    }
                }
                
                // Принимаем отфильтрованные записи от других процессов
                for (int p = 1; p < size; p++) {
                    int other_filtered_count;
                    MPI_Recv(&other_filtered_count, 1, MPI_INT, p, 1, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                    for (int j = 0; j < other_filtered_count; j++) {
                        Record rec;
                        MPI_Recv(&rec, sizeof(Record), MPI_BYTE, p, 2, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                        all_filtered.push_back(rec);
                    }
                }
                
                cout << "\n=== ОТФИЛЬТРОВАННЫЕ ДАННЫЕ (flag=1 и value>50) ===" << endl;
                cout << left << setw(5) << "ID" << setw(15) << "Category" << setw(10) << "Value" << "Flag" << endl;
                cout << "----------------------------------------" << endl;
                for (const auto& rec : all_filtered) {
                    cout << left << setw(5) << rec.id 
                         << setw(15) << rec.category 
                         << setw(10) << fixed << setprecision(2) << rec.value 
                         << rec.flag << endl;
                }
                
                cout << "\n=== РЕЗУЛЬТАТЫ АГРЕГАЦИИ ===" << endl;
                cout << left << setw(15) << "Category" << setw(10) << "SUM" << setw(10) << "COUNT" << setw(10) << "AVG" << endl;
                cout << "----------------------------------------" << endl;
                for (auto& p : global_result) {
                    double avg = p.second.second > 0 ? p.second.first / p.second.second : 0;
                    cout << left << setw(15) << p.first 
                         << setw(10) << fixed << setprecision(2) << p.second.first
                         << setw(10) << p.second.second
                         << setw(10) << fixed << setprecision(2) << avg << endl;
                }
                cout << "\n";
            }
            
            cout << N << "," << size << "," << time_ms << endl;
            
        } else {
            // Отправляем свои результаты на процесс 0
            for (auto& p : local_result) {
                Packet pkt;
                strcpy(pkt.category, p.first.c_str());
                pkt.sum = p.second.first;
                pkt.count = p.second.second;
                MPI_Send(&pkt, sizeof(Packet), MPI_BYTE, 0, 0, MPI_COMM_WORLD);
            }
            
            // Отправляем отфильтрованные записи (только для N=20)
            if (N == 20) {
                vector<Record> local_filtered;
                for (int i = 0; i < local_n; i++) {
                    if (recv_buffer[i].flag == 1 && recv_buffer[i].value > threshold) {
                        local_filtered.push_back(recv_buffer[i]);
                    }
                }
                int filtered_count = local_filtered.size();
                MPI_Send(&filtered_count, 1, MPI_INT, 0, 1, MPI_COMM_WORLD);
                for (const auto& rec : local_filtered) {
                    MPI_Send(&rec, sizeof(Record), MPI_BYTE, 0, 2, MPI_COMM_WORLD);
                }
            }
        }
        
        MPI_Barrier(MPI_COMM_WORLD);
    }
    
    MPI_Finalize();
    return 0;
}