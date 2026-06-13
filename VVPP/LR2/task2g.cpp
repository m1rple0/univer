#include <iostream>
#include <cstdlib>
#include <ctime>
#include "omp.h"
#include <vector>
using namespace std;

int num_nodes = 0;
int low_limit_nodes = 150;
int percent = 70;
int plus_num_node = 50;

struct node
{
    struct node *left;
    struct node *right;
    int num;
    int depth;  // для отладочного вывода
};

void tree_init(struct node *tree, int mode, int depth = 0)
{
    static int loc_val;
    if (mode < 1)
        loc_val = 1;
    tree->num = loc_val++;
    tree->depth = depth;
    tree->left = NULL;
    tree->right = NULL;
    
    if (loc_val > low_limit_nodes)
        return;
    
    int n = rand() % 100;
    if (n < percent)
    {
        tree->left = new node;
        tree_init(tree->left, 1, depth + 1);
    }
    
    n = rand() % 100;
    if (n < percent)
    {
        tree->right = new node;
        tree_init(tree->right, 1, depth + 1);
    }
}

void work(int n)
{
    long long k = 1;
    int limit = (n * plus_num_node) * (n * plus_num_node);
    for(int i = 2; i <= limit; i++)
        k *= i;
}

// Последовательная версия (обычный порядок - сверху вниз)
void node_process_topdown_serial(struct node *tree)
{
    num_nodes++;
    work(tree->num);
    cout << "Top-down (serial): node " << tree->num << " (depth " << tree->depth << ")" << endl;
    if (tree->left) node_process_topdown_serial(tree->left);
    if (tree->right) node_process_topdown_serial(tree->right);
}

// Последовательная версия (снизу вверх - листья к корню)
void node_process_bottomup_serial(struct node *tree)
{
    // Сначала обрабатываем потомков
    if (tree->left) node_process_bottomup_serial(tree->left);
    if (tree->right) node_process_bottomup_serial(tree->right);
    
    // Потом обрабатываем текущий узел
    num_nodes++;
    work(tree->num);
    cout << "Bottom-up (serial): node " << tree->num << " (depth " << tree->depth << ")" << endl;
}

// Параллельная версия (снизу вверх)
void node_process_bottomup_parallel(struct node *tree)
{
    // Создаём задачи для потомков
    #pragma omp task
    if (tree->left) node_process_bottomup_parallel(tree->left);
    
    #pragma omp task
    if (tree->right) node_process_bottomup_parallel(tree->right);
    
    // Ждём завершения всех потомков
    #pragma omp taskwait
    
    // Обрабатываем текущий узел только после потомков
    #pragma omp atomic
    num_nodes++;
    
    work(tree->num);
    
    #pragma omp critical
    cout << "Bottom-up (parallel): node " << tree->num 
         << " (depth " << tree->depth << ", thread " << omp_get_thread_num() << ")" << endl;
}

// Параллельная версия (сверху вниз для сравнения)
void node_process_topdown_parallel(struct node *tree)
{
    #pragma omp atomic
    num_nodes++;
    
    work(tree->num);
    
    #pragma omp critical
    cout << "Top-down (parallel): node " << tree->num 
         << " (depth " << tree->depth << ", thread " << omp_get_thread_num() << ")" << endl;
    
    #pragma omp task
    if (tree->left) node_process_topdown_parallel(tree->left);
    
    #pragma omp task
    if (tree->right) node_process_topdown_parallel(tree->right);
}

int main()
{
    struct node tree;
    srand(time(NULL));
    tree_init(&tree, 0);
    
    cout << "\n========================================" << endl;
    cout << "Сравнение обхода сверху-вниз и снизу-вверх" << endl;
    cout << "========================================\n" << endl;
    
    // 1. Последовательный обход сверху-вниз
    num_nodes = 0;
    double start = omp_get_wtime();
    node_process_topdown_serial(&tree);
    double time_topdown_serial = omp_get_wtime() - start;
    cout << "\n--- Top-down serial: " << time_topdown_serial 
         << " sec, nodes=" << num_nodes << " ---\n" << endl;
    
    // 2. Последовательный обход снизу-вверх
    num_nodes = 0;
    start = omp_get_wtime();
    node_process_bottomup_serial(&tree);
    double time_bottomup_serial = omp_get_wtime() - start;
    cout << "\n--- Bottom-up serial: " << time_bottomup_serial 
         << " sec, nodes=" << num_nodes << " ---\n" << endl;
    
    // 3. Параллельный обход сверху-вниз
    num_nodes = 0;
    start = omp_get_wtime();
    #pragma omp parallel
    {
        #pragma omp single
        {
            node_process_topdown_parallel(&tree);
        }
    }
    double time_topdown_parallel = omp_get_wtime() - start;
    cout << "\n--- Top-down parallel: " << time_topdown_parallel 
         << " sec, nodes=" << num_nodes << " ---\n" << endl;
    
    // 4. Параллельный обход снизу-вверх
    num_nodes = 0;
    start = omp_get_wtime();
    #pragma omp parallel
    {
        #pragma omp single
        {
            node_process_bottomup_parallel(&tree);
        }
    }
    double time_bottomup_parallel = omp_get_wtime() - start;
    cout << "\n--- Bottom-up parallel: " << time_bottomup_parallel 
         << " sec, nodes=" << num_nodes << " ---\n" << endl;
    
    // Вывод сравнительных результатов
    cout << "\n========================================" << endl;
    cout << "Сравнение времени выполнения:" << endl;
    cout << "========================================" << endl;
    cout << "Top-down (сверху-вниз)   serial:   " << time_topdown_serial << " sec" << endl;
    cout << "Bottom-up (снизу-вверх)  serial:   " << time_bottomup_serial << " sec" << endl;
    cout << "Top-down (сверху-вниз)   parallel: " << time_topdown_parallel << " sec" << endl;
    cout << "Bottom-up (снизу-вверх)  parallel: " << time_bottomup_parallel << " sec" << endl;
    
    double speedup_serial = time_topdown_serial / time_bottomup_serial;
    double speedup_parallel = time_topdown_parallel / time_bottomup_parallel;
    
    cout << "\nОтношение времени (top-down / bottom-up):" << endl;
    cout << "Serial:   " << speedup_serial << "x" << endl;
    cout << "Parallel: " << speedup_parallel << "x" << endl;
    
    return 0;
}