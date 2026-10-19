import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Загрузка
df = pd.read_csv('LR3/lab3.csv', encoding='cp1251')
print(df.head())

# 2. Распределение переменных
plt.hist(df['income'], bins=30, color='black', alpha=0.8)
plt.xlabel('income'); plt.ylabel('spending_rating')
plt.title('spending_rating based on income')

# 3. Корреляция
print("age vs income:", df['age'].corr(df['income']))
print("age vs spending_rating:", df['age'].corr(df['spending_rating']))
print("income vs spending_rating:", df['income'].corr(df['spending_rating']))

# 4. Выбросы — ящик с усами
plt.boxplot(df['income'])
plt.ylabel('income'); plt.title('Income emissions analysis')
# 5. Категориальные переменные
print(df['gender'].value_counts())
df['gender'].value_counts().plot(kind='bar', color='steelblue')
plt.title('gender distribution'); 

# 6. Дешборд
plt.figure(figsize=(10, 8))

plt.subplot(2, 2, 1)
plt.hist(df['income'], bins=30, color='black', alpha=0.8)
plt.xlabel('income'); plt.ylabel('spending_rating')

plt.subplot(2, 2, 2)
plt.scatter(df['age'], df['income'], color='black')
plt.xlabel('age'); plt.ylabel('income')

plt.subplot(2, 2, 3)
plt.boxplot(df['income'])
plt.xlabel('income'); plt.title('income emissions analysis')

plt.subplot(2, 2, 4)
sns.heatmap(df.corr(numeric_only=True), annot=True, fmt='.2g')

plt.tight_layout()
plt.savefig('lab3_dashboard.png', dpi=150)