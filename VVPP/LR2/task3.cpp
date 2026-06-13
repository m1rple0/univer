#include <iostream>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include "omp.h"
using namespace std;

int low_limit_nodes = 150;
int percent = 70;
int plus_num_node = 50;

struct node {
    struct node *left;
    struct node *right;
    int num;
    int param;
};

void tree_init(struct node *tree, int mode) {
    static int loc_val;
    if (mode < 1) {
        loc_val = 1;
        srand(time(NULL));
    }
    tree->num = loc_val++;
    tree->param = rand() % 10001;
    tree->left = NULL;
    tree->right = NULL;
    
    if (loc_val > low_limit_nodes)
        return;
    
    int n = rand() % 100;
    if (n < percent) {
        tree->left = new node;
        tree_init(tree->left, 1);
    }
    
    n = rand() % 100;
    if (n < percent) {
        tree->right = new node;
        tree_init(tree->right, 1);
    }
}

void work(int n) {
    long long k = 1;
    int limit = (n * plus_num_node) * (n * plus_num_node);
    for(int i = 2; i <= limit; i++)
        k *= i;
}

// 3а. Последовательный поиск (все подходящие)
void search_serial(node *tree, int par, int prec, int &found, int &total) {
    if (!tree) return;
    total++;
    work(tree->num);
    if (abs(tree->param - par) <= prec) found++;
    search_serial(tree->left, par, prec, found, total);
    search_serial(tree->right, par, prec, found, total);
}

// 3б. Параллельный поиск с atomic
int total_atomic = 0, found_atomic = 0;
void search_atomic(node *tree, int par, int prec) {
    if (!tree) return;
    #pragma omp atomic
    total_atomic++;
    work(tree->num);
    if (abs(tree->param - par) <= prec) {
        #pragma omp atomic
        found_atomic++;
    }
    #pragma omp task
    if (tree->left) search_atomic(tree->left, par, prec);
    #pragma omp task
    if (tree->right) search_atomic(tree->right, par, prec);
}

// 3в. Параллельный поиск с reduction (переменнные локальные)
int total_reduction = 0, found_reduction = 0;
void search_reduction(node *tree, int par, int prec, int &total_local, int &found_local) {
    if (!tree) return;
    total_local++;
    work(tree->num);
    if (abs(tree->param - par) <= prec) found_local++;
    #pragma omp task
    if (tree->left) search_reduction(tree->left, par, prec, total_local, found_local);
    #pragma omp task
    if (tree->right) search_reduction(tree->right, par, prec, total_local, found_local);
}

// 3г. Последовательный поиск первой вершины 
bool found_serial = false;
node* result_serial = NULL;
int total_first_serial = 0;

void search_first_serial(node *tree, int par, int prec) {
    if (!tree || found_serial) return;
    total_first_serial++;
    work(tree->num);
    if (abs(tree->param - par) <= prec) {
        found_serial = true;
        result_serial = tree;
        return;
    }
    search_first_serial(tree->left, par, prec);
    search_first_serial(tree->right, par, prec);
}

// 3е. Параллельный поиск первой вершины
int found_parallel = 0;
node* result_parallel = NULL;
int total_first_parallel = 0;

void search_first_parallel(node *tree, int par, int prec) {
    if (!tree || found_parallel) return;
    #pragma omp atomic
    total_first_parallel++;
    work(tree->num);
    if (abs(tree->param - par) <= prec) {
        #pragma omp critical
        if (!found_parallel) {
            found_parallel = 1;
            result_parallel = tree;
        }
        return;
    }
    if (!found_parallel) {
        #pragma omp task
        if (tree->left) search_first_parallel(tree->left, par, prec);
        #pragma omp task
        if (tree->right) search_first_parallel(tree->right, par, prec);
        #pragma omp taskwait
    }
}

int main() {
    struct node tree;
    tree_init(&tree, 0);
    
    int par, prec;
    cout << "Введите Par (0..10000): ";
    cin >> par;
    cout << "Введите Prec: ";
    cin >> prec;
    cout << "\n";
    
    // 3а. Последовательный поиск всех подходящих
    cout << "Последовательный поиск" << endl;
    int found_all_serial = 0, total_all_serial = 0;
    double start = omp_get_wtime();
    search_serial(&tree, par, prec, found_all_serial, total_all_serial);
    double time_serial_all = omp_get_wtime() - start;
    cout << "Обработано: " << total_all_serial << ", Найдено: " << found_all_serial << endl;
    cout << "Время: " << time_serial_all << " сек\n" << endl;
    
    // 3б. Параллельный поиск с atomic
    cout << "Параллельный поиск" << endl;
    total_atomic = found_atomic = 0;
    start = omp_get_wtime();
    #pragma omp parallel
    {
        #pragma omp single
        search_atomic(&tree, par, prec);
    }
    double time_atomic = omp_get_wtime() - start;
    cout << "Обработано: " << total_atomic << ", Найдено: " << found_atomic << endl;
    cout << "Время: " << time_atomic << " сек\n" << endl;
    
    // 3в. Параллельный поиск с reduction
    cout << "Параллельный поиск" << endl;
    total_reduction = found_reduction = 0;
    start = omp_get_wtime();
    #pragma omp parallel
    {
        int total_local = 0, found_local = 0;
        #pragma omp single
        search_reduction(&tree, par, prec, total_local, found_local);
        #pragma omp atomic
        total_reduction += total_local;
        #pragma omp atomic
        found_reduction += found_local;
    }
    double time_reduction = omp_get_wtime() - start;
    cout << "Обработано: " << total_reduction << ", Найдено: " << found_reduction << endl;
    cout << "Время: " << time_reduction << " сек\n" << endl;
    
    // 3г. Последовательный поиск первой подходящей
    cout << "Последовательный поиск " << endl;
    found_serial = false;
    result_serial = NULL;
    total_first_serial = 0;
    start = omp_get_wtime();
    search_first_serial(&tree, par, prec);
    double time_serial_first = omp_get_wtime() - start;
    if (result_serial)
        cout << "Найдена вершина #" << result_serial->num << " (параметр=" << result_serial->param << ")" << endl;
    else
        cout << "Вершина не найдена" << endl;
    cout << "Обработано: " << total_first_serial << endl;
    cout << "Время: " << time_serial_first << " сек\n" << endl;
    
    // 3е. Параллельный поиск первой подходящей
    cout << "Параллельный поиск (первая подходящая)" << endl;
    found_parallel = 0;
    result_parallel = NULL;
    total_first_parallel = 0;
    start = omp_get_wtime();
    #pragma omp parallel
    {
        #pragma omp single
        search_first_parallel(&tree, par, prec);
    }
    double time_parallel_first = omp_get_wtime() - start;
    if (result_parallel)
        cout << "Найдена вершина #" << result_parallel->num << " (параметр=" << result_parallel->param << ")" << endl;
    else
        cout << "Вершина не найдена" << endl;
    cout << "Обработано: " << total_first_parallel << endl;
    cout << "Время: " << time_parallel_first << " сек\n" << endl;
    
    // Сравнительная таблица
    cout << "Cравнение" << endl;
    cout << "3а (serial all):        " << time_serial_all << " сек" << endl;
    cout << "3б (atomic all):        " << time_atomic << " сек" << endl;
    cout << "3в (reduction all):     " << time_reduction << " сек" << endl;
    cout << "3г (serial first):      " << time_serial_first << " сек" << endl;
    cout << "3е (parallel first):    " << time_parallel_first << " сек" << endl;
    
    return 0;
}