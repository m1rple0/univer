import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from math import isnan
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, fpmax

# 1. Загрузка данных
df = pd.read_csv('LR6/lab6.csv', encoding='cp1251')
print(df.head())
print(df.shape)

# 2. Переформирование нужной колонки
# берём только product, чистим пробелы
np_df = df.to_numpy()
np_df = [[elem.strip() for elem in row[4:] if isinstance(elem, str)] for row in np_df]
print(np_df[:5])

# 3. Уникальные значения
unique_items = set()
for row in np_df:
    for elem in row:
        unique_items.add(elem)
print("Уникальных товаров:", len(unique_items))
print(unique_items)

# 4. TransactionEncoder → one-hot матрица
te = TransactionEncoder()
te_array = te.fit(np_df).transform(np_df)
df_new = pd.DataFrame(te_array, columns=te.columns_)
print(df_new.head())
print(df_new.shape)

# 5. FPGrowth и FPmax
min_support = 0.05

fpg = fpgrowth(df_new, min_support=min_support, use_colnames=True)
fpg['length'] = fpg['itemsets'].apply(len)
print("\nFPGrowth:")
print(fpg.sort_values('support', ascending=False))

fpm = fpmax(df_new, min_support=min_support, use_colnames=True)
fpm['length'] = fpm['itemsets'].apply(len)
print("\nFPmax:")
print(fpm.sort_values('support', ascending=False))

# 6. Визуализация: зависимость числа наборов от min_support
min_support_range = np.arange(0.01, 0.4, 0.01)
fpg_counts, fpm_counts = [], []

for ms in min_support_range:
    fpg_counts.append(len(fpgrowth(df_new, min_support=ms, use_colnames=True)))
    fpm_counts.append(len(fpmax(df_new, min_support=ms, use_colnames=True)))

plt.figure(figsize=(10, 5))
plt.plot(min_support_range, fpg_counts, label='FPGrowth')
plt.plot(min_support_range, fpm_counts, label='FPmax')
plt.xlabel('min_support')
plt.ylabel('Количество наборов')
plt.title('Сравнение FPGrowth и FPmax')
plt.legend()
plt.grid(True)
plt.savefig('lab6_compare.png', dpi=150)
plt.show()

# 7. Граф ассоциаций (FPGrowth)
top = fpg[fpg['length'] >= 2].sort_values('support', ascending=False).head(15)

G = nx.Graph()
for _, row in top.iterrows():
    items = list(row['itemsets'])
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            G.add_edge(items[i], items[j], weight=row['support'])

plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, k=0.8, seed=42)
weights = [G[u][v]['weight'] * 10 for u, v in G.edges()]
nx.draw(G, pos, with_labels=True, node_color='lightblue',
        node_size=2000, font_size=10, width=weights, edge_color='gray')
plt.title('Граф ассоциаций (FPGrowth)')
plt.savefig('lab6_graph.png', dpi=150)
plt.show()

# 8. Большой датасет otchet6.csv
big = pd.read_csv('LR6/otchet6.csv', encoding='cp1251')
print(big.head())

# первый столбец — размер транзакции, остальные — товары
big_np = big.to_numpy()
big_transactions = [
    [elem.strip() for elem in row[1:] if isinstance(elem, str) and elem.strip() != '']
    for row in big_np
]
print("Транзакций:", len(big_transactions))
print(big_transactions[:3])

te2 = TransactionEncoder()
te2_array = te2.fit(big_transactions).transform(big_transactions)
big_df = pd.DataFrame(te2_array, columns=te2.columns_)
print(big_df.shape)

big_fpg = fpgrowth(big_df, min_support=0.02, use_colnames=True)
big_fpg['length'] = big_fpg['itemsets'].apply(len)
print(big_fpg.sort_values('support', ascending=False).head(10))

big_fpm = fpmax(big_df, min_support=0.02, use_colnames=True)
big_fpm['length'] = big_fpm['itemsets'].apply(len)
print(big_fpm.sort_values('support', ascending=False).head(10))