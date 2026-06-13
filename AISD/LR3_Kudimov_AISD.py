import time
import random
from functools import lru_cache

#  Бинарный поиск
def linear_find(arr, x):
    for i in range(len(arr)):
        if arr[i] == x:
            return i
    return -1

def binary_find(arr, x):
    l = 0
    r = len(arr) - 1
    while l <= r:
        m = (l + r) // 2
        if arr[m] == x:
            return m
        elif arr[m] < x:
            l = m + 1
        else:
            r = m - 1
    return -1

def real_binary_search(f, a, b, eps=1e-7): # вещественный БП
    for _ in range(100):
        c = (a + b) / 2
        if abs(f(c)) < eps or (b - a) < eps:
            return c
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2


def first_occurrence(arr, x): # целочисоенный БП поиск первого
    l = 0
    r = len(arr)
    while l < r:
        m = (l + r) // 2
        if arr[m] < x:
            l = m + 1
        else:
            r = m
    return l if l < len(arr) and arr[l] == x else -1


def last_occurrence(arr, x):  # целочисоенный БП поиск последнего
    l = 0
    r = len(arr)
    while l < r:
        m = (l + r) // 2
        if arr[m] <= x:
            l = m + 1
        else:
            r = m
    return l - 1 if l > 0 and arr[l - 1] == x else -1


import time

