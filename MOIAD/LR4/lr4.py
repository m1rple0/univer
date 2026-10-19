import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA, FactorAnalysis

df = pd.read_csv('LR4/lab4.csv', encoding='cp1251')
print(df.info())

# класс — пол, признаки — остальное
X = df[['age', 'income', 'spending_rating']].values
y = df['gender'].values

# масштабируем
X = MinMaxScaler().fit_transform(X)
print(X[:5])

# PCA
pca = PCA()
X_pca = pca.fit_transform(X)
print(pca.explained_variance_ratio_)
print(pca.singular_values_)

# FA
fa = FactorAnalysis(n_components=3, random_state=0)
X_fa = fa.fit_transform(X)
print(fa.components_)

# дисперсия для FA считаем сами
corr = np.corrcoef(X, rowvar=False)
vals = np.sort(np.linalg.eigvalsh(corr))[::-1]
print(vals / vals.sum())

# графики
fig, ax = plt.subplots(1, 2, figsize=(13, 6))

for g, c in [('Male', 'r'), ('Female', 'g')]:
    m = y == g
    ax[0].scatter(X_pca[m, 0], X_pca[m, 1], c=c, label=g)
    ax[1].scatter(X_fa[m, 0], X_fa[m, 1], c=c, label=g)

ax[0].set_title('PCA'); ax[0].set_xlabel('PC1'); ax[0].set_ylabel('PC2')
ax[1].set_title('FA');  ax[1].set_xlabel('FA1'); ax[1].set_ylabel('FA2')
ax[0].legend(); ax[1].legend()
plt.tight_layout()
plt.savefig('lab4.png', dpi=150)

# таблицы
pca_df = pd.DataFrame(X_pca[:, :2], columns=['PC1', 'PC2'])
pca_df['gender'] = y
fa_df = pd.DataFrame(X_fa[:, :2], columns=['FA1', 'FA2'])
fa_df['gender'] = y
print(pca_df.head())
print(fa_df.head())