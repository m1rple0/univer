import time
import random
from collections import deque

# обходы графа

def dfs_rek(g, v, visited=None): # v glubiny recursivno
    if visited is None:
        visited = set()
    visited.add(v)
    path = [v]
    for u in g[v]:
        if u not in visited:
            path.extend(dfs_rek(g, u, visited))
    return path


def dfs_stack(g, start): # v glubiny stekom
    visited = set()
    stack = [start]
    res = []
    while stack:
        v = stack.pop()
        if v not in visited:
            visited.add(v)
            res.append(v)
            neigh = list(g[v])
            for u in reversed(neigh):
                if u not in visited:
                    stack.append(u)
    return res


def bfs_queue(g, start): # v shirinu 
    visited = set([start])
    q = deque([start])
    res = []
    while q:
        v = q.popleft()
        res.append(v)
        for u in g[v]:
            if u not in visited:
                visited.add(u)
                q.append(u)
    return res


# своя тупая очередь с приоритетом (для Дейкстры)

class PQueue:
    def __init__(self):
        self.data = []
    
    def push(self, prio, val):
        self.data.append((prio, val))
        self._up(len(self.data) - 1)
    
    def pop(self):
        if not self.data:
            return None
        self._swap(0, len(self.data) - 1)
        item = self.data.pop()
        self._down(0)
        return item
    
    def empty(self):
        return len(self.data) == 0
    
    def _up(self, i):
        p = (i - 1) // 2
        if i > 0 and self.data[i][0] < self.data[p][0]:
            self._swap(i, p)
            self._up(p)
    
    def _down(self, i):
        left = 2*i + 1
        right = 2*i + 2
        smallest = i
        if left < len(self.data) and self.data[left][0] < self.data[smallest][0]:
            smallest = left
        if right < len(self.data) and self.data[right][0] < self.data[smallest][0]:
            smallest = right
        if smallest != i:
            self._swap(i, smallest)
            self._down(smallest)
    
    def _swap(self, i, j):
        self.data[i], self.data[j] = self.data[j], self.data[i]


def dijkstra(g, start):
    dist = {v: 9999999 for v in g}
    dist[start] = 0
    pq = PQueue()
    pq.push(0, start)
    visited = set()
    
    while not pq.empty():
        cur_dist, v = pq.pop()
        if v in visited:
            continue
        visited.add(v)
        for u, w in g[v].items():
            nd = cur_dist + w
            if nd < dist[u]:
                dist[u] = nd
                pq.push(nd, u)
    return dist


# генерация графов

def gen_sparse(n, edges_per_vertex=3):
    g = {i: {} for i in range(n)}
    for i in range(n):
        candidates = [j for j in range(n) if j != i]
        if len(candidates) > edges_per_vertex:
            neigh = random.sample(candidates, edges_per_vertex)
        else:
            neigh = candidates
        for j in neigh:
            w = random.randint(1, 20)
            g[i][j] = w
            g[j][i] = w
    return g


def gen_dense(n, prob=0.6):
    g = {i: {} for i in range(n)}
    for i in range(n):
        for j in range(i+1, n):
            if random.random() < prob:
                w = random.randint(1, 20)
                g[i][j] = w
                g[j][i] = w
    return g


def gen_complete(n):
    g = {i: {} for i in range(n)}
    for i in range(n):
        for j in range(n):
            if i != j:
                g[i][j] = random.randint(1, 20)
    return g


def matr_to_list(matr):
    n = len(matr)
    g = {i: {} for i in range(n)}
    for i in range(n):
        for j in range(n):
            if matr[i][j] != 0:
                g[i][j] = matr[i][j]
    return g


def list_to_matr(g, n):
    m = [[0]*n for _ in range(n)]
    for i in range(n):
        for j, w in g[i].items():
            m[i][j] = w
    return m


# тестирование

