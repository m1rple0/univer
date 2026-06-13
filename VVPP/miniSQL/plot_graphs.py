import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# НАСТРОЙКИ 
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# даннеы

# Загрузка OpenMP
print("Загрузка OpenMP...")
df_openmp = pd.read_csv('results_openmp.csv')

# Загрузка MPI
print("Загрузка MPI...")
df_mpi = pd.read_csv('results_mpi.csv')

# Для OpenMP берём лучший результат (максимальное ускорение) для каждого N и threads
best_openmp = df_openmp.loc[df_openmp.groupby(['N', 'threads'])['speedup'].idxmax()]

print("Данные загружены успешно!\n")

# openmp
print("Строим графики OpenMP...")

plt.figure(figsize=(10, 6))

for N in best_openmp['N'].unique():
    data = best_openmp[best_openmp['N'] == N]
    N_million = int(N / 1000000)
    plt.plot(data['threads'], data['speedup'], 'o-', 
             label=f'N = {N_million}M', linewidth=2, markersize=8)

threads_max = best_openmp['threads'].max()
plt.plot([1, threads_max], [1, threads_max], 'k--', 
         label='Идеальное ускорение', linewidth=1.5, alpha=0.7)

plt.xlabel('Количество потоков', fontsize=12)
plt.ylabel('Ускорение', fontsize=12)
plt.title('OpenMP: Ускорение от количества потоков', fontsize=14)
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graph_openmp_speedup.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ graph_openmp_speedup.png")


plt.figure(figsize=(10, 6))

for N in best_openmp['N'].unique():
    data = best_openmp[best_openmp['N'] == N]
    N_million = int(N / 1000000)
    plt.plot(data['threads'], data['efficiency'], 'o-', 
             label=f'N = {N_million}M', linewidth=2, markersize=8)

plt.plot([1, threads_max], [1, 1], 'k--', 
         label='Идеальная эффективность', linewidth=1.5, alpha=0.7)

plt.xlabel('Количество потоков', fontsize=12)
plt.ylabel('Эффективность', fontsize=12)
plt.title('OpenMP: Эффективность от количества потоков', fontsize=14)
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graph_openmp_efficiency.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ graph_openmp_efficiency.png")

plt.figure(figsize=(12, 7))

for threads in [2, 4, 8]:
    data_chunk = df_openmp[(df_openmp['threads'] == threads) & 
                            (df_openmp['N'] == 100000000)]
    if not data_chunk.empty:
        data_chunk = data_chunk.sort_values('chunk_size')
        chunk_labels = ['авто' if x == 0 else str(x) for x in data_chunk['chunk_size']]
        plt.plot(range(len(data_chunk)), data_chunk['speedup'], 'o-', 
                 label=f'{threads} потоков', linewidth=2, markersize=8)

plt.xticks(range(len(chunk_labels)), chunk_labels)
plt.xlabel('Размер блока (chunk_size)', fontsize=12)
plt.ylabel('Ускорение', fontsize=12)
plt.title('OpenMP: Влияние размера блока на ускорение (N = 100M)', fontsize=14)
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graph_chunk_size.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ graph_chunk_size.png")

#mpi
print("\nСтроим графики MPI...")

plt.figure(figsize=(10, 6))

for N in df_mpi['N'].unique():
    data = df_mpi[df_mpi['N'] == N]
    N_million = int(N / 1000000)
    plt.plot(data['processes'], data['speedup'], 'o-', 
             label=f'N = {N_million}M', linewidth=2, markersize=8)

proc_max = df_mpi['processes'].max()
plt.plot([1, proc_max], [1, proc_max], 'k--', 
         label='Идеальное ускорение', linewidth=1.5, alpha=0.7)

plt.xlabel('Количество процессов', fontsize=12)
plt.ylabel('Ускорение', fontsize=12)
plt.title('MPI: Ускорение от количества процессов', fontsize=14)
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graph_mpi_speedup.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ graph_mpi_speedup.png")


plt.figure(figsize=(10, 6))

for N in df_mpi['N'].unique():
    data = df_mpi[df_mpi['N'] == N]
    N_million = int(N / 1000000)
    efficiency = data['speedup'] / data['processes']
    plt.plot(data['processes'], efficiency, 'o-', 
             label=f'N = {N_million}M', linewidth=2, markersize=8)

plt.plot([1, proc_max], [1, 1], 'k--', 
         label='Идеальная эффективность', linewidth=1.5, alpha=0.7)

plt.xlabel('Количество процессов', fontsize=12)
plt.ylabel('Эффективность', fontsize=12)
plt.title('MPI: Эффективность от количества процессов', fontsize=14)
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graph_mpi_efficiency.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ graph_mpi_efficiency.png")

#sravnenie
print("\nСтроим сравнительные графики...")

plt.figure(figsize=(10, 6))

N_compare = 100000000

openmp_100M = best_openmp[best_openmp['N'] == N_compare]
mpi_100M = df_mpi[df_mpi['N'] == N_compare]

if not openmp_100M.empty and not mpi_100M.empty:
    plt.plot(openmp_100M['threads'], openmp_100M['speedup'], 'ro-', 
             label='OpenMP', linewidth=2, markersize=8)
    plt.plot(mpi_100M['processes'], mpi_100M['speedup'], 'bs-', 
             label='MPI', linewidth=2, markersize=8)

plt.plot([1, 8], [1, 8], 'k--', 
         label='Идеальное ускорение', linewidth=1.5, alpha=0.7)

