#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <fstream>

using namespace std;

// Фильтрация и суммирование
long long filter_and_sum(const vector<int>& data, int key) {
    long long sum = 0;
    for (size_t i = 0; i < data.size(); i++) {
        if (data[i] % key == 0) {
            sum += data[i];
        }
    }
    return sum;
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

int main() {
    int sizes[] = {10000000, 50000000, 100000000, 200000000};
    int key = 13;
    
    ofstream results_file("results_sequential.csv");
    results_file << "N,time_seconds,sum_result" << endl;
    
    cout << "Последовательно" << endl;
    for (int i = 0; i < 4; i++) {
        int N = sizes[i];
        
        cout << "Генерируем массив из " << N << " чисел... ";
        vector<int> data = generate_array(N);
        
        clock_t start = clock();
        long long result = filter_and_sum(data, key); //filtracia i summ
        clock_t end = clock();
        
        double elapsed = double(end - start) / CLOCKS_PER_SEC;

        cout << "Результат: " << result << endl;
        cout << "Время: " << elapsed << " секунд" << endl << endl;
        
        results_file << N << "," << elapsed << "," << result << endl;
    }
    
    results_file.close();

    return 0;
}