def test_graph(g, name):
    n = len(g)
    edges = sum(len(g[i]) for i in g) // 2
    print(f"\n {name} ")
    print(f"вершин: {n}, ребер: {edges}")
    
    start_v = 0
    
    t1 = time.perf_counter()
    r1 = dfs_rek(g, start_v)
    t2 = time.perf_counter()
    print(f"DFS рекурсия:   {t2-t1:.6f} с ({len(r1)} вершин)")
    
    t1 = time.perf_counter()
    r2 = dfs_stack(g, start_v)
    t2 = time.perf_counter()
    print(f"DFS стек:       {t2-t1:.6f} с ({len(r2)} вершин)")
    
    t1 = time.perf_counter()
    r3 = bfs_queue(g, start_v)
    t2 = time.perf_counter()
    print(f"BFS:            {t2-t1:.6f} с ({len(r3)} вершин)")
    
    t1 = time.perf_counter()
    d = dijkstra(g, start_v)
    t2 = time.perf_counter()
    print(f"Дейкстра:       {t2-t1:.6f} с")
    print(f"расстояния до {min(5, n)} вершин: {list(d.items())[:5]}")
    
    if set(r1) == set(r2) == set(r3):
        print("обходы корректны")
    else:
        print("ошибка в обходах")


def run_tests():
    
    # маленький граф для проверки
    print("\nмаленький граф (ручная проверка)")
    small = {
        0: {1: 2, 2: 5},
        1: {0: 2, 3: 1, 4: 3},
        2: {0: 5, 5: 4},
        3: {1: 1},
        4: {1: 3},
        5: {2: 4}
    }
    print("граф:")
    for v in small:
        print(f"  {v} -> {list(small[v].keys())}")
    print(f"\nDFS рекурсия от 0: {dfs_rek(small, 0)}")
    print(f"DFS стек от 0:     {dfs_stack(small, 0)}")
    print(f"BFS от 0:          {bfs_queue(small, 0)}")
    
    # тест на разных графах
    test_graph(small, "ручной граф")
    
    # разреженные
    for n in [10, 50, 100]:
        g = gen_sparse(n, edges_per_vertex=3)
        test_graph(g, f"разреженный n={n}")
    
    # плотные
    for n in [10, 50, 100]:
        g = gen_dense(n, prob=0.7)
        test_graph(g, f"плотный n={n}")
    
    # полносвязные (только небольшие)
    for n in [5, 10, 20]:
        g = gen_complete(n)
        test_graph(g, f"полносвязный n={n}")
    
    # тест с матрицей смежности
    print("\n представление через матрицу")
    n = 15
    g_list = gen_dense(n, 0.5)
    g_matr = list_to_matr(g_list, n)
    g_from_matr = matr_to_list(g_matr)
    test_graph(g_from_matr, f"матрица {n}x{n} (преобразовано)")
    
    # граничные случаи
    print("\n граничные случаи")
    test_graph({0: {}}, "одна вершина")
    test_graph({0: {1: 1}, 1: {0: 1}}, "две вершины")
    
    # цепочка
    chain = {i: {} for i in range(20)}
    for i in range(19):
        chain[i][i+1] = 1
        chain[i+1][i] = 1
    test_graph(chain, "цепочка из 20 вершин")
    
    # звезда
    star = {0: {}}
    for i in range(1, 20):
        star[0][i] = 1
        star[i] = {0: 1}
    test_graph(star, "звезда (центр + 19 листьев)")
    
    # большой граф (500 вершин)
    print("\n большой граф (500 вершин, разреженный)")
    big = gen_sparse(500, edges_per_vertex=3)
    
    t1 = time.perf_counter()
    dfs_stack(big, 0)
    t2 = time.perf_counter()
    print(f"DFS на 500: {t2-t1:.4f} с")
    
    t1 = time.perf_counter()
    bfs_queue(big, 0)
    t2 = time.perf_counter()
    print(f"BFS на 500: {t2-t1:.4f} с")
    
    # замеры для Дейкстры отдельно
    print("\n производительность Дейкстры")
    for n in [10, 20, 50, 100]:
        g_sp = gen_sparse(n, 3)
        g_de = gen_dense(n, 0.7)
        
        t1 = time.perf_counter()
        dijkstra(g_sp, 0)
        t_sp = time.perf_counter() - t1
        
        t1 = time.perf_counter()
        dijkstra(g_de, 0)
        t_de = time.perf_counter() - t1
        
        print(f"n={n:3}  разреженный: {t_sp:.6f} с   плотный: {t_de:.6f} с")
    


if __name__ == "__main__":
    run_tests()