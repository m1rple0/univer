#include <iostream>
#include <cstdlib>
#include "omp.h"
using namespace std;

int main()
{
    int p = 1;
    #pragma omp parallel shared(p)
    {
        #pragma omp single
        {
            cout << "Single - " << omp_get_thread_num() << endl;
            while (p)
            {
                #pragma omp task
                {
                    int n = rand() % 100;
                    #pragma omp critical
                    {
                        if (n < 50 && p == 1)
                        {
                            p = 0;
                            cout << "Finished by " << omp_get_thread_num() << endl;
                        }
                    }
                    cout << omp_get_thread_num() << ": n=" << n << endl;
                }
            }
        }
    }
    return 0;
}