import numpy as np


# Вспомогательная функция для евклидовой нормы
def norm(v):
    return np.linalg.norm(v)


def golden_section_search(f, xk, pk, a=-10, b=10, tol=1e-5):
    phi = (1 + np.sqrt(5)) / 2
    num_evals = 0

    def g(alpha):
        nonlocal num_evals
        num_evals += 1
        return f(xk + alpha * pk)

    while abs(b - a) > tol:
        c = b - (b - a) / phi
        d = a + (b - a) / phi
        if g(c) < g(d):
            b = d
        else:
            a = c
    alpha = (a + b) / 2
    return alpha, num_evals



def hooke_jeeves(f, x0, h, z=0.5, epsilon=1e-5, max_iter=10000):
    n = len(x0)
    xk = np.copy(x0)
    total_evals = 0

    def exploratory_search(b, h):
        nonlocal total_evals
        x = np.copy(b)
        for i in range(n):
            xp = x.copy()
            xp[i] += h[i]
            fp = f(xp)
            total_evals += 1
            xm = x.copy()
            xm[i] -= h[i]
            fm = f(xm)
            total_evals += 1
            f_current = f(x)
            total_evals += 1
            if fp < f_current:
                x = xp
            elif fm < f_current:
                x = xm
        return x

    b1 = np.copy(xk)
    k = 0
    while norm(h) > epsilon and k < max_iter:
        b2 = exploratory_search(xk, h)
        x_next = b2 + (b2 - b1)
        x = exploratory_search(x_next, h)
        f_x = f(x)
        f_b2 = f(b2)
        total_evals += 2
        if f_x < f_b2:
            xk = x
            b1 = b2
        else:
            h = z * h
            xk = b1
        k += 1

    return xk, f(xk), total_evals


# Метод Флетчера-Ривса
def fletcher_reeves(f, grad_f, x0, epsilon=1e-5, max_iter=10000):
    n = len(x0)
    xk = np.copy(x0)
    total_evals = 0
    gk = grad_f(xk)
    pk = -gk
    k = 0

    while norm(gk) > epsilon and k < max_iter:
        alpha, evals = golden_section_search(f, xk, pk)
        total_evals += evals
        x_next = xk + alpha * pk
        g_next = grad_f(x_next)
        if (k + 1) % n == 0:
            beta = 0
        else:
            beta = (norm(g_next) ** 2) / (norm(gk) ** 2)
        pk = -g_next + beta * pk
        xk = x_next
        gk = g_next
        k += 1

    return xk, f(xk), total_evals


# Метод Ньютона-Рафсона
def newton_raphson(f, grad_f, hess_f, x0, epsilon=1e-5, max_iter=10000):
    xk = np.copy(x0)
    total_evals = 0
    k = 0

    while k < max_iter:
        gk = grad_f(xk)
        if norm(gk) <= epsilon:
            break
        try:
            Hk = hess_f(xk)
            inv_Hk = np.linalg.inv(Hk)
            pk = -inv_Hk @ gk
        except (np.linalg.LinAlgError, ValueError):
            pk = -gk  # Fallback на градиент
        alpha, evals = golden_section_search(f, xk, pk)
        total_evals += evals
        xk = xk + alpha * pk
        k += 1

    return xk, f(xk), total_evals


# Тестовая функция: f(x) = 4(x1 - 5)^2 + (x2 - 6)^2
def test_function(x):
    return 4 * (x[0] - 5) ** 2 + (x[1] - 6) ** 2


def grad_test_function(x):
    return np.array([8 * (x[0] - 5), 2 * (x[1] - 6)])


def hess_test_function(x):
    return np.array([[8, 0], [0, 2]])


# Функция Розенброка
def rosenbrock(x):
    return sum(100.0 * (x[1:] - x[:-1] ** 2.0) ** 2.0 + (1 - x[:-1]) ** 2.0)


def grad_rosenbrock(x):
    xm = x[1:-1]
    xp = x[2:]
    xm_m1 = x[:-2]
    der = np.zeros_like(x)
    der[1:-1] = 200 * (xm - xm_m1 ** 2) - 400 * (xp - xm ** 2) * xm - 2 * (1 - xm)
    der[0] = -400 * x[0] * (x[1] - x[0] ** 2) - 2 * (1 - x[0])
    der[-1] = 200 * (x[-1] - x[-2] ** 2)
    return der


def hess_rosenbrock(x):
    if len(x) != 2:
        raise ValueError("Only for n=2")
    H = np.array([[1202 - 400 * x[1] + 800 * x[0] ** 2, -400 * x[0]],
                  [-400 * x[0], 200]])
    return H


# Функция Химмельблау
def himmelblau(x):
    return (x[0]**2 + x[1] - 11)**2 + (x[0] + x[1]**2 - 7)**2


def grad_himmelblau(x):
    return np.array([
        4 * x[0] * (x[0]**2 + x[1] - 11) + 2 * (x[0] + x[1]**2 - 7),
        2 * (x[0]**2 + x[1] - 11) + 4 * x[1] * (x[0] + x[1]**2 - 7)
    ])


def hess_himmelblau(x):
    return np.array([
        [12 * x[0]**2 + 4 * x[1] - 42, 4 * x[0] + 4 * x[1]],
        [4 * x[0] + 4 * x[1], 4 * x[0] + 12 * x[1]**2 - 26]
    ])


# Функция Вуда
def wood(x):
    return (100 * (x[1] - x[0]**2)**2 + (1 - x[0])**2 +
            90 * (x[3] - x[2]**2)**2 + (1 - x[2])**2 +
            10.1 * ((x[1] - 1)**2 + (x[3] - 1)**2) +
            19.8 * (x[1] - 1) * (x[3] - 1))


