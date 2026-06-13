def solve():
    n = int(input())
    tree = [[] for _ in range(n+1)]
    root = 0

    parents = list(map(int, input().split()))
    for i, parent in enumerate(parents, start=1):
        if parent == 0:
            root = i
        else:
            tree[parent].append(i)

    tin = [0] * (n+1)
    tout = [0] * (n+1)
    timer = 0
    stack = [(root, False)]

    while stack:
        x, processed = stack.pop()
        if not processed:
            timer += 1
            tin[x] = timer
            stack.append((x, True))
            for child in reversed(tree[x]):
                stack.append((child, False))
        else:
            tout[x] = timer

    m = int(input())  # количество запросов
    results = []
    for _ in range(m):
        u, v = map(int, input().split())
        if tin[u] <= tin[v] <= tout[u]:
            results.append("1")
        else:
            results.append("0")
    
    return "\n".join(results)

print(solve())