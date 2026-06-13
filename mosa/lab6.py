import numpy as np
import random

def generate_random_vector(size):
    beta = 2 * np.random.rand(size) - 1
    sum_ = np.linalg.norm(beta)
    return beta / sum_

def statistical_gradient_method(
        func,
        x0: np.ndarray,
        h,
        M,
        epsilon=0.001,
        beta=0.618,
        lambda_=1.0,
        max_iters_num=1000
    ):
    """
    Метод статистического градиента
    """
    k = 0
    x = x0.copy()

    while True:
        k += 1
        if k > max_iters_num:
            return x, k

        f_x = func(x)

        grad_est = np.zeros_like(x)

        # Формирование статистической оценки градиента
        for _ in range(M):
            xi = generate_random_vector(x.size)
            df = func(x + h * xi) - f_x
            grad_est += xi * df

        grad_norm = np.linalg.norm(grad_est)

        if grad_norm < 1e-12:
            h = h * beta
            if np.linalg.norm(h) <= epsilon:
                return x, k
            continue

        # Нормированное направление спуска
        direction = grad_est / grad_norm

        # Рабочий шаг
        x_new = x - lambda_ * direction

        # Критерий остановки
        if np.linalg.norm(x_new - x) <= epsilon:
            return x_new, k

        # Если улучшение есть — принимаем шаг
        if func(x_new) < f_x:
            x = x_new
            lambda_ *= 1.2
        else:
            lambda_ *= beta 


def repetative_random_search(func, x0: np.ndarray, h, M, beta=0.5, hamma=0.7, lambda_=1, epsilon=0.001, max_iters_num=1000):
    k = 0
    x1 = x0
    x2 = x0
    while True:
        k += 1
        if k > max_iters_num:
            return x1, k
        if k <= 2:
            x0 = x1
            x1 = x2
            x2,_ = statistical_gradient_method(func, x1, h, M, epsilon)
            #print(x0, x1, x2, func(x2), func(x1))
        else:
            S2 = x2 - x1
            S1 = x1 - x0
            S = hamma * S2 + (1-hamma) * S1
            for i in range(M):
                v = generate_random_vector(x0.size)
                x3 = x2 + lambda_ * (beta*S/np.linalg.norm(S) + (1-beta)*v/np.linalg.norm(v))
                #print(x0, x1, x2, x3, func(x3), func(x2))
                if func(x3) < func(x2):
                    #print(x0, x1, x2, x3, func(x3), func(x2))
                    if lambda_ <= epsilon:
                        return x3, k
                    lambda_ *= 2
                    x0 = x1
                    x1 = x2
                    x2 = x3
                    break
            else:
                lambda_ *= 0.5

# Определение тестовых функций
def himmelblau(x):
    """Функция Химмельблау №1"""
    return 4*(x[0]-5)**2 + (x[1] - 6)**2

def rastrigin(x):
    """Функция Расстрыгина (2D)"""
    n = len(x)
    return 10*n + sum(x[i]**2 - 10*np.cos(2*np.pi*x[i]) for i in range(n))

def ackley(x):
    """Функция Экли"""
    return -20*np.exp(-0.2*np.sqrt(0.5*(x[0]**2 + x[1]**2))) - \
           np.exp(0.5*(np.cos(2*np.pi*x[0]) + np.cos(2*np.pi*x[1]))) + np.e + 20

def beale(x):
    """Функция Била"""
    return (1.5 - x[0] + x[0]*x[1])**2 + \
           (2.25 - x[0] + x[0]*x[1]**2)**2 + \
           (2.625 - x[0] + x[0]*x[1]**3)**2

def bukin(x):
    """Функция Букина"""
    return 100*np.sqrt(np.abs(x[1] - 0.01*x[0]**2)) + 0.01*np.abs(x[0] + 10)

def matyas(x):
    """Функция Матьяса"""
    return 0.26*(x[0]**2 + x[1]**2) - 0.48*x[0]*x[1]

def rosenbrock(x):
    """Функция Розенброка"""
    return 100*(x[1] - x[0]**2)**2 + (x[0] - 1)**2

# Словарь доступных функций
functions = {
    1: ("Функция Химмельблау №1 (2D)", himmelblau, 2),
    2: ("Функция Расстрыгина (2D)", rastrigin, 2),
    3: ("Функция Расстрыгина (3D)", rastrigin, 3),
    4: ("Функция Расстрыгина (4D)", rastrigin, 4),
    5: ("Функция Экли (2D)", ackley, 2),
    6: ("Функция Била (2D)", beale, 2),
    7: ("Функция Букина (2D)", bukin, 2),
    8: ("Функция Матьяса (2D)", matyas, 2),
    9: ("Функция Розенброка (2D)", rosenbrock, 2)
}

if __name__ == "__main__":
    print("Доступные функции для оптимизации:")
    print("-" * 50)
    for key, (name, _, dim) in functions.items():
        print(f"{key}. {name}")
    print("-" * 50)
    
    # Выбор функции
    choice = int(input("Выберите номер функции (1-9): "))
    if choice not in functions:
        raise ValueError("Неверный номер функции")
    
    func_name, func, dimension = functions[choice]
    
    # Ввод начальной точки
    print(f"\nВыбрана функция: {func_name}")
    
    if dimension == 2:
        x_input = input("Введите начальную точку (два числа через пробел): ")
        x0 = np.array([float(x) for x in x_input.split()])
        if len(x0) != 2:
            raise ValueError("Неверное количество координат")
    elif dimension == 3:
        x_input = input("Введите начальную точку (три числа через пробел): ")
        x0 = np.array([float(x) for x in x_input.split()])
        if len(x0) != 3:
            raise ValueError("Неверное количество координат")
    elif dimension == 4:
        x_input = input("Введите начальную точку (четыре числа через пробел): ")
        x0 = np.array([float(x) for x in x_input.split()])
        if len(x0) != 4:
            raise ValueError("Неверное количество координат")
    
    # Ввод точности
    epsilon = float(input("Введите точность epsilon (по умолчанию 0.001): ") or "0.001")
    M = int(input("Введите кол-во моделирований (по умолчанию 1000): ") or "1000")
    max_iters_num = int(input("Введите максимальное кол-во итераций (по умолчанию 1000): ") or "1000")
    
    # Параметры алгоритмов
    h = np.ones(dimension)
    
    print("\n" + "=" * 60)
    
    # Запуск алгоритмов
    print("\nРезультаты работы алгоритмов:")
    print("-" * 40)
    
    # Метод улучшенного зондирования
    result1, iterations1 = statistical_gradient_method(func, x0, h, M, epsilon=epsilon, max_iters_num=max_iters_num)
    print(f"Метод статистического градиента:")
    print(f"  Найденная точка: {result1}")
    print(f"  Значение функции: {func(result1):.6f}")
    print(f"  Количество итераций: {iterations1}")
    
    # Метод повторного случайного поиска
    result2, iterations2 = repetative_random_search(func, x0, h, M, epsilon=epsilon, max_iters_num=max_iters_num)
    print(f"\nМетод повторяющегося случайного поиска:")
    print(f"  Найденная точка: {result2}")
    print(f"  Значение функции: {func(result2):.6f}")
    print(f"  Количество итераций: {iterations2}")
        