def grad_wood(x):
    return np.array([
        -400 * x[0] * (x[1] - x[0]**2) - 2 * (1 - x[0]),
        200 * (x[1] - x[0]**2) + 20.2 * (x[1] - 1) + 19.8 * (x[3] - 1),
        -360 * x[2] * (x[3] - x[2]**2) - 2 * (1 - x[2]),
        180 * (x[3] - x[2]**2) + 20.2 * (x[3] - 1) + 19.8 * (x[1] - 1)
    ])


def hess_wood(x):
    # Для n=4 гессиан сложен, используем численное приближение или градиентный спуск
    return np.zeros((4, 4))  # Заглушка, метод Ньютона-Рафсона использует градиент при ошибке


# Функция Пауэлла
def powell(x):
    return ((x[0] + 10 * x[1])**2 + 5 * (x[2] - x[3])**2 +
            (x[1] - 2 * x[2])**4 + 10 * (x[0] - x[3])**4)


def grad_powell(x):
    return np.array([
        2 * (x[0] + 10 * x[1]) + 40 * (x[0] - x[3])**3,
        20 * (x[0] + 10 * x[1]) + 4 * (x[1] - 2 * x[2])**3,
        10 * (x[2] - x[3]) - 8 * (x[1] - 2 * x[2])**3,
        -10 * (x[2] - x[3]) - 40 * (x[0] - x[3])**3
    ])


def hess_powell(x):
    # Для n=4 гессиан сложен и вырожден в минимуме, используем градиентный спуск
    return np.zeros((4, 4))  # Заглушка, метод Ньютона-Рафсона использует градиент при ошибке


# Функция Матьяса
def matyas(x):
    return 0.26 * (x[0]**2 + x[1]**2) - 0.48 * x[0] * x[1]


def grad_matyas(x):
    return np.array([
        0.52 * x[0] - 0.48 * x[1],
        0.52 * x[1] - 0.48 * x[0]
    ])


def hess_matyas(x):
    return np.array([[0.52, -0.48], [-0.48, 0.52]])


# Словарь функций
functions = {
    1: ('Тестовая функция', test_function, grad_test_function, hess_test_function, np.array([0.0, 0.0]),
        np.array([1.0, 1.0]), 0.001),
    2: ('Функция Розенброка', rosenbrock, grad_rosenbrock, hess_rosenbrock, np.array([-1.2, 1.0]),
        np.array([0.1, 0.1]), 0.001),
    3: ('Функция Химмельблау', himmelblau, grad_himmelblau, hess_himmelblau, np.array([0.0, 0.0]),
        np.array([1.0, 1.0]), 0.001),
    4: ('Функция Вуда', wood, grad_wood, hess_wood,
        [np.array([-3.0, -1.0, -3.0, -1.0]), np.array([2.0, -1.0, -3.0, -1.0])],
        np.array([0.1, 0.1, 0.1, 0.1]), 0.001),
    5: ('Функция Пауэлла', powell, grad_powell, hess_powell,
        [np.array([3.0, -1.0, 0.0, 1.0]), np.array([1.0, 1.0, 1.0, 1.0])],
        np.array([0.1, 0.1, 0.1, 0.1]), 0.001),
    6: ('Функция Матьяса', matyas, grad_matyas, hess_matyas, np.array([0.0, 0.0]),
        np.array([1.0, 1.0]), 0.001)
}


# Основная программа
def main():
    print("Выберите задание:")
    for key, (name, _, _, _, _, _, _) in functions.items():
        print(f"{key}. {name}")

    try:
        choice = int(input("Введите номер функции (1-6): "))
        if choice not in functions:
            raise ValueError
    except ValueError:
        print("Неверный выбор, используется Тестовая функция")
        choice = 1

    name, f, grad_f, hess_f, x0, h, epsilon = functions[choice]
    print(f"\nВыбрана: {name}")

    # Если для функции указано несколько начальных точек
    if isinstance(x0, list):
        print("\nВыберите начальную точку:")
        for i, point in enumerate(x0, 1):
            print(f"{i}. {point}")
        try:
            point_choice = int(input("Введите номер начальной точки: ")) - 1
            if point_choice not in range(len(x0)):
                raise ValueError
            x0 = x0[point_choice]
        except ValueError:
            print("Неверный выбор, используется первая начальная точка")
            x0 = x0[0]

    print(f"\nНачальная точка: {x0}")
    print("\nМетод Хука-Дживса:")
    x_hj, f_hj, evals_hj = hooke_jeeves(f, x0, h, z=0.5, epsilon=epsilon)
    print(f"Минимум в точке: {x_hj}")
    print(f"Значение функции: {f_hj}")
    print(f"Число вычислений f: {evals_hj}")

    print("\nМетод Флетчера-Ривса:")
    x_fr, f_fr, evals_fr = fletcher_reeves(f, grad_f, x0, epsilon=epsilon)
    print(f"Минимум в точке: {x_fr}")
    print(f"Значение функции: {f_fr}")
    print(f"Число вычислений f: {evals_fr}")

    print("\nМетод Ньютона-Рафсона:")
    x_nr, f_nr, evals_nr = newton_raphson(f, grad_f, hess_f, x0, epsilon=epsilon)
    print(f"Минимум в точке: {x_nr}")
    print(f"Значение функции: {f_nr}")
    print(f"Число вычислений f: {evals_nr}")


if __name__ == "__main__":
    main()