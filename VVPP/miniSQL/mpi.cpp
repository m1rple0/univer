#include <iostream>
#include <vector>
#include <cstdlib>
#include <fstream>
#include <string>
#include <mpi.h>

using namespace std;

// Фильтрация и суммирование (MPI версия)
long long filter_and_sum_mpi(const vector<int>& data, int key, 
                              int my_rank, int total_processes) {
    int n = data.size();
    
    // Вычисляем, какую часть массива обрабатывает текущий процесс
    int chunk_size = n / total_processes;
    int start = my_rank * chunk_size;
    int end = (my_rank == total_processes - 1) ? n : start + chunk_size;
    
    // Каждый процесс считает сумму на своей части массива
    long long local_sum = 0;
    for (int i = start; i < end; i++) {
        if (data[i] % key == 0) {
            local_sum += data[i];
        }
    }
    
    // Собираем все локальные суммы на процессе 0
    long long global_sum = 0;
    MPI_Reduce(&local_sum, &global_sum, 1, MPI_LONG_LONG, MPI_SUM, 0, MPI_COMM_WORLD);
    
    return global_sum;
}

// Генерация массива
vector<int> generate_array(int size, int seed = 42) {
    vector<int> arr(size);
    srand(seed);
    for (int i = 0; i < size; i++) {
        arr[i] = rand() % 1000;
    }
    return arr;
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    
    int my_rank, total_processes;
    MPI_Comm_rank(MPI_COMM_WORLD, &my_rank);
    MPI_Comm_size(MPI_COMM_WORLD, &total_processes);
    
    int sizes[] = {10000000, 50000000, 100000000, 200000000};
    int key = 13;
    double seq_times[4] = {0};
    
    // Процесс 0 читает последовательные времена
    if (my_rank == 0) {
        ifstream seq_file("results_sequential.csv");
        if (!seq_file.is_open()) {
            cout << "ОШИБКА, сначал sequential" << endl;
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        
        string line;
        getline(seq_file, line); // пропускаем заголовок
        
        // Читаем 4 строки с результатами
        for (int i = 0; i < 4; i++) {
            if (getline(seq_file, line)) {
                // Разбираем CSV строку вручную (без sscanf)
                size_t first_comma = line.find(',');
                size_t second_comma = line.find(',', first_comma + 1);
                
                string time_str = line.substr(first_comma + 1, second_comma - first_comma - 1);
                seq_times[i] = stod(time_str);
            }
        }
        seq_file.close();
        
        cout << "MPI" << endl;
        cout << "Количество процессов: " << total_processes << endl << endl;
    }
    
    // Рассылаем последовательные времена всем процессам
    MPI_Bcast(seq_times, 4, MPI_DOUBLE, 0, MPI_COMM_WORLD);
    
    // Открываем файл для записи (только процесс 0)
    ofstream results_file;
    if (my_rank == 0) {
        // Открываем в режиме добавления (ios::app), чтобы не перезаписывать
        results_file.open("results_mpi.csv", ios::app);
        // Если файл пустой, пишем заголовок
        results_file.seekp(0, ios::end);
        if (results_file.tellp() == 0) {
            results_file << "N,processes,time_seconds,speedup,efficiency,result" << endl;
        }
        
        cout << "N\t\tВремя(с)\tУскорение\tЭффективность" << endl;
    }
    
    // Для каждого размера задачи
    for (int sz = 0; sz < 4; sz++) {
        int N = sizes[sz];
        double T_seq = seq_times[sz];
        
        vector<int> data;
        
        // Процесс 0 генерирует данные
        if (my_rank == 0) {
            cout << "Генерация " << N << " записей... " << flush;
            data = generate_array(N);
            cout << "Готово" << endl;
        }
        
        // Рассылаем размер массива
        MPI_Bcast(&N, 1, MPI_INT, 0, MPI_COMM_WORLD);
        
        // Все процессы выделяют память
        if (my_rank != 0) {
            data.resize(N);
        }
        
        // Рассылаем данные всем процессам
        MPI_Bcast(data.data(), N, MPI_INT, 0, MPI_COMM_WORLD);
        
        // Синхронизация перед измерением времени
        MPI_Barrier(MPI_COMM_WORLD);
        
        // Измеряем время вычислений
        double start_time = MPI_Wtime();
        long long result = filter_and_sum_mpi(data, key, my_rank, total_processes);
        double end_time = MPI_Wtime();
        
        double T_par = end_time - start_time;
        double speedup = T_seq / T_par;
        double efficiency = speedup / total_processes;
        
        // Только процесс 0 выводит результаты
        if (my_rank == 0) {
            cout << N << "\t" << T_par << "\t\t" << speedup << "\t\t" << efficiency << endl;
            results_file << N << "," << total_processes << ","
                         << T_par << "," << speedup << "," << efficiency << ","
                         << result << endl;
        }
        
        MPI_Barrier(MPI_COMM_WORLD);
    }
    
    if (my_rank == 0) {
        results_file.close();
    }
    
    MPI_Finalize();
    return 0;
}