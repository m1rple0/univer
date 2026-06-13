
import numpy as np
import math
from lab1 import fibonacci_method

def partial_derivative(func, x, i, h=1e-6):
    """
    Числовая частичная производная (центральная разность).
    Если в lab2 есть аналитическая, замените на импорт.
    """
    e = np.zeros_like(x)
    e[i] = h
    return (func(x + e) - func(x - e)) / (2 * h)

def solve_linear_programming(c, A_ub=None, b_ub=None, bounds=None):
    """
    Решает задачу линейного программирования произвольной размерности.
    """
    result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds, method="highs")
    return result

def zoutendijk(func, x0: np.ndarray, P_A_matrix: np.ndarray, P_b: np.ndarray, epsilon=0.001, eps_active=1e-6):
    k = 0
    x = x0.copy()
    n = x.size
    while True:
        k += 1
        grad = np.array([partial_derivative(func, x, i) for i in range(n)])
        
        # Определение активных ограничений (A x - b <= 0, активные если близко к 0)
        residuals_ineq = P_A_matrix @ x - P_b
        active_ineq = np.where(residuals_ineq >= -eps_active)[0]
        
        # Активные нижние границы x_j >= 0
        active_low = np.where(x <= eps_active)[0]
        
        # LP: max beta, переменные [d_1, ..., d_n, beta]
        dim = n + 1
        c = np.zeros(dim)
        c[-1] = -1  # min -beta == max beta
        
        A_ub_list = []
        b_ub_list = []
        
        # grad^T d + beta <= 0
        row = np.append(grad, 1.0)
        A_ub_list.append(row)
        b_ub_list.append(0.0)
        
        # Для активных A_i d + beta <= 0
        for i in active_ineq:
            row = np.append(P_A_matrix[i], 1.0)
            A_ub_list.append(row)
            b_ub_list.append(0.0)
        
        # Для активных x_j >= 0: -d_j + beta <= 0
        for j in active_low:
            row = np.zeros(dim)
            row[j] = -1.0
            row[-1] = 1.0
            A_ub_list.append(row)
            b_ub_list.append(0.0)
        
        A_ub = np.array(A_ub_list) if A_ub_list else None
        b_ub = np.array(b_ub_list) if b_ub_list else None
        
        # Нормализация: -1 <= d_j <= 1, beta >= 0
        bounds = [(-1, 1) for _ in range(n)] + [(0, None)]
        
        result = solve_linear_programming(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds)
        
        if not result.success:
            raise ValueError(f"LP не решена успешно: {result.message}")
        
        beta_opt = -result.fun
        d = result.x[:-1]
        
        if beta_opt <= epsilon:
            return x, k
        
        # alpha_max для feasibility
        alpha_max = float('inf')
        for i in range(P_A_matrix.shape[0]):
            A_d = P_A_matrix[i] @ d
            if A_d > 0:
                alpha_i = (P_b[i] - P_A_matrix[i] @ x) / A_d
                alpha_max = min(alpha_max, alpha_i)
        
        for j in range(n):
            if d[j] < 0:
                alpha_j = -x[j] / d[j]
                alpha_max = min(alpha_max, alpha_j)
        
        if alpha_max <= 0:
            raise ValueError("alpha_max <= 0, направление не осуществимо")
        if math.isinf(alpha_max):
            alpha_max = 10.0  # Fallback для unbounded, подстройте если нужно
        
        # Поиск по строке с fibonacci_method (аналог golden)
        alpha, _, _ = fibonacci_method(lambda a: func(x + a * d), 0, alpha_max, epsilon)
        
        x1 = x + alpha * d
        if abs(func(x1) - func(x)) <= epsilon:
            return x1, k
        x = x1

if __name__ == "__main__":
    # Определяем список задач для метода Зонтейдейка
    tasks = [
        {
            'name': "Задача из примера: f(x) = -(-(x₁ - 1)² - 2(x₂ - 1)² + 3) → min",
            'func': lambda x: -(-(x[0] - 1)**2 - 2*(x[1] - 1)**2 + 3),
            'A_matrix': np.array([[1, 2],[2,-1]]),
            'b': np.array([8,12])
        },
        {
            'name': "Задача 3: f(x) = 4/x₁ + 9/x₂ + x₁ + x₂ → min",
            'func': lambda x: 4/x[0] + 9/x[1] + x[0] + x[1],
            'A_matrix': np.array([[1, 1]]),  # x₁ + x₂ ≤ 6
            'b': np.array([6])
        },
        {
            'name': "Задача 5: F = 7x₁² - 4x₂⁴ + 3x₃² - 4x₄² + 6x₅² + 5x₆",
            'func': lambda x: 7*x[0]**2 - 4*x[1]**4 + 3*x[2]**2 - 4*x[3]**2 + 6*x[4]**2 + 5*x[5],
            'A_matrix': np.array([
                [2, 3, 1, 1, 2, 4],      # 2x₁ + 3x₂ + x₃ + x₄ + 2x₅ + 4x₆ ≤ 48
                [-3, 0, 4, 0, 4, 3],     # -3x₁ + 4x₃ + 4x₅ + 3x₆ ≤ 36
                [-1, -4, -5, -4, -6, -4], # -(x₁ + 4x₂ + 5x₃ + 4x₄ + 6x₅ + 4x₆) ≤ -20 (т.е. >=20)
                [-5, -3, -6, -1, -2, -1]  # -(5x₁ + 3x₂ + 6x₃ + x₄ + 2x₅ + x₆) ≤ -30 (т.е. >=30)
            ]),
            'b': np.array([48, 36, -20, -30])
        }
    ]
    
    while True:
        print("\n" + "="*70)
        print("МЕТОД ЗОНТЕЙДЕЙКА - ВЫБОР ЗАДАЧИ")
        print("="*70)
        
        for i, task in enumerate(tasks, 1):
            print(f"{i}) {task['name']}")
        print(f"{len(tasks)+1}) Выход")
        
        choice = int(input("\nВаш выбор: "))
        if choice == len(tasks) + 1:
            print("Выход из программы.")
            break
        if choice < 1 or choice > len(tasks):
            print("Неверный выбор! Попробуйте снова.")
            continue
        
        task = tasks[choice-1]
        print(f"\n{task['name']}")
        
        # Ввод точности
        epsilon = float(input("Введите точность (например, 0.001): "))
        
        # Выбор начальной точки
        x0_input = input("Введите начальную точку (через пробел): ")
        x0 = np.array([float(x) for x in x0_input.split()])
        
        print(f"\nЗапуск метода Зонтейдейка...")
        
        # Запуск метода
        x_opt, iterations = zoutendijk(
            task['func'],
            x0,
            task['A_matrix'],
            task['b'],
            epsilon=epsilon
        )
        
        # Вывод результатов
        f_opt = task['func'](x_opt)
        num_of_signs = int(-math.log10(epsilon))
        
        print(f"\nРЕЗУЛЬТАТЫ:")
        print(f"Найденная точка минимума: {np.array2string(x_opt, precision=num_of_signs, suppress_small=True)}")
        print(f"Значение функции в минимуме: {f_opt:.{num_of_signs}f}")
        print(f"Количество итераций: {iterations}")