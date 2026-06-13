import numpy as np
#import time
import math
from lab2 import newton_raphson

#для составления штрафных функций используем параболические
def penalty_function(x: np.ndarray, border_functions_eq, border_functions_ineq, r):
    sum_ = 0
    #для равенств
    for func in border_functions_eq:
        sum_ += func(x)**2
    #для неравенств
    for func in border_functions_ineq:
        sum_ += min(func(x), 0)**2
    return r*sum_

def numerical_gradient(f, x, h=1e-5):
    grad = np.zeros_like(x)
    for i in range(len(x)):
        ei = np.zeros_like(x)
        ei[i] = h
        grad[i] = (f(x + ei) - f(x - ei)) / (2 * h)
    return grad

def numerical_hessian(f, x, h=1e-4):
    n = len(x)
    hess = np.zeros((n, n))
    for i in range(n):
        ei = np.zeros_like(x)
        ei[i] = h
        grad_plus = numerical_gradient(f, x + ei)
        grad_minus = numerical_gradient(f, x - ei)
        hess[:, i] = (grad_plus - grad_minus) / (2 * h)
    return hess

def penalty_method(x0: np.ndarray, need_func, border_functions_eq, border_functions_ineq, r=0.1, z=5, epsilon=0.001):
    k = 0
    help_func = lambda x: need_func(x) + penalty_function(x, border_functions_eq, border_functions_ineq, r)
    grad_help = lambda x: numerical_gradient(help_func, x)
    hess_help = lambda x: numerical_hessian(help_func, x)
    while True:
        k += 1
        x0, _, _ = newton_raphson(help_func, grad_help, hess_help, x0, epsilon=epsilon)
        penalty = penalty_function(x0, border_functions_eq, border_functions_ineq, r)
        if penalty < epsilon:
            return x0, k
        r *= z

#для составления барьерной функции применяем обратную функцию барьера Кэрролла
def barrier_function(x: np.ndarray, border_functions_ineq, r):
    sum_ = 0
    #для неравенств
    for func in border_functions_ineq:
        f_num = func(x)
        if f_num > 0:
            sum_ += 1/(func(x))
        else:
            sum_ += 10**8
    return r*sum_

def barrier_method(x0: np.ndarray, need_func, border_functions_ineq, r=100, z=0.1, epsilon=0.001):
    k = 0
    help_func = lambda x: need_func(x) + barrier_function(x, border_functions_ineq, r)
    grad_help = lambda x: numerical_gradient(help_func, x)
    hess_help = lambda x: numerical_hessian(help_func, x)
    while True:
        k += 1
        for func in border_functions_ineq:
            if func(x0) <= 0:
                return x0, k
        x0, _, _ = newton_raphson(help_func, grad_help, hess_help, x0, epsilon=epsilon)
        barrier = barrier_function(x0, border_functions_ineq, r)
        if abs(barrier) < epsilon:
            return x0, k
        r *= z

if __name__ == "__main__":
    # Определяем список задач для условной минимизации
    tasks = [
        {
            'name': "Задача 1.1: f(x) = x₁² + x₂ при x₁ + x₂ = 2",
            'func': lambda x: x[0]**2 + x[1]**2,
            'eq_constraints': [lambda x: x[0] + x[1] - 2],
            'ineq_constraints': []
        },
        {
            'name': "Задача 1.2: f(x) = x₁² + x₂ при x₁ = 1 и 2 - x₁ - x₂ ≥ 0",
            'func': lambda x: x[0]**2 + x[1]**2,
            'eq_constraints': [lambda x: x[0] - 1],
            'ineq_constraints': [lambda x: 2 - x[0] - x[1]]
        },
        {
            'name': "Задача 3: f(x) = x₁² + x₂ при x₁ ≥ 1 и 2 - x₁ - x₂ ≥ 0",
            'func': lambda x: x[0]**2 + x[1]**2,
            'eq_constraints': [],
            'ineq_constraints': [
                lambda x: x[0] - 1,
                lambda x: 2 - x[0] - x[1]
            ]
        },
        {
            'name': "Задача 2.9: f(x) = (x₁ + 4)² + (x₂ - 4)² при 2x₁ - x₂ ≤ 2, x₁ ≥ 0, x₂ ≥ 0",
            'func': lambda x: (x[0] + 4)**2 + (x[1] - 4)**2,
            'eq_constraints': [],
            'ineq_constraints': [
                lambda x: 2 - 2*x[0] + x[1],
                lambda x: x[0],
                lambda x: x[1]
            ]
        },
        {
            'name': "Задача 2.11: f(x) = 3x₁² + 4x₁x₂ + 5x₂²",
            'func': lambda x: 3*x[0]**2 + 4*x[0]*x[1] + 5*x[1]**2,
            'eq_constraints': [],
            'ineq_constraints': [
                lambda x: x[0] + x[1] - 4,
                lambda x: x[0],
                lambda x: x[1]
            ]
        }
    ]
    
    while True:
        print("\n" + "="*60)
        print("Выберите задачу условной минимизации:")
        for i, task in enumerate(tasks, 1):
            print(f"{i}) {task['name']}")
        print(f"{len(tasks)+1}) Выход")
        
        choice = int(input("Ваш выбор: "))
        if choice == len(tasks) + 1:
            break
        if choice < 1 or choice > len(tasks):
            print("Неверный выбор!")
            continue
            
        task = tasks[choice-1]
        
        # Ввод точности
        epsilon = float(input("Введите точность (например, 0.001): "))
        
        # Выбор начальной точки
        x0_input = input("Введите начальную точку (через пробел, например: 0 0): ")
        x0 = np.array([float(x) for x in x0_input.split()])
        
        # Выбор метода
        print("\nВыберите метод:")
        print("1) Метод штрафных функций")
        print("2) Метод барьерных функций")
        
        print(f"\nРешаем задачу с начальной точкой {x0} и точностью {epsilon}")
        
        method_choice = int(input("Ваш выбор: "))
        
        if method_choice == 1:
            result = penalty_method(
                x0, 
                task['func'], 
                task['eq_constraints'], 
                task['ineq_constraints'],
                epsilon=epsilon
            )
            print("Метод штрафных функций:")
        elif method_choice == 2:
            if task['eq_constraints']:
                print("Метод барьерных функций не поддерживает ограничения-равенства!")
                continue
            result = barrier_method(
                x0,
                task['func'],
                task['ineq_constraints'],
                epsilon=epsilon
            )
            print("Метод барьерных функций:")
        else:
            print("Неверный выбор метода!")
            continue
        
        # Вывод результатов
        if result is not None:
            x_opt, iterations = result
            num_of_signs = int(-math.log10(epsilon))
            print(f"Найденная точка минимума: {np.array2string(x_opt, precision=num_of_signs, suppress_small=True)}")
            print(f"Значение функции в минимуме: {task['func'](x_opt):.{num_of_signs}f}")
            print(f"Количество итераций: {iterations}")
        else:
            print("Решение не найдено!")