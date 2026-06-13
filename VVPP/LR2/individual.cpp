#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <omp.h>

using namespace std;

struct SearchResult {
    string substring;
    bool found;
    int line_number;
};

// Параллельный поиск с tasks (блочное разбиение)
void parallel_file_search_tasks(const vector<string>& lines,
                                 const vector<string>& substrings,
                                 vector<SearchResult>& results,
                                 int chunk_size = 1000) {
    results.clear();
    for (const auto& sub : substrings) {
        results.push_back({sub, false, -1});
    }
    
    int num_chunks = (lines.size() + chunk_size - 1) / chunk_size;
    
    #pragma omp parallel
    {
        #pragma omp single
        {
            for (int chunk = 0; chunk < num_chunks; chunk++) {
                #pragma omp task
                {
                    int start = chunk * chunk_size;
                    int end = min(start + chunk_size, (int)lines.size());
                    
                    for (int i = start; i < end; i++) {
                        for (size_t s = 0; s < substrings.size(); s++) {
                            if (!results[s].found && lines[i].find(substrings[s]) != string::npos) {
                                #pragma omp critical
                                {
                                    if (!results[s].found) {
                                        results[s].found = true;
                                        results[s].line_number = i + 1;
                                        cout << "Поток " << omp_get_thread_num() 
                                             << " нашёл \"" << substrings[s] 
                                             << "\" в строке " << i + 1 << endl;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

// Рекурсивный поиск с tasks
void recursive_search_tasks(const vector<string>& lines,
                            const vector<string>& substrings,
                            vector<SearchResult>& results,
                            int start, int end,
                            int depth = 0) {
    
    if (end - start < 1000 || depth > 3) {
        for (int i = start; i < end; i++) {
            for (size_t s = 0; s < substrings.size(); s++) {
                if (!results[s].found && lines[i].find(substrings[s]) != string::npos) {
                    #pragma omp critical
                    {
                        if (!results[s].found) {
                            results[s].found = true;
                            results[s].line_number = i + 1;
                        }
                    }
                }
            }
        }
        return;
    }
    
    int mid = (start + end) / 2;
    
    #pragma omp task
    recursive_search_tasks(lines, substrings, results, start, mid, depth + 1);
    
    #pragma omp task
    recursive_search_tasks(lines, substrings, results, mid, end, depth + 1);
    
    #pragma omp taskwait
}

// Создание тестового файла
void create_test_file(const string& filename, int num_lines) {
    ofstream file(filename);
    if (!file.is_open()) return;
    
    for (int i = 1; i <= num_lines; i++) {
        if (i % 1000 == 0)
            file << "Line " << i << ": ERROR - Something went wrong!\n";
        else if (i % 500 == 0)
            file << "Line " << i << ": WARNING - Low memory\n";
        else if (i % 2000 == 0)
            file << "Line " << i << ": SUCCESS - Operation completed\n";
        else if (i % 1500 == 0)
            file << "Line " << i << ": FAILED - Connection timeout\n";
        else
            file << "Line " << i << ": INFO - Normal operation\n";
    }
    file.close();
    cout << "Создан тестовый файл: " << filename << " (" << num_lines << " строк)\n";
}

int main() {
    
    string filename = "test_file_lab2.txt";
    const int NUM_LINES = 50000;
    
    create_test_file(filename, NUM_LINES);
    
    // Чтение файла
    vector<string> lines;
    ifstream infile(filename);
    if (!infile.is_open()) {
        cerr << "Не удалось открыть файл!\n";
        return 1;
    }
    
    string line;
    while (getline(infile, line)) {
        lines.push_back(line);
    }
    infile.close();
    
    cout << "Файл прочитан. Всего строк: " << lines.size() << endl;
    
    vector<string> substrings = {"ERROR", "WARNING", "SUCCESS", "FAILED"};
    vector<SearchResult> results;
    
    // Поиск с tasks (блочное разбиение)
    cout << "\nПоиск с tasks (блочное разбиение)\n";
    double start = omp_get_wtime();
    parallel_file_search_tasks(lines, substrings, results, 2000);
    double time_blocks = omp_get_wtime() - start;
    
    cout << "\nРезультаты поиска\n";
    for (size_t i = 0; i < substrings.size(); i++) {
        cout << "Подстрока \"" << results[i].substring << "\": ";
        if (results[i].found)
            cout << "найдена в строке " << results[i].line_number;
        else
            cout << "не найдена";
        cout << endl;
    }
    cout << "\nВремя (блочное разбиение): " << time_blocks << " сек\n";
    
    // Рекурсивный поиск с tasks
    cout << "\nРекурсивный поиск с tasks\n";
    vector<SearchResult> results_recursive;
    for (const auto& sub : substrings) {
        results_recursive.push_back({sub, false, -1});
    }
    
    start = omp_get_wtime();
    #pragma omp parallel
    {
        #pragma omp single
        {
            recursive_search_tasks(lines, substrings, results_recursive, 0, lines.size());
        }
    }
    double time_recursive = omp_get_wtime() - start;
    
    cout << "Время (рекурсивное разбиение): " << time_recursive << " сек\n";
    if (time_blocks > 0 && time_recursive > 0) {
        cout << "Сравнение: рекурсия " << (time_recursive < time_blocks ? "быстрее" : "медленнее") 
             << " блоков в " << (time_recursive < time_blocks ? time_blocks/time_recursive : time_recursive/time_blocks) << "x\n";
    }
    
    return 0;
}