def performance_comparison():
    sizes = [1000, 10000, 100000, 500000]
    iterations = 10000
    print(f"Количество запусков на каждый размер: {iterations}\n")
    
    print(f"{'Размер':<12} {'Классический':<15} {'Первый':<15} {'Последний':<15} {'Вещественный':<15}")
  
    results = []
    
    for size in sizes:
        arr = list(range(size))  # отсортированный массив
        f = lambda x: x**2 - 2
        
        # 1. Классический
        start = time.perf_counter()
        for _ in range(iterations):
            binary_find(arr, size // 2)
        t1 = time.perf_counter() - start
        
        # 2. Первое вхождение
        start = time.perf_counter()
        for _ in range(iterations):
            first_occurrence(arr, size // 2)
        t2 = time.perf_counter() - start
        
        # 3. Последнее вхождение
        start = time.perf_counter()
        for _ in range(iterations):
            last_occurrence(arr, size // 2)
        t3 = time.perf_counter() - start
        
        # 4. Вещественный (не зависит от размера)
        start = time.perf_counter()
        for _ in range(iterations):
            real_binary_search(f, 1, 2)
        t4 = time.perf_counter() - start
        
        results.append((size, t1, t2, t3, t4))
        
        print(f"{size:<12} {t1:<15.4f} {t2:<15.4f} {t3:<15.4f} {t4:<15.4f}")
    

    base_time = results[0][1]  # время на минимальном размере
    for size, t1, t2, t3, _ in results:
        print(f"{size:<12} {t1/base_time:<15.2f} {t2/base_time:<15.2f} {t3/base_time:<15.2f}")
    
   
def fib_recursive(n):
    if n <= 1:
        return n
    return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_iterative(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a


@lru_cache(maxsize=None)
def fib_recursive_cached(n):
    if n <= 1:
        return n
    return fib_recursive_cached(n - 1) + fib_recursive_cached(n - 2)


fib_cache = {}
def fib_iterative_cached(n):
    if n in fib_cache:
        return fib_cache[n]
    a, b = 0, 1
    for i in range(n + 1):
        if i == n:
            fib_cache[n] = a
            return a
        a, b = b, a + b


def fib_demo():
    print("\n Числа Фибоначчи ")
    nums = [10, 20, 30, 35]
    for n in nums:
        print(f"\nF({n}):")
        
        t1 = time.perf_counter()
        r1 = fib_iterative(n)
        t2 = time.perf_counter()
        print(f"  итеративно           {r1} ({t2 - t1:.6f} с)")

        t1 = time.perf_counter()
        r1 = fib_iterative_cached(n)
        t2 = time.perf_counter()
        print(f"  итеративно с кешем   {r1} ({t2 - t1:.6f} с)")


        t1 = time.perf_counter()
        r2 = fib_recursive_cached(n)
        t2 = time.perf_counter()
        print(f"  рекурсивно с кешем   {r2} ({t2 - t1:.6f} с)")

        if n <= 30:
            t1 = time.perf_counter()
            r3 = fib_recursive(n)
            t2 = time.perf_counter()
            print(f"  рекурсивно без кеша  {r3} ({t2 - t1:.6f} с)")


# 3. Префиксные суммы и суффиксные суммы

def build_prefix_n1(a):
    p = [0] * (len(a) + 1)
    for i in range(len(a)):
        p[i + 1] = p[i] + a[i]
    return p


def build_prefix_n(a):
    p = a.copy()
    for i in range(1, len(p)):
        p[i] += p[i - 1]
    return p


def prefix_sum_query_n1(p, l, r):
    return p[r + 1] - p[l]


def prefix_sum_query_n(p, l, r):
    if l == 0:
        return p[r]
    return p[r] - p[l - 1]


def max_prefix(a):
    cur = 0
    best = float('-inf')
    for v in a:
        cur += v
        if cur > best:
            best = cur
    return best


def build_suffix(a):
    s = [0] * (len(a) + 1)
    for i in range(len(a) - 1, -1, -1):
        s[i] = s[i + 1] + a[i]
    return s


def suffix_sum_query(s, l, r):
    return s[l] - s[r + 1]


def max_suffix(a):
    cur = 0
    best = float('-inf')
    for v in reversed(a):
        cur += v
        if cur > best:
            best = cur
    return best


def prefix_suffix_demo():
    print("\n Префиксные и суффиксные суммы")
    a = [3, -1, 4, 2, -5, 6]
    print("Массив:", a)

    p1 = build_prefix_n1(a)
    p2 = build_prefix_n(a)
    print("Префиксные суммы (n+1):", p1)
    print("Префиксные суммы (n):  ", p2)

    queries = [(0, 2), (1, 4), (2, 5)]
    print("\nЗапросы сумм подотрезков:")
    for l, r in queries:
        s1 = prefix_sum_query_n1(p1, l, r)
        s2 = prefix_sum_query_n(p2, l, r)
        print(f"  [{l}, {r}] -> {s1} (через n+1), {s2} (через n)")

    print("\nМаксимальная сумма на префиксе:", max_prefix(a))

    s = build_suffix(a)
    print("Суффиксные суммы:", s[:-1])
    for l, r in queries:
        print(f"  [{l}, {r}] через суффиксы: {suffix_sum_query(s, l, r)}")
    print("Максимальная сумма на суффиксе:", max_suffix(a))


# 4. Рюкзак (с повторениями)

def knapsack_unbounded(w, v, cap):
    dp = [0] * (cap + 1)
    choice = [[] for _ in range(cap + 1)]
    for c in range(1, cap + 1):
        for i in range(len(w)):
            if w[i] <= c:
                new_val = dp[c - w[i]] + v[i]
                if new_val > dp[c]:
                    dp[c] = new_val
                    choice[c] = choice[c - w[i]] + [i]
    return dp[cap], choice[cap]


def knapsack_demo():
    print("\n Рюкзак с повторениями")
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 8]
    capacity = 10

    print("Веса:", weights)
    print("Ценности:", values)
    print("Вместимость:", capacity)

    total_val, items = knapsack_unbounded(weights, values, capacity)
    print(f"Максимальная ценность: {total_val}")
    print("Выбранные предметы (индексы):", items)
    print("Итоговый вес:", sum(weights[i] for i in items))


# 5. макс общ последовательность lcs

def lcs(s1, s2):
    n = len(s1)
    m = len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # восстановление
    i, j = n, m
    seq = []
    while i > 0 and j > 0:
        if s1[i - 1] == s2[j - 1]:
            seq.append(s1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] > dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    return dp[n][m], ''.join(reversed(seq))


def lcs_demo():
    print("\n Наибольшая общая подпоследовательность ")
    a = "AGGTAB"
    b = "GXTXAYB"
    print(f"A = {a}")
    print(f"B = {b}")

    length, seq = lcs(a, b)
    print(f"Длина LCS: {length}")
    print(f"Последовательность: {seq}")

    # дополнительные примеры
    print("\nДругие примеры:")
    for x, y in [("ABC", "AC"), ("ABCD", "AXBXD"), ("abcde", "ace")]:
        ln, s = lcs(x, y)
        print(f"  LCS('{x}', '{y}') = {ln} ('{s}')")

def main():
    print("Лабораторная работа №3")
    performance_comparison()
    fib_demo()
    prefix_suffix_demo()
    knapsack_demo()
    lcs_demo()

if __name__ == "__main__":
    main()