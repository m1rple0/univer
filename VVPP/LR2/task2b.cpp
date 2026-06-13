#include <iostream>
#include <cstdlib>
#include <ctime>
#include "omp.h"
using namespace std;

int num_nodes = 0;
int low_limit_nodes = 150;
int percent = 70;
int plus_num_node = 50;

struct node {
    struct node *left;
    struct node *right;
    int num;
};

void tree_init(struct node *tree, int mode) {
    static int loc_val;
    if (mode < 1) loc_val = 1;
    tree->num = loc_val++;
    tree->left = NULL;
    tree->right = NULL;
    if (loc_val > low_limit_nodes) return;
    
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
    int k = 1;
    for(int i = 2; i <= (n * plus_num_node) * (n * plus_num_node); i++)
        k *= i;
}

void node_process(struct node *tree) {
    num_nodes++;
    work(tree->num);
    cout << tree->num << endl;
    if (tree->left) node_process(tree->left);
    if (tree->right) node_process(tree->right);
}

void node_process_parallel(struct node *tree) {
    #pragma omp atomic
    num_nodes++;
    
    work(tree->num);
    
    #pragma omp critical
    cout << tree->num << " thr=" << omp_get_thread_num() << endl;
    
    #pragma omp task
    if (tree->left) node_process_parallel(tree->left);
    #pragma omp task
    if (tree->right) node_process_parallel(tree->right);
}

int main() {
    struct node tree;
    srand(time(NULL));
    tree_init(&tree, 0);
    
    double start = omp_get_wtime();
    node_process(&tree);
    double time1 = omp_get_wtime() - start;
    
    num_nodes = 0;
    start = omp_get_wtime();
    #pragma omp parallel
    {
        #pragma omp single
        {
            node_process_parallel(&tree);
        }
    }
    double time2 = omp_get_wtime() - start;
    
    cout << "Serial time: " << time1 << " sec, nodes=" << num_nodes << endl;
    cout << "Parallel time: " << time2 << " sec" << endl;
    return 0;
}