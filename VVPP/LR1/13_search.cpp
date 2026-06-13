#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <omp.h>

using namespace std;

int main(int argc, char* argv[]) {
    if (argc < 3) {
        cerr << "Usage: " << argv[0] << " <filename> <substring1> [substring2 ...]" << endl;
        return 1;
    }

    string filename = argv[1];
    vector<string> substrings;
    for (int i = 2; i < argc; ++i) {
        substrings.push_back(argv[i]);
    }

    // Находим максимальную длину искомой строки
    size_t max_len = 0;
    for (const auto& s : substrings) {
        if (s.length() > max_len) max_len = s.length();
    }

    // Читаем файл целиком
    ifstream file(filename, ios::binary);
    if (!file.is_open()) {
        cerr << "Cannot open file: " << filename << endl;
        return 1;
    }

    file.seekg(0, ios::end);
    streamsize fileSize = file.tellg();
    file.seekg(0, ios::beg);
    
    if (fileSize <= 0) {
        cerr << "File is empty or cannot read size" << endl;
        return 1;
    }
    
    string content(fileSize, '\0');
    file.read(&content[0], fileSize);
    file.close();

    // Определяем количество потоков
    int num_threads = 4; // значение по умолчанию
    if (const char* env = getenv("OMP_NUM_THREADS")) {
        int env_threads = atoi(env);
        if (env_threads > 0) num_threads = env_threads;
    }
    omp_set_num_threads(num_threads);

    cout << "File: " << filename << " (size: " << fileSize << " bytes)" << endl;
    cout << "Searching for " << substrings.size() << " strings:" << endl;
    for (const auto& s : substrings) {
        cout << "  - \"" << s << "\"" << endl;
    }
    cout << "Using " << num_threads << " threads" << endl;

    // Вектор для счётчиков
    vector<int> counts(substrings.size(), 0);

    // Время начала
    double start_time = omp_get_wtime();

    // Разбиваем файл на блоки с перекрытием
    size_t block_size = fileSize / num_threads;
    if (block_size == 0) block_size = fileSize;
    
    // Преобразуем fileSize в size_t для сравнений
    size_t fileSize_t = static_cast<size_t>(fileSize);

    #pragma omp parallel for schedule(static)
    for (int tid = 0; tid < num_threads; ++tid) {
        size_t start = tid * block_size;
        size_t end = (tid == num_threads - 1) ? fileSize_t : start + block_size;

        // Добавляем перекрытие на max_len символов
        size_t block_start = (start > max_len) ? start - max_len : 0;
        size_t block_end = (end + max_len < fileSize_t) ? end + max_len : fileSize_t;

        string block = content.substr(block_start, block_end - block_start);

        // Для каждой искомой строки ищем вхождения в этом блоке
        for (size_t idx = 0; idx < substrings.size(); ++idx) {
            const string& pattern = substrings[idx];
            size_t pos = block.find(pattern);
            int local_count = 0;
            
            while (pos != string::npos) {
                // Проверяем, что найденное вхождение принадлежит исходному блоку
                size_t global_pos = block_start + pos;
                if (global_pos >= start && global_pos + pattern.length() <= end) {
                    local_count++;
                }
                pos = block.find(pattern, pos + 1);
            }
            
            if (local_count > 0) {
                #pragma omp atomic
                counts[idx] += local_count;
            }
        }
    }

    double end_time = omp_get_wtime();
    double elapsed = end_time - start_time;

    // Вывод результатов
    cout << "\nSearch results:" << endl;
    for (size_t i = 0; i < substrings.size(); ++i) {
        cout << "  String \"" << substrings[i] << "\" found " << counts[i] << " times." << endl;
    }
    cout << "\nTotal search time: " << elapsed << " seconds" << endl;

    return 0;
}