import time
import random
import math
import sys
from collections import deque

def ymnojenie(A, B):
    """
    Обычное умножение матриц O(n³)
    """
    n = len(A)
    C = [[0] * n for _ in range(n)]
    
    for i in range(n):
        for k in range(n):
            aik = A[i][k]
            for j in range(n):
                C[i][j] += aik * B[k][j]
    return C


def matrix_add(A, B):
    """Сложение матриц"""
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]


def matrix_sub(A, B):
    """Вычитание матриц"""
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]


def strassen(A, B):
    """
    Алгоритм Штрассена для умножения матриц
    Асимптотика O(n^log2(7)) ≈ O(n^2.81)
    """
    n = len(A)
    
    if n <= 64:
        return ymnojenie(A, B)
    
    if n % 2 != 0:
        A = [row + [0] for row in A] + [[0] * (n + 1)]
        B = [row + [0] for row in B] + [[0] * (n + 1)]
        n += 1
    
    m = n // 2
    
    a11 = [row[:m] for row in A[:m]]
    a12 = [row[m:] for row in A[:m]]
    a21 = [row[:m] for row in A[m:]]
    a22 = [row[m:] for row in A[m:]]
    
    b11 = [row[:m] for row in B[:m]]
    b12 = [row[m:] for row in B[:m]]
    b21 = [row[:m] for row in B[m:]]
    b22 = [row[m:] for row in B[m:]]
    
    p1 = strassen(matrix_add(a11, a22), matrix_add(b11, b22))
    p2 = strassen(matrix_add(a21, a22), b11)
    p3 = strassen(a11, matrix_sub(b12, b22))
    p4 = strassen(a22, matrix_sub(b21, b11))
    p5 = strassen(matrix_add(a11, a12), b22)
    p6 = strassen(matrix_sub(a21, a11), matrix_add(b11, b12))
    p7 = strassen(matrix_sub(a12, a22), matrix_add(b21, b22))
    
    c11 = matrix_add(matrix_sub(matrix_add(p1, p4), p5), p7)
    c12 = matrix_add(p3, p5)
    c21 = matrix_add(p2, p4)
    c22 = matrix_add(matrix_sub(matrix_add(p1, p3), p2), p6)
    
    result = []
    for i in range(m):
        result.append(c11[i] + c12[i])
    for i in range(m):
        result.append(c21[i] + c22[i])
    
    return result


def generate_matrix(n):
    return [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]


def test1():
    n = 4
    A = generate_matrix(n)
    B = generate_matrix(n)
    
    print(f"\nМатрица A ({n}x{n}):")
    for row in A:
        print(f"  {row}")
    
    print(f"\nМатрица B ({n}x{n}):")
    for row in B:
        print(f"  {row}")
    
    C_naive = ymnojenie(A, B)
    print(f"\nРезультат обычного умножения:")
    for row in C_naive:
        print(f"  {row}")
    
    C_strassen = strassen(A, B)
    print(f"\nРезультат Штрассена:")
    for row in C_strassen:
        print(f"  {row}")


def test1_proizvoditelnost():
    print("\nПроизводительность:")
    
    sizes = [32, 64, 128]
    print("\nРазмер | Наивный (мс) | Штрассен (мс) | Ускорение")
    
    for n in sizes:
        A = generate_matrix(n)
        B = generate_matrix(n)
        
        start = time.time()
        ymnojenie(A, B)
        time_naive = (time.time() - start) * 1000
        
        start = time.time()
        strassen(A, B)
        time_strassen = (time.time() - start) * 1000
        
        speedup = time_naive / time_strassen if time_strassen > 0 else 0
        
        print(f"{n:5d} | {time_naive:11.2f} | {time_strassen:11.2f} | {speedup:8.2f}x")
    
    print("\nАсимптотическая оценка:")
    print("  Наивный метод:      O(n³)")
    print("  Алгоритм Штрассена: O(n^log2(7)) ≈ O(n^2.81)")