plt.xlabel('Количество потоков/процессов', fontsize=12)
plt.ylabel('Ускорение', fontsize=12)
plt.title('Сравнение OpenMP и MPI (N = 100M)', fontsize=14)
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graph_comparison_speedup.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ graph_comparison_speedup.png")

plt.figure(figsize=(10, 6))

if not openmp_100M.empty and not mpi_100M.empty:
    openmp_efficiency = openmp_100M['efficiency']
    mpi_efficiency = mpi_100M['speedup'] / mpi_100M['processes']
    
    plt.plot(openmp_100M['threads'], openmp_efficiency, 'ro-', 
             label='OpenMP', linewidth=2, markersize=8)
    plt.plot(mpi_100M['processes'], mpi_efficiency, 'bs-', 
             label='MPI', linewidth=2, markersize=8)

plt.plot([1, 8], [1, 1], 'k--', 
         label='Идеальная эффективность', linewidth=1.5, alpha=0.7)

plt.xlabel('Количество потоков/процессов', fontsize=12)
plt.ylabel('Эффективность', fontsize=12)
plt.title('Сравнение эффективности OpenMP и MPI (N = 100M)', fontsize=14)
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('graph_comparison_efficiency.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ graph_comparison_efficiency.png")

print("\nСтроим график зависимости эффективности MPI от размерности задачи...")

plt.figure(figsize=(12, 7))

# Группируем по количеству процессов
for processes in df_mpi['processes'].unique():
    if processes == 1:
        continue  # Пропускаем 1 процесс (эффективность всегда 1)
    
    data_proc = df_mpi[df_mpi['processes'] == processes]
    if not data_proc.empty:
        data_proc = data_proc.sort_values('N')
        N_in_millions = data_proc['N'] / 1000000
        efficiency = data_proc['speedup'] / processes
        
        plt.plot(N_in_millions, efficiency, 'o-', 
                 label=f'{processes} процессов', linewidth=2, markersize=8)

plt.plot([10, 200], [1, 1], 'k--', 
         label='Идеальная эффективность', linewidth=1.5, alpha=0.7)

plt.xlabel('Размер задачи N (миллионов)', fontsize=12)
plt.ylabel('Эффективность', fontsize=12)
plt.title('MPI: Зависимость эффективности от размерности задачи', fontsize=14)
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.xscale('log')  # Логарифмическая шкала для лучшей читаемости
plt.tight_layout()
plt.savefig('graph_mpi_efficiency_vs_problem_size.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ graph_mpi_efficiency_vs_problem_size.png")
\
print("\nСтроим график зависимости эффективности OpenMP от размерности задачи...")

plt.figure(figsize=(12, 7))

for threads in best_openmp['threads'].unique():
    if threads == 1:
        continue
    
    data_thread = best_openmp[best_openmp['threads'] == threads]
    if not data_thread.empty:
        data_thread = data_thread.sort_values('N')
        N_in_millions = data_thread['N'] / 1000000
        
        plt.plot(N_in_millions, data_thread['efficiency'], 'o-', 
                 label=f'{threads} потоков', linewidth=2, markersize=8)

plt.plot([10, 200], [1, 1], 'k--', 
         label='Идеальная эффективность', linewidth=1.5, alpha=0.7)

plt.xlabel('Размер задачи N (миллионов)', fontsize=12)
plt.ylabel('Эффективность', fontsize=12)
plt.title('OpenMP: Зависимость эффективности от размерности задачи', fontsize=14)
plt.legend(loc='best')
plt.grid(True, alpha=0.3)
plt.xscale('log')
plt.tight_layout()
plt.savefig('graph_openmp_efficiency_vs_problem_size.png', dpi=150, bbox_inches='tight')
plt.close()
print("  ✓ graph_openmp_efficiency_vs_problem_size.png")




#result

print("\n--- ЛУЧШИЕ РЕЗУЛЬТАТЫ OPENMP ---")
for N in best_openmp['N'].unique():
    data = best_openmp[best_openmp['N'] == N]
    best_idx = data['speedup'].idxmax()
    best_row = data.loc[best_idx]
    N_million = int(N / 1000000)
    print(f"N = {N_million}M: max speedup = {best_row['speedup']:.2f}x "
          f"(threads={best_row['threads']}, chunk={int(best_row['chunk_size']) if best_row['chunk_size']!=0 else 'auto'})")

print("\n--- ЛУЧШИЕ РЕЗУЛЬТАТЫ MPI ---")
for N in df_mpi['N'].unique():
    data = df_mpi[df_mpi['N'] == N]
    best_idx = data['speedup'].idxmax()
    best_row = data.loc[best_idx]
    N_million = int(N / 1000000)
    print(f"N = {N_million}M: max speedup = {best_row['speedup']:.2f}x "
          f"(processes={best_row['processes']})")

print("\n--- ЭФФЕКТИВНОСТЬ MPI ПРИ РАЗНЫХ РАЗМЕРАХ ЗАДАЧИ ---")
for processes in df_mpi['processes'].unique():
    if processes == 1:
        continue
    print(f"\n{processes} процессов:")
    for N in df_mpi['N'].unique():
        data = df_mpi[(df_mpi['processes'] == processes) & (df_mpi['N'] == N)]
        if not data.empty:
            eff = data['speedup'].values[0] / processes
            N_million = int(N / 1000000)
            print(f"  N = {N_million}M: эффективность = {eff:.3f} ({eff*100:.1f}%)")
