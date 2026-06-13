#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>
#include <cctype>
#include <mpi.h>

using namespace std;

struct Result {
    int filePos;
    int patternId;
    int processRank;
};

// Функция для перевода строки в нижний регистр
string toLower(const string& s) {
    string result = s;
    for (char& c : result) {
        c = tolower(c);
    }
    return result;
}

// Регистронезависимый поиск
vector<Result> findAllMatchesCaseInsensitive(const string& text, int startPos, int rank,
                                               const vector<string>& patterns) {
    vector<Result> results;
    string lowerText = toLower(text);
    
    for (size_t p = 0; p < patterns.size(); p++) {
        const string& pattern = patterns[p];
        string lowerPattern = toLower(pattern);
        size_t pos = 0;
        while ((pos = lowerText.find(lowerPattern, pos)) != string::npos) {
            Result r;
            r.filePos = startPos + pos;
            r.patternId = p;
            r.processRank = rank;
            results.push_back(r);
            pos += lowerPattern.length();
        }
    }
    return results;
}

int main(int argc, char** argv) {
    MPI_Init(&argc, &argv);
    
    int rank, size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    // Шаблоны для поиска (в нижнем регистре)
    vector<string> patterns = {"error", "warning", "failed", "timeout", "exception"};
    int numPatterns = patterns.size();
    
    string filename = "input.txt";
    string fileContent;
    int fileSize = 0;
    
    double startTime = MPI_Wtime();
    
    // ===== ПРОЦЕСС 0: ЧИТАЕТ ФАЙЛ =====
    if (rank == 0) {
        ifstream file(filename);
        if (file.is_open()) {
            stringstream buffer;
            buffer << file.rdbuf();
            fileContent = buffer.str();
            fileSize = fileContent.length();
            file.close();
        }
        
        cout << "\n========================================" << endl;
        cout << "ЛР4: Поиск строк в файле (коллективные MPI)" << endl;
        cout << "Регистронезависимый поиск" << endl;
        cout << "========================================" << endl;
        cout << "Файл: " << filename << " (" << fileSize << " байт)" << endl;
        cout << "Шаблоны: ";
        for (const auto& p : patterns) cout << "\"" << p << "\" ";
        cout << endl;
        cout << "Процессов: " << size << endl;
        cout << "========================================\n" << endl;
    }
    
    MPI_Bcast(&fileSize, 1, MPI_INT, 0, MPI_COMM_WORLD);
    
    if (fileSize == 0) {
        if (rank == 0) cout << "Ошибка: файл не найден!" << endl;
        MPI_Finalize();
        return 1;
    }
    
    // ===== РАССЫЛКА ШАБЛОНОВ =====
    int totalPatternsSize = 0;
    vector<int> patternSizes(numPatterns);
    
    if (rank == 0) {
        for (int i = 0; i < numPatterns; i++) {
            patternSizes[i] = patterns[i].size() + 1;
            totalPatternsSize += patternSizes[i];
        }
    }
    
    MPI_Bcast(&totalPatternsSize, 1, MPI_INT, 0, MPI_COMM_WORLD);
    
    char* allPatterns = new char[totalPatternsSize + 1];
    
    if (rank == 0) {
        int offset = 0;
        for (int i = 0; i < numPatterns; i++) {
            strcpy(allPatterns + offset, patterns[i].c_str());
            offset += patternSizes[i];
        }
    }
    
    MPI_Bcast(allPatterns, totalPatternsSize, MPI_CHAR, 0, MPI_COMM_WORLD);
    
    if (rank != 0) {
        patterns.clear();
        int offset = 0;
        for (int i = 0; i < numPatterns; i++) {
            string p(allPatterns + offset);
            patterns.push_back(p);
            offset += p.size() + 1;
        }
    }
    
    // ===== РАСПРЕДЕЛЕНИЕ ФАЙЛА =====
    int maxPatternLen = 0;
    for (const auto& p : patterns) {
        if ((int)p.length() > maxPatternLen) maxPatternLen = p.length();
    }
    int overlap = maxPatternLen;
    
    int baseChunk = fileSize / size;
    int remainder = fileSize % size;
    
    int* chunkSizes = new int[size];
    int* offsets = new int[size];
    
    int currentOffset = 0;
    for (int i = 0; i < size; i++) {
        offsets[i] = currentOffset;
        int chunk = baseChunk + (i < remainder ? 1 : 0);
        
        if (i < size - 1) {
            chunkSizes[i] = chunk + overlap;
            currentOffset += chunk;
        } else {
            chunkSizes[i] = chunk;
            currentOffset += chunk;
        }
    }
    
    for (int i = 0; i < size; i++) {
        if (offsets[i] + chunkSizes[i] > fileSize) {
            chunkSizes[i] = fileSize - offsets[i];
        }
    }
    
    char* myChunk = new char[chunkSizes[rank] + 1];
    
    MPI_Scatterv(
        (rank == 0) ? (void*)fileContent.c_str() : nullptr,
        chunkSizes, offsets, MPI_CHAR,
        myChunk, chunkSizes[rank], MPI_CHAR,
        0, MPI_COMM_WORLD
    );
    myChunk[chunkSizes[rank]] = '\0';
    
    // ===== ПОИСК (регистронезависимый) =====
    vector<Result> allMatches = findAllMatchesCaseInsensitive(string(myChunk), offsets[rank], rank, patterns);
    
    // Фильтруем дубликаты на границах
    vector<Result> filteredResults;
    int originalEnd = offsets[rank] + (baseChunk + (rank < remainder ? 1 : 0));
    if (rank == size - 1) originalEnd = fileSize;
    
    for (const auto& res : allMatches) {
        if (res.filePos < originalEnd) {
            filteredResults.push_back(res);
        }
    }
    
    // ===== СБОР РЕЗУЛЬТАТОВ =====
    int localCount = filteredResults.size();
    int* allCounts = new int[size];
    
    MPI_Gather(&localCount, 1, MPI_INT, allCounts, 1, MPI_INT, 0, MPI_COMM_WORLD);
    
    int totalCount = 0;
    int* recvOffsets = new int[size];
    
    if (rank == 0) {
        for (int i = 0; i < size; i++) {
            recvOffsets[i] = totalCount;
            totalCount += allCounts[i];
        }
    }
    
    int* localPositions = new int[localCount];
    int* localPatternIds = new int[localCount];
    int* localRanks = new int[localCount];
    
    for (int i = 0; i < localCount; i++) {
        localPositions[i] = filteredResults[i].filePos;
        localPatternIds[i] = filteredResults[i].patternId;
        localRanks[i] = filteredResults[i].processRank;
    }
    
    int* globalPositions = nullptr;
    int* globalPatternIds = nullptr;
    int* globalRanks = nullptr;
    
    if (rank == 0 && totalCount > 0) {
        globalPositions = new int[totalCount];
        globalPatternIds = new int[totalCount];
        globalRanks = new int[totalCount];
    }
    
    MPI_Gatherv(localPositions, localCount, MPI_INT,
                globalPositions, allCounts, recvOffsets, MPI_INT,
                0, MPI_COMM_WORLD);
    
    MPI_Gatherv(localPatternIds, localCount, MPI_INT,
                globalPatternIds, allCounts, recvOffsets, MPI_INT,
                0, MPI_COMM_WORLD);
    
    MPI_Gatherv(localRanks, localCount, MPI_INT,
                globalRanks, allCounts, recvOffsets, MPI_INT,
                0, MPI_COMM_WORLD);
    
    double endTime = MPI_Wtime();
    
    // ===== ВЫВОД РЕЗУЛЬТАТОВ =====
    if (rank == 0) {
        cout << "\n========== РЕЗУЛЬТАТЫ ПОИСКА ==========" << endl;
        
        if (totalCount == 0) {
            cout << "Совпадений не найдено." << endl;
        } else {
            // Сортировка по позиции
            for (int i = 0; i < totalCount; i++) {
                for (int j = i + 1; j < totalCount; j++) {
                    if (globalPositions[i] > globalPositions[j]) {
                        swap(globalPositions[i], globalPositions[j]);
                        swap(globalPatternIds[i], globalPatternIds[j]);
                        swap(globalRanks[i], globalRanks[j]);
                    }
                }
            }
            
            for (int i = 0; i < totalCount; i++) {
                cout << "[" << globalRanks[i] << "] Позиция " << globalPositions[i]
                     << " -> \"" << patterns[globalPatternIds[i]] << "\"" << endl;
            }
        }
        
        cout << "========================================" << endl;
        cout << "Всего совпадений: " << totalCount << endl;
        cout << "Время выполнения: " << (endTime - startTime) << " сек" << endl;
        cout << "========================================" << endl;
        
        delete[] allCounts;
        delete[] recvOffsets;
        if (globalPositions) delete[] globalPositions;
        if (globalPatternIds) delete[] globalPatternIds;
        if (globalRanks) delete[] globalRanks;
    }
    
    delete[] chunkSizes;
    delete[] offsets;
    delete[] myChunk;
    delete[] allPatterns;
    delete[] localPositions;
    delete[] localPatternIds;
    delete[] localRanks;
    
    MPI_Finalize();
    return 0;
}
