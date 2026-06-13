import time
import random
import sys
from collections import deque

def arrays(): 
    print("\nCписки")
    
    arr = [5, 2, 9, 1]
    print(f"Исходный массив: {arr}")
    print(f"Первый элемент: {arr[0]}")

    arr.append(7)
    print(f"После добавления 7: {arr}")
    arr.remove(9)
    print(f"После удаления 9: {arr}")
    
    # Перебор
    print("Перебор элементов:", end=" ")
    for x in arr:
        print(x, end=" ")
    print()


def sets():
    print("\nМножества")

    s = set()
    
    s.add(5)
    s.add(2)
    s.add(5) 
    print(f"Множество после добавления: {s}")
    
    s.update([1, 3, 7])
    print(f"После добавления [1,3,7]: {s}")
    
    if 2 in s:
        print("Элемент 2 найден")

    s.remove(2)
    print(f"После удаления 2: {s}")
    
    s2 = {3, 4, 5, 6}
    print(f"Объединение: {s.union(s2)}")
    print(f"Пересечение: {s.intersection(s2)}")


def dicts():
    print("\nСловари")
    
    d = {}
    
    d["apple"] = 5
    d["banana"] = 3
    d["cherry"] = 7
    print(f"Словарь: {d}")
    
    print(f"apple: {d['apple']}")
    
    print("Пары ключ-значение:", end=" ")
    for key, value in d.items():
        print(f"{key}:{value}", end=" ")
    print()
    
    if "banana" in d:
        print("banana найдена")
    
    del d["cherry"]
    print(f"После удаления cherry: {d}")
    
    print(f"orange: {d.get('orange', 'не найдено')}")


def queue():
    print("\nОчередь")
    
    dq = deque([10, 20, 30])
    print(f"Исходная очередь: {dq}")
    
    dq.append(40)
    print(f"После append(40): {dq}")
    
    dq.appendleft(5)
    print(f"После appendleft(5): {dq}")
    
    print(f"Первый элемент: {dq[0]}")
    print(f"Последний элемент: {dq[-1]}")
    
    left = dq.popleft()
    right = dq.pop()
    print(f"Удалили слева: {left}, справа: {right}")
    print(f"Очередь после удаления: {dq}")


def test():
    print("\nПроизводительность")
    size = 100000
    
    # Создаем коллекции
    lst = list(range(size))
    st = set(range(size))
    dct = {i: i for i in range(size)}
    dq = deque(range(size))
    
    # Память
    print("ПАМЯТЬ (байт):")
    print(f"  list:  {sys.getsizeof(lst):,}")
    print(f"  set:   {sys.getsizeof(st):,}")
    print(f"  dict:  {sys.getsizeof(dct):,}")
    print(f"  deque: {sys.getsizeof(dq):,}")
    
    # Поиск
    x = size - 1
    print("\nПОИСК (сек):")
    
    start = time.time()
    print(f"  list:  {x in lst} - {time.time()-start:.6f}")
    
    start = time.time()
    print(f"  set:   {x in st} - {time.time()-start:.6f}")
    
    start = time.time()
    print(f"  dict:  {x in dct} - {time.time()-start:.6f}")
    
    start = time.time()
    print(f"  deque: {x in dq} - {time.time()-start:.6f}")
    
    # Добавление
    new = size + 1
    print("\nДОБАВЛЕНИЕ (сек):")
    
    start = time.time()
    lst.append(new)
    print(f"  list:  {time.time()-start:.6f}")
    
    start = time.time()
    st.add(new)
    print(f"  set:   {time.time()-start:.6f}")
    
    start = time.time()
    dct[new] = new
    print(f"  dict:  {time.time()-start:.6f}")
    
    start = time.time()
    dq.append(new)
    print(f"  deque: {time.time()-start:.6f}")
    



def bubble_sort(arr):
    #Пузырьковая сортировка с оптимизацией
    n = len(arr)
    arr = arr.copy()  
    
    for i in range(n):
        swapped = False
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break

    return arr


def testbs():
    print("\nBubbleSort:")
    
    
    arr_random = [random.randint(1, 100) for _ in range(10)]
    print(f"Исходный: {arr_random}")
    sorted_arr = bubble_sort(arr_random)
    print(f"Отсортированный: {sorted_arr}")


def median_of_three(arr, low, high):
    
    #Вычисление медианы трех элементов (low, mid, high)
    #Для улучшения выбора опорного элемента в быстрой сортировке
    
    mid = (low + high) // 2
    if arr[low] > arr[mid]:
        arr[low], arr[mid] = arr[mid], arr[low]
    if arr[low] > arr[high]:
        arr[low], arr[high] = arr[high], arr[low]
    if arr[mid] > arr[high]:
        arr[mid], arr[high] = arr[high], arr[mid]
    return mid


def ninther(arr, low, high):
    # Tukey's ninther - выбор медианы из медиан трех групп по три элемента
    # Это улучшенный метод выбора опорного элемента для быстрой сортировки
    if high - low < 9:  # Если массив маленький, просто берем медиану трех
        return median_of_three(arr, low, high)
    step = (high - low) // 3
    m1 = median_of_three(arr, low, low + step)
    m2 = median_of_three(arr, low + step, low + 2 * step)
    m3 = median_of_three(arr, low + 2 * step, high)

    if arr[m1] > arr[m2]:
        m1, m2 = m2, m1
    if arr[m1] > arr[m3]:
        m1, m3 = m3, m1
    if arr[m2] > arr[m3]:
        m2, m3 = m3, m2
    return m2


def partition(arr, low, high, pivot_index):
    # Разбиение массива относительно опорного элемента
    pivot = arr[pivot_index]
    # Перемещаем опорный элемент в конец
    arr[pivot_index], arr[high] = arr[high], arr[pivot_index]
    
    i = low - 1
    
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    
    # Возвращаем опорный элемент на правильную позицию
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quicksort_ninther(arr, low, high):
    # Быстрая сортировка с использованием ninthe
    if low < high:
        # Выбираем опорный элемент с помощью ninther
        pivot_index = ninther(arr, low, high)
        
        # Разбиение
        pivot_final_index = partition(arr, low, high, pivot_index)
        
        # Рекурсивно сортируем части
        quicksort_ninther(arr, low, pivot_final_index - 1)
        quicksort_ninther(arr, pivot_final_index + 1, high)
    
    return arr


def quicksort_queue(arr):
    
    #Быстрая сортировка с использованием очереди (итеративная версия)
    #Использует очередь для обработки подмассивов вместо рекурсии
    
    if len(arr) <= 1:
        return arr
    
    arr = arr.copy()
    queue = deque()
    # Добавляем в очередь всю задачу
    queue.append((0, len(arr) - 1))
    
    while queue:
        low, high = queue.popleft()
        
        if low < high:
            # Используем медиану трех для выбора опорного элемента
            pivot_index = median_of_three(arr, low, high)
            pivot_final_index = partition(arr, low, high, pivot_index)
            
            # Добавляем подзадачи в очередь
            queue.append((low, pivot_final_index - 1))
            queue.append((pivot_final_index + 1, high))
    
    return arr


def quicksort_recursive(arr):
    
    #Обычная рекурсивная быстрая сортировка для сравнения
    
    if len(arr) <= 1:
        return arr
    
    arr = arr.copy()
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quicksort_recursive(left) + middle + quicksort_recursive(right)


def test_advanced_sorts():
    """Тестирование сложных алгоритмов сортировки"""
    print("\nQuickSort:")
    
    # Тестовые данные
    test_arrays = {
        "Массив": [random.randint(1, 100) for _ in range(10)]
    }
    
    for name, arr in test_arrays.items():
        print(f"\n{name}: {arr}")
        
        # Тест QuickSort с ninther
        sorted1 = quicksort_ninther(arr.copy(), 0, len(arr) - 1)
        print(f"  QuickSort с ninther: {sorted1}")
        
        # Тест QuickSort с очередью
        sorted2 = quicksort_queue(arr.copy())
        print(f"  QuickSort с очередью: {sorted2}")
        


def tests():
    #Сравнение производительности различных алгоритмов сортировки
    print("\nСравнение производительности:")
    
    sizes = [100, 500, 1000]
    results = {"bubble": [], "quicksort_ninther": [], "quicksort_queue": []}
    
    for size in sizes:
        # Генерируем случайный массив
        arr = [random.randint(1, 10000) for _ in range(size)]
        
        # Тест пузырьковой сортировки (только для маленьких массивов)
        if size <= 2000:
            arr_copy = arr.copy()
            start = time.time()
            bubble_sort(arr_copy)
            end = time.time()
            results["bubble"].append((end - start) * 1000)
        else:
            results["bubble"].append(None)
        
        # Тест быстрой сортировки с ninther
        arr_copy = arr.copy()
        start = time.time()
        quicksort_ninther(arr_copy, 0, len(arr_copy) - 1)
        end = time.time()
        results["quicksort_ninther"].append((end - start) * 1000)
        
        # Тест быстрой сортировки с очередью
        arr_copy = arr.copy()
        start = time.time()
        quicksort_queue(arr_copy)
        end = time.time()
        results["quicksort_queue"].append((end - start) * 1000)
        
        print(f"\nРазмер {size}:")
        if results["bubble"][-1]:
            print(f"  Пузырьковая: {results['bubble'][-1]:.2f} мс")
        print(f"  QuickSort (ninther): {results['quicksort_ninther'][-1]:.2f} мс")
        print(f"  QuickSort (queue): {results['quicksort_queue'][-1]:.2f} мс")
    
    return results, sizes



def main():
    
    #Работа с коллекциями
    arrays()
    sets()
    dicts()
    queue()
    test()
    
    # Часть 2: Пузырьковая сортировка
    testbs()
    
    # Часть 3: Сложные алгоритмы
    test_advanced_sorts()
    
    # Сравнение производительности
    results, sizes = tests()
    
    

if __name__ == "__main__":
    main()