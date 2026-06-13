#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <ctime>
#include <cstring>
#include <iomanip>

using namespace std;

struct Record {
    int id;
    char category[32];
    double value;
    int flag;
};

int main() {
    int sizes[] = {20, 1000000, 5000000, 10000000};  // 20 записей для проверки
    const char* categories[] = {"Electronics", "Clothing", "Food", "Books"};
    double threshold = 50.0;
    
    cout << "========== SEQUENTIAL VERSION ==========" << endl;
    
    for (int idx = 0; idx < 4; idx++) {
        int N = sizes[idx];
        
        // Генерация данных
        vector<Record> data(N);
        for (int i = 0; i < N; i++) {
            data[i].id = i;
            strcpy(data[i].category, categories[rand() % 4]);
            data[i].value = (rand() % 10000) / 100.0;
            data[i].flag = rand() % 2;
        }
        
        // Для маленького N (20 записей) показываем все данные
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
        
        clock_t start = clock();
        
        unordered_map<string, pair<double, int>> result;
        vector<Record> filtered;  // сохраняем отфильтрованные записи
        
        for (int i = 0; i < N; i++) {
            if (data[i].flag == 1 && data[i].value > threshold) {
                string cat(data[i].category);
                result[cat].first += data[i].value;
                result[cat].second++;
                filtered.push_back(data[i]);  // запоминаем отфильтрованные
            }
        }
        
        clock_t end = clock();
        double time_ms = (double)(end - start) / CLOCKS_PER_SEC * 1000;
        
        // Для маленького N показываем отфильтрованные данные
        if (N == 20) {
            cout << "\n=== ОТФИЛЬТРОВАННЫЕ ДАННЫЕ (flag=1 и value>50) ===" << endl;
            cout << left << setw(5) << "ID" << setw(15) << "Category" << setw(10) << "Value" << "Flag" << endl;
            cout << "----------------------------------------" << endl;
            for (const auto& rec : filtered) {
                cout << left << setw(5) << rec.id 
                     << setw(15) << rec.category 
                     << setw(10) << rec.value 
                     << rec.flag << endl;
            }
            
            cout << "\n=== РЕЗУЛЬТАТЫ АГРЕГАЦИИ ===" << endl;
            cout << left << setw(15) << "Category" << setw(10) << "SUM" << setw(10) << "COUNT" << setw(10) << "AVG" << endl;
            cout << "----------------------------------------" << endl;
            for (auto& p : result) {
                double avg = p.second.second > 0 ? p.second.first / p.second.second : 0;
                cout << left << setw(15) << p.first 
                     << setw(10) << fixed << setprecision(2) << p.second.first
                     << setw(10) << p.second.second
                     << setw(10) << fixed << setprecision(2) << avg << endl;
            }
            cout << "\n";
        }
        
        cout << N << "," << 1 << "," << time_ms << endl;
    }
    
    return 0;
}