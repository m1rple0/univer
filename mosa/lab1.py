import math


def davis_swann_campi(func, x0, h, max_iter=100):
    f0 = func(x0)
    f1 = func(x0 + h)

    if f1 > f0:
        h = -h
        f1 = func(x0 + h)
        if f1 > f0:
            a, b = x0 - abs(h), x0 + abs(h)
            return (a, b)

    x_prev2 = x0
    x_prev1 = x0 + h
    f_prev1 = func(x_prev1)
    k = 2

    while k <= max_iter:
        xk = x0 + (2 ** (k - 1)) * h
        fk = func(xk)

        if fk >= f_prev1:
            a = min(x_prev2, xk)
            b = max(x_prev2, xk)
            return (a, b)

        x_prev2, x_prev1 = x_prev1, xk
        f_prev1 = fk
        k += 1

    raise RuntimeError(f"Не удалось локализовать минимум за {max_iter} итераций")


def dichotomy_method(f, a, b, epsilon=0.01, delta=None):
    if delta is None:
        delta = epsilon / 10

    iterations = 0
    while (b - a) / 2 >= epsilon:
        iterations += 1
        x1 = 0.5 * (a + b) - delta
        x2 = 0.5 * (a + b) + delta
        f1 = f(x1)
        f2 = f(x2)

        if f1 <= f2:
            b = x2
        else:
            a = x1

    x_star = 0.5 * (a + b)
    return x_star, f(x_star), iterations


def fibonacci_method(f, a, b, epsilon=0.01, delta=None):
    if delta is None:
        delta = epsilon / 10

    fib = [1, 1]
    while fib[-1] < (b - a) / (2 * epsilon):
        fib.append(fib[-1] + fib[-2])
    N = len(fib) - 1

    k = 0
    x1 = a + (fib[N - 2] / fib[N]) * (b - a)
    x2 = a + (fib[N - 1] / fib[N]) * (b - a)
    f1 = f(x1)
    f2 = f(x2)
    iterations = 0

    while k < N - 3:
        iterations += 1
        if f1 <= f2:
            b = x2
            x2 = x1
            x1 = a + (fib[N - k - 3] / fib[N - k - 1]) * (b - a)
            f2 = f1
            f1 = f(x1)
        else:
            a = x1
            x1 = x2
            x2 = a + (fib[N - k - 2] / fib[N - k - 1]) * (b - a)
            f1 = f2
            f2 = f(x2)
        k += 1

    x2 = x1 + delta
    f1 = f(x1)
    f2 = f(x2)
    if f1 <= f2:
        b = x2
    else:
        a = x1

    x_star = 0.5 * (a + b)
    return x_star, f(x_star), iterations + 1


def func1(x):
    return (x - 1) ** 2


def func2(x):
    return 4 * x ** 3 - 8 * x ** 2 - 11 * x + 5


def func3(x):
    if x == 0:
        raise ValueError("Деление на ноль в f(x) = x + 3/x^2")
    return x + 3 / (x ** 2)


def func4(x):
    if x ** 2 == 4:
        raise ValueError("Деление на ноль в f(x) = (x + 2.5)/(4 - x^2)")
    return (x + 2.5) / (4 - x ** 2)


def func5(x):
    return -math.sin(x) - (math.sin(3 * x)) / 3


def func6(x):
    return -2 * math.sin(x) - math.sin(2 * x) - (2 * math.sin(3 * x)) / 3


functions = {
    1: (func1, "f(x) = (x-1)**2"),
    2: (func2, "f(x) = 4*x**3 - 8*x**2 - 11*x + 5"),
    3: (func3, "f(x) = x + 3/x**2"),
    4: (func4, "f(x) = (x + 2.5)/(4 - x**2)"),
    5: (func5, "f(x) = -sin(x) - sin(3x)/3"),
    6: (func6, "f(x) = -2sin(x) - sin(2x) - 2sin(3x)/3")
}

if __name__ == "__main__":
    # Выбор функции
    print("Выберите функцию:")
    print("1) f(x) = (x-1)**2")
    print("2) f(x) = 4*x**3 - 8*x**2 - 11*x + 5")
    print("3) f(x) = x + 3/x**2")
    print("4) f(x) = (x + 2.5)/(4 - x**2)")
    print("5) f(x) = -sin(x) - sin(3x)/3")
    print("6) f(x) = -2sin(x) - sin(2x) - 2sin(3x)/3")

    while True:
        try:
            choice = int(input("Введите номер функции (1-6): "))
            if choice in functions:
                break
            print("Пожалуйста, выберите число от 1 до 6")
        except ValueError:
            print("Пожалуйста, введите корректное число")

    f, func_name = functions[choice]

    try:
        x0 = float(input("Введите начальную точку x0: "))
        h = float(input("Введите шаг h: "))
    except ValueError:
        print("Ошибка: введите корректные числовые значения")
        exit(1)

    try:
        interval = davis_swann_campi(f, x0, h)
        print(f"\nФункция: {func_name}")
        print(f"x0 = {x0}, h = {h}")
        print(f"Отрезок локализации минимума: {interval}")
    except (RuntimeError, ValueError) as e:
        print(f"Ошибка при локализации минимума: {e}")
        exit(1)

    a, b = interval

    try:
        x_min_d, f_min_d, it_d = dichotomy_method(f, a, b)
        print(f"\nМетод дихотомии: минимум найден за {it_d} итераций")
        print(f"x* = {x_min_d:.6f}, f(x*) = {f_min_d:.6f}")
    except ValueError as e:
        print(f"Ошибка в методе дихотомии: {e}")

    # Метод Фибоначчи
    try:
        x_min_f, f_min_f, it_f = fibonacci_method(f, a, b)
        print(f"\nМетод Фибоначчи: минимум найден за {it_f} итераций")
        print(f"x* = {x_min_f:.6f}, f(x*) = {f_min_f:.6f}")
    except ValueError as e:
        print(f"Ошибка в методе Фибоначчи: {e}")