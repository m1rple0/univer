import pandas as pd
import numpy as np
from sklearn import preprocessing
import matplotlib.pyplot as plt

df = pd.read_csv('LR1/lab1.csv', encoding='cp1251')
print(df.head(), df.shape, sep='\n')

# 1. normalize для age
age = np.array(df['age'])
norm = preprocessing.normalize([age])
print(norm[0][:10], norm[0] @ norm[0])

# 2. normalize по столбцам и строкам
print(preprocessing.normalize(df, axis=0)[:3])
print(preprocessing.normalize(df, axis=1)[:3])

# 3. MinMaxScaler (0, 3)
mm = preprocessing.MinMaxScaler(feature_range=(0, 3))
mm_df = pd.DataFrame(mm.fit_transform(df), columns=df.columns)
print(mm_df.head())

# 4. MaxAbsScaler (-1, 1)
ma = preprocessing.MaxAbsScaler()
ma_df = pd.DataFrame(ma.fit_transform(df), columns=df.columns)
print(ma_df.head())

# 5. RobustScaler (25, 75)
rb = preprocessing.RobustScaler(quantile_range=(25.0, 75.0))
rb_df = pd.DataFrame(rb.fit_transform(df), columns=df.columns)
print(rb_df.head())

# 6. QuantileTransformer (uniform)
qt = preprocessing.QuantileTransformer(n_quantiles=100,
                                       output_distribution='uniform',
                                       random_state=42)
qt_df = pd.DataFrame(qt.fit_transform(df), columns=df.columns)
print(qt_df.head())

# 7. Графики
fig, ax = plt.subplots(2, 2, figsize=(12, 9))
ax[0, 0].hist(df['age'], bins=20, color='steelblue'); ax[0, 0].set_title('исходные')
ax[0, 1].hist(mm_df['age'], bins=20, color='orange');   ax[0, 1].set_title('MinMax')
ax[1, 0].hist(ma_df['age'], bins=20, color='red');      ax[1, 0].set_title('MaxAbs')
ax[1, 1].hist(qt_df['age'], bins=20, color='green');    ax[1, 1].set_title('Quantile')
plt.tight_layout(); plt.savefig('lab1_visualization.png', dpi=150);

# 8. Сводка
print(pd.DataFrame({
    'Исходные': [f"{df[c].min():.0f}..{df[c].max():.0f}" for c in df.columns],
    'MinMax':   [f"{mm_df[c].min():.2f}..{mm_df[c].max():.2f}" for c in df.columns],
    'MaxAbs':   [f"{ma_df[c].min():.2f}..{ma_df[c].max():.2f}" for c in df.columns],
    'Robust':   [f"{rb_df[c].min():.2f}..{rb_df[c].max():.2f}" for c in df.columns],
    'Quantile': [f"{qt_df[c].min():.2f}..{qt_df[c].max():.2f}" for c in df.columns],
}, index=df.columns))
