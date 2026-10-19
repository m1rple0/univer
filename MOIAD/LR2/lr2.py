import pandas as pd

# загрузка
df = pd.read_csv('LR2/lab2.csv', encoding='cp1251')
print(df.head())
print(df.info())

# переименование столбцов
df.columns = ['id', 'gender', 'age', 'income', 'spending_rating']
print(df.info())

# удаляем строки с пустым id
df = pd.read_csv('LR2/lab2.csv', encoding='cp1251')
df.columns = ['id', 'gender', 'age', 'income', 'spending_rating']
df.dropna(subset=['id'], inplace=True)

# пропуски в age
print(df[df['age'].isnull()])
m_age = round(df[df['gender'] == 'Male']['age'].mean())
f_age = round(df[df['gender'] == 'Female']['age'].mean())
print(m_age, f_age)
df.loc[(df['age'].isnull()) & (df['gender'] == 'Male'), 'age'] = m_age
df.loc[(df['age'].isnull()) & (df['gender'] == 'Female'), 'age'] = f_age

# пропуски в income
print(df[df['income'].isnull()])
m_inc = round(df[df['gender'] == 'Male']['income'].mean())
f_inc = round(df[df['gender'] == 'Female']['income'].mean())
print(m_inc, f_inc)
df.loc[(df['income'].isnull()) & (df['gender'] == 'Male'), 'income'] = m_inc
df.loc[(df['income'].isnull()) & (df['gender'] == 'Female'), 'income'] = f_inc

# дубликаты
print(df[df.duplicated()])
print(df.duplicated().sum())
df = df.drop_duplicates().reset_index(drop=True)

# приводим числа к int
for c in ['id', 'age', 'income', 'spending_rating']:
    df[c] = df[c].astype(int)

print(df.head())
print(df.dtypes)

# сохраняем
df.to_csv('processed_final.csv', index=False)