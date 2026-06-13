#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstring>
#include <mpi.h>

using namespace std;

// Структура для результата поиска
struct SearchResult {
    int fileIndex;
    int lineNumber;
    string pattern;
    string foundLine;
};

// Функция поиска нескольких строк в одном файле
vector<SearchResult> searchInFile(const string& filename, 
                                   const vector<string>& patterns,
                                   int fileIndex) {
    vector<SearchResult> results;
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Не удалось открыть файл: " << filename << endl;
        return results;
    }
    
    string line;
    int lineNum = 0;
    while (getline(file, line)) {
        lineNum++;
        for (const auto& pattern : patterns) {
            if (line.find(pattern) != string::npos) {
                results.push_back({fileIndex, lineNum, pattern, line});
            }
        }
    }
    file.close();
    return results;
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    if (size < 2) {
        if (rank == 0) {
            cout << "Ошибка: нужно минимум 2 процесса." << endl;
            cout << "Запуск: mpirun -np N ./search_mpi" << endl;
        }
        MPI_Finalize();
        return 1;
    }
    
    // Список файлов для поиска (можно передавать через аргументы командной строки)
    vector<string> files;
    vector<string> patterns;
    
    if (rank == 0) {
        // --- Процесс 0: инициализация задачи ---
        
        // Файлы для поиска (вариант 13 - несколько файлов)
        files = {
            "file1.txt", "file2.txt", "file3.txt", "file4.txt"
        };
        
        // Строки для поиска (несколько)
        patterns = {
            "error", "warning", "failed", "timeout", "exception"
        };
        
        cout << "Поиск строк в файлах" << endl;
        cout << "Файлы: ";
        for (const auto& f : files) cout << f << " ";
        cout << endl;
        cout << "Шаблоны: ";
        for (const auto& p : patterns) cout << p << " ";
        cout << endl;
        
        // Отправляем количество файлов и шаблонов всем процессам
        int numFiles = files.size();
        int numPatterns = patterns.size();
        
        MPI_Bcast(&numFiles, 1, MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Bcast(&numPatterns, 1, MPI_INT, 0, MPI_COMM_WORLD);
        
        // Отправляем имена файлов
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < numFiles; j++) {
                int len = files[j].length() + 1;
                MPI_Send(&len, 1, MPI_INT, i, 100 + j, MPI_COMM_WORLD);
                MPI_Send(files[j].c_str(), len, MPI_CHAR, i, 200 + j, MPI_COMM_WORLD);
            }
        }
        
        // Отправляем шаблоны поиска
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < numPatterns; j++) {
                int len = patterns[j].length() + 1;
                MPI_Send(&len, 1, MPI_INT, i, 300 + j, MPI_COMM_WORLD);
                MPI_Send(patterns[j].c_str(), len, MPI_CHAR, i, 400 + j, MPI_COMM_WORLD);
            }
        }
        
    } else {
        // --- Процессы 1..N-1: получают данные ---
        
        int numFiles, numPatterns;
        MPI_Bcast(&numFiles, 1, MPI_INT, 0, MPI_COMM_WORLD);
        MPI_Bcast(&numPatterns, 1, MPI_INT, 0, MPI_COMM_WORLD);
        
        // Получаем имена файлов
        files.resize(numFiles);
        for (int j = 0; j < numFiles; j++) {
            int len;
            MPI_Recv(&len, 1, MPI_INT, 0, 100 + j, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            char* buffer = new char[len];
            MPI_Recv(buffer, len, MPI_CHAR, 0, 200 + j, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            files[j] = string(buffer);
            delete[] buffer;
        }
        
        // Получаем шаблоны поиска
        patterns.resize(numPatterns);
        for (int j = 0; j < numPatterns; j++) {
            int len;
            MPI_Recv(&len, 1, MPI_INT, 0, 300 + j, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            char* buffer = new char[len];
            MPI_Recv(buffer, len, MPI_CHAR, 0, 400 + j, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            patterns[j] = string(buffer);
            delete[] buffer;
        }
    }
    
    // --- Все процессы выполняют поиск в своих файлах ---
    double startTime = MPI_Wtime();
    
    // Распределяем файлы между процессами
    int numFiles = files.size();
    vector<SearchResult> allResults;
    
    for (int i = rank; i < numFiles; i += size) {
        cout << "[Процесс " << rank << "] Обрабатываю файл: " << files[i] << endl;
        vector<SearchResult> results = searchInFile(files[i], patterns, i);
        allResults.insert(allResults.end(), results.begin(), results.end());
    }
    
    double endTime = MPI_Wtime();
    double localTime = endTime - startTime;
    
    // --- Сбор результатов на процессе 0 через point-to-point обмен ---
    
    if (rank != 0) {
        // Отправляем количество результатов процессу 0
        int numResults = allResults.size();
        MPI_Send(&numResults, 1, MPI_INT, 0, 500, MPI_COMM_WORLD);
        
        // Отправляем каждый результат
        for (const auto& res : allResults) {
            MPI_Send(&res.fileIndex, 1, MPI_INT, 0, 501, MPI_COMM_WORLD);
            MPI_Send(&res.lineNumber, 1, MPI_INT, 0, 502, MPI_COMM_WORLD);
            
            int patternLen = res.pattern.length() + 1;
            MPI_Send(&patternLen, 1, MPI_INT, 0, 503, MPI_COMM_WORLD);
            MPI_Send(res.pattern.c_str(), patternLen, MPI_CHAR, 0, 504, MPI_COMM_WORLD);
            
            int lineLen = res.foundLine.length() + 1;
            MPI_Send(&lineLen, 1, MPI_INT, 0, 505, MPI_COMM_WORLD);
            MPI_Send(res.foundLine.c_str(), lineLen, MPI_CHAR, 0, 506, MPI_COMM_WORLD);
        }
        
        // Отправляем время выполнения
        MPI_Send(&localTime, 1, MPI_DOUBLE, 0, 507, MPI_COMM_WORLD);
        
    } else {
        // Процесс 0: собираем все результаты
        vector<SearchResult> globalResults;
        double maxTime = localTime;
        
        for (int p = 1; p < size; p++) {
            int numResults;
            MPI_Recv(&numResults, 1, MPI_INT, p, 500, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            
            for (int k = 0; k < numResults; k++) {
                SearchResult res;
                MPI_Recv(&res.fileIndex, 1, MPI_INT, p, 501, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                MPI_Recv(&res.lineNumber, 1, MPI_INT, p, 502, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                
                int patternLen;
                MPI_Recv(&patternLen, 1, MPI_INT, p, 503, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                char* patternBuf = new char[patternLen];
                MPI_Recv(patternBuf, patternLen, MPI_CHAR, p, 504, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                res.pattern = string(patternBuf);
                delete[] patternBuf;
                
                int lineLen;
                MPI_Recv(&lineLen, 1, MPI_INT, p, 505, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                char* lineBuf = new char[lineLen];
                MPI_Recv(lineBuf, lineLen, MPI_CHAR, p, 506, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                res.foundLine = string(lineBuf);
                delete[] lineBuf;
                
                globalResults.push_back(res);
            }
            
            double procTime;
            MPI_Recv(&procTime, 1, MPI_DOUBLE, p, 507, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
            if (procTime > maxTime) maxTime = procTime;
        }
        
        // Добавляем результаты самого процесса 0
        for (const auto& res : allResults) {
            globalResults.push_back(res);
        }
        
        // --- Вывод результатов ---
        cout << "\nРЕЗУЛЬТАТЫ" << endl;
        if (globalResults.empty()) {
            cout << "Совпадений не найдено." << endl;
        } else {
            for (const auto& res : globalResults) {
                cout << "Файл " << files[res.fileIndex] 
                     << ", строка " << res.lineNumber
                     << ", найдено: \"" << res.pattern << "\"" << endl;
                cout << "  Текст: " << res.foundLine << endl;
            }
        }
        
        cout << "Общее время выполнения: " << maxTime << " сек." << endl;
    }
    
    MPI_Finalize();
    return 0;
}