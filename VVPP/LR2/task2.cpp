#include <iostream>
#include <cstdlib>
#include <ctime>
#include "omp.h"
using namespace std;

// Число вершин в результирующем дереве
int num_nodes = 0;
// Ограничиваем число создаваемых вершин
int low_limit_nodes = 150;
// Вероятность создания вершины-потомка (0,7)
int percent = 70;
// Для номеров вершин
int plus_num_node = 50;

// Вершина графа (дерева)
struct node
{
    struct node *left;
    struct node *right;
    int num;
};

// Создаем дерево
void tree_init(struct node *tree, int mode)
{
    static int loc_val;
    if (mode < 1)
        loc_val = 1;
    tree->num = loc_val++;
    tree->left = NULL;
    tree->right = NULL;
    
    if (loc_val > low_limit_nodes)
        return;
    
    // Потомок слева
    int n = rand() % 100;
    if (n < percent)
    {
        tree->left = new node;
        tree_init(tree->left, 1);
    }
    
    // Потомок справа
    n = rand() % 100;
    if (n < percent)
    {
        tree->right = new node;
        tree_init(tree->right, 1);
    }
}

// Имитируем обработку узла (вычисление факториала)
void work(int n)
{
    long long k = 1;  // используем long long для предотвращения переполнения
    int limit = (n * plus_num_node) * (n * plus_num_node);
    for(int i = 2; i <= limit; i++)
        k *= i;
}

// Обрабатываем узел (последовательная версия)
void node_process(struct node *tree)
{
    // Подсчитываем число узлов
    num_nodes++;
    
    // Связываем с каждым узлом какую-то работу
    work(tree->num);
    
    // Выводим номер узла, который обработали
    cout << "Обработан узел " << tree->num << endl;
    
    if (tree->left)
        node_process(tree->left);
    if (tree->right)
        node_process(tree->right);
}

int main()
{
    struct node tree;
    
    // Инициализируем дерево
    srand(time(NULL));
    tree_init(&tree, 0);
    
    double start;
    start = omp_get_wtime();
    
    node_process(&tree);
    
    cout << "Time is " << omp_get_wtime() - start << " seconds" << endl;
    cout << "Num_nodes = " << num_nodes << endl;
    
    return 0;
}