def euclidean(a, b):
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a
def extended_euclidean(a, b):
    if b == 0:
        return a, 1, 0
    gcd, x1, y1 = extended_euclidean(b, a % b)
    return gcd, y1, x1 - (a // b) * y1


def test_euclidean():
    print("\nАлгоритм Евклида для нахождения НОД:")
    
    test_pairs = [(48, 18), (100, 35), (1071, 462), (123456, 789012), (17, 19)]
    
    print("\nЧисло a | Число b | НОД | Представление a*x + b*y = НОД")
    print("-" * 55)
    
    for a, b in test_pairs:
        gcd = euclidean(a, b)
        gcd_ext, x, y = extended_euclidean(a, b)
        print(f"{a:7d} | {b:7d} | {gcd:3d} | {a}*{x} + {b}*{y} = {gcd_ext}")


def eratosthenes(limit):
    if limit < 2:
        return []
    
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(limit ** 0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    
    return [i for i, prime in enumerate(is_prime) if prime]


def test_erato():
    print("\n Решето эратосфена")
    
    for limit in [10, 50, 100]:
        primes = eratosthenes(limit)
        print(f"\nПростые числа до {limit}: {primes}")
    
    print("\nСравнение производительности:")
    print("Limit     | Время (мс) | Кол-во простых")
    print("-" * 40)
    
    for limit in [10000, 100000, 500000]:
        start = time.time()
        primes = eratosthenes(limit)
        elapsed = (time.time() - start) * 1000
        print(f"{limit:8d} | {elapsed:9.2f} | {len(primes):14d}")


def moneti(amount):
    # Выдача сдачи жадным алгоритмом 
    coins = [50, 10, 5, 2, 1]
    result = {}
    remaining = amount
    
    for coin in coins:
        if remaining >= coin:
            count = remaining // coin
            result[coin] = count
            remaining -= coin * count
    return result if remaining == 0 else None


def activity_selection(activities):
    # Выбор максимального количества непересекающихся активов
    sorted_activities = sorted(activities, key=lambda x: x[1])
    selected = []
    last_end = -1
    
    for start, end in sorted_activities:
        if start >= last_end:
            selected.append((start, end))
            last_end = end
    
    return selected


def zadacha (items, capacity):
    # Задача о рюкзак
    items_sorted = sorted(items, key=lambda x: x[0]/x[1], reverse=True)
    total_value = 0
    remaining = capacity
    result = []
    
    for value, weight in items_sorted:
        if remaining >= weight:
            result.append((value, weight, 1.0))
            total_value += value
            remaining -= weight
        else:
            fraction = remaining / weight
            result.append((value, weight, fraction))
            total_value += value * fraction
            break
    
    return total_value, result


def test_greedy():
    print("\nЖадные алгоритмы:")
    print("\n1. Выдача сдачи:")
    for amount in [89, 37, 100, 63]:
        change = moneti(amount)
        print(f"   {amount} руб. = ", end="")
        for coin, cnt in sorted(change.items(), reverse=True):
            print(f"{cnt}×{coin}р ", end="")
        print()
    print("\n2. Выбор активов (максимизация количества):")
    activities = [(1,4), (3,5), (0,6), (5,7), (3,8), (5,9), (6,10), (8,11), (8,12), (2,13), (12,14)]
    selected = activity_selection(activities)
    print(f"   Всего активов: {len(activities)}")
    print(f"   Выбрано: {len(selected)}")
    print(f"   Выбранные интервалы: {selected}")
    
    # Дробный рюкзак
    print("\n3. Дробная задача о рюкзаке:")
    items = [(60, 10), (100, 20), (120, 30)]
    capacity = 50
    total_value, selected_items = zadacha(items, capacity)
    print(f"   Предметы (ценность, вес): {items}")
    print(f"   Вместимость: {capacity}")
    print(f"   Максимальная ценность: {total_value}")
    for value, weight, fraction in selected_items:
        print(f"     Ценность {value}, вес {weight}, взято {fraction:.0%}")


def givens_rotation_qr(A):
    import copy
    
    A = copy.deepcopy(A)
    m = len(A)
    n = len(A[0])
    
    Q = [[1.0 if i == j else 0.0 for j in range(m)] for i in range(m)]
    
    for j in range(n):
        for i in range(m-1, j, -1):
            if abs(A[i][j]) < 1e-10:
                continue
            
            r = math.hypot(A[i-1][j], A[i][j])
            c = A[i-1][j] / r
            s = A[i][j] / r
            
            for k in range(j, n):
                temp = c * A[i-1][k] + s * A[i][k]
                A[i][k] = -s * A[i-1][k] + c * A[i][k]
                A[i-1][k] = temp
            
            for k in range(m):
                temp = c * Q[i-1][k] + s * Q[i][k]
                Q[i][k] = -s * Q[i-1][k] + c * Q[i][k]
                Q[i-1][k] = temp
    
    Q = [[Q[j][i] for j in range(m)] for i in range(m)]
    return Q, A


def qr():
    print("\nQR методом гивенса:")
    
    A = [
        [12, -51, 4],
        [6, 167, -68],
        [-4, 24, -41]
    ]
    
    print("\nИсходная матрица A:")
    for row in A:
        print(f"  {row}")
    
    Q, R = givens_rotation_qr(A)
    
    print("\nМатрица Q (ортогональная):")
    for row in Q:
        print(f"  {[round(x, 4) for x in row]}")
    
    print("\nМатрица R (верхнетреугольная):")
    for row in R:
        print(f"  {[round(x, 4) for x in row]}")
    
    # Проверка Q * R = A
    n = len(A)
    QR = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                QR[i][j] += Q[i][k] * R[k][j]
    
    print("\nПроверка Q * R:")
    for row in QR:
        print(f"  {[round(x, 4) for x in row]}")


def main():
    test1()
    test1_proizvoditelnost()
    test_euclidean()
    test_erato()
    test_greedy()
    qr()
    

if __name__ == "__main__":
    main()