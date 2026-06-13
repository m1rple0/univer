import numpy as np
import random
import math

def cauchy_gen_point(x0, T, p_min=None, p_max=None):
    delta = T * np.tan(np.pi * (np.random.rand(x0.size) - 0.5))
    return x0 + delta

def quenching_gen_point(x0, T, p_min=None, p_max=None):
    if p_min is None:
        p_min = np.array([-1e8 for i in range(x0.size)])
    if p_max is None:
        p_max = np.array([1e8 for i in range(x0.size)])
    
    components = []
    for i in range(x0.size):
        a = random.random()
        if a > 0.5:
            sign_a = 1
        elif a < 0.5:
            sign_a = -1
        else:
            sign_a = 0
        z = sign_a * T * ((1 + 1 / T) ** abs(2 * a - 1) - 1)
        components.append((p_max[i] - p_min[i]) * z)
    return x0 + np.array(components)

def cauchy_temperature_func(i, T0, n=None):
    return T0 / i

def quenching_temperature_func(i, T0, n, m=1, p=1):
    c = m * math.exp(-p / n)
    return T0 * math.exp(-c * i ** (1 / n))

def imitation_firing(energy_func, temperature_func, generate_point_func, x0, T0, p_min=None, p_max=None, T_min=0, max_iters_num=1000):
    i = 1
    T = T0
    x_opt = x0
    f_opt = energy_func(x0)
    while i <= max_iters_num and T > T_min:
        if i > 1:
            T = temperature_func(i, T0, x0.size)
        i += 1
        x1 = generate_point_func(x0, T, p_min, p_max)
        if not (p_min is None) or not (p_max is None):
            while True:
                flag = True
                for j in range(x1.size):
                    if not (p_min is None) and x1[j] < p_min[j]:
                        flag = False
                    if not (p_max is None) and x1[j] > p_max[j]:
                        flag = False
                if flag:
                    break
                x1 = generate_point_func(x0, T, p_min, p_max)
        if energy_func(x1) < f_opt:
            x0 = x1
            x_opt = x0
            f_opt = energy_func(x0)
            continue
        else:
            hibbs_p = math.exp((energy_func(x0) - energy_func(x1)) / T)
            if random.random() <= hibbs_p:
                x0 = x1
    return x_opt, i

# Тестовые функции
def schaffer_n4(x):
    return 0.5 + (math.cos(math.sin(abs(x[0]**2 - x[1]**2)))**2 - 0.5) / (1 + 0.001 * (x[0]**2 + x[1]**2))**2

def holder_table(x):
    return -abs(math.sin(x[0]) * math.cos(x[1]) * math.exp(abs(1 - math.sqrt(x[0]**2 + x[1]**2) / math.pi)))

def easom(x):
    return -math.cos(x[0]) * math.cos(x[1]) * math.exp(- (x[0] - math.pi)**2 - (x[1] - math.pi)**2)

if __name__ == "__main__":
    print("=" * 50)
    print("МЕТОД ИМИТАЦИИ ОТЖИГА - ДЕМО")
    print("=" * 50)
    
    # Выбор функции
    print("\nВыберите функцию:")
    print("1. Функция Шафера №4")
    print("2. Табличная функция Хольдера")
    print("3. Функция Изома")
    
    func_choice = int(input("Введите номер (1-3): "))
    
    if func_choice == 1:
        func = schaffer_n4
        bounds = [(-100, 100), (-100, 100)]
        print("Выбрана: Функция Шафера №4")
    elif func_choice == 2:
        func = holder_table
        bounds = [(-10, 10), (-10, 10)]
        print("Выбрана: Табличная функция Хольдера")
    else:
        func = easom
        bounds = [(-100, 100), (-100, 100)]
        print("Выбрана: Функция Изома")
    
    # Выбор метода
    print("\nВыберите метод отжига:")
    print("1. Отжиг Коши")
    print("2. Метод тушения")
    
    method_choice = int(input("Введите номер (1-2): "))
    
    if method_choice == 1:
        gen_func = cauchy_gen_point
        temp_func = cauchy_temperature_func
        print("Выбран: Отжиг Коши")
    else:
        gen_func = quenching_gen_point
        temp_func = quenching_temperature_func
        print("Выбран: Метод тушения")
    
    # Ввод параметров
    x0_input = input("\nВведите начальную точку: ")
    x0 = np.array([float(val) for val in x0_input.split()])
    
    T0 = float(input("Введите начальную температуру: "))
    T_min = float(input("Введите минимальную температуру (по умолчанию 0.001): ") or "0.001")
    max_iters = int(input("Введите максимум итераций (по умолчанию 1000): ") or "1000")
    
    # Настройка границ
    use_default_bounds = (input(f"\nИспользовать стандартные границы {bounds}? (y/n): ") or "y").lower() == 'y'
    
    if use_default_bounds:
        p_min = np.array([b[0] for b in bounds])
        p_max = np.array([b[1] for b in bounds])
    else:
        print("\nВведите границы для каждой координаты:")
        p_min = np.zeros(2)
        p_max = np.zeros(2)
        for i in range(2):
            p_min[i] = float(input(f"Минимум для x[{i}]: "))
            p_max[i] = float(input(f"Максимум для x[{i}]: "))
    
    # Запуск алгоритма
    print("\n" + "=" * 50)
    print("Запуск алгоритма...")
    print("=" * 50)
    
    x_result, iterations = imitation_firing(
        energy_func=func,
        temperature_func=temp_func,
        generate_point_func=gen_func,
        x0=x0,
        T0=T0,
        p_min=p_min,
        p_max=p_max,
        T_min=T_min,
        max_iters_num=max_iters
    )
    
    # Результаты
    print("\nРЕЗУЛЬТАТЫ:")
    print("-" * 50)
    print(f"Найденная точка: {x_result}")
    print(f"Значение функции: {func(x_result)}")
    print(f"Выполнено итераций: {iterations}")