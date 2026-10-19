import pandas as pd
import numpy as np
import nltk
import pymorphy2
from matplotlib import pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from wordcloud import WordCloud

# если nltk ещё не качал ресурсы — раскомментируй один раз:
# nltk.download('punkt')
# nltk.download('stopwords')

# 1. Загрузка
df = pd.read_csv('LR5/lab5.csv', encoding='cp1251')
print(df.head())

# 2. Уникальные id и продукты
ids = list(set(df['id']))
products = list(set(df['product'].str.strip()))
print("Покупателей:", len(ids))
print("Продуктов:", len(products))
print(products)

# 3. Новый датасет: список товаров по каждому покупателю
all_product = [
    [p.strip() for p in df[df['id'] == i]['product']]
    for i in ids
]
print(all_product[:3])

# 4. Облако слов на «сырых» данных
text = " ".join(df['product'].str.strip())
cloud = WordCloud(width=800, height=400,
                  background_color='black').generate(text)

plt.figure(figsize=(10, 5))
plt.imshow(cloud)
plt.axis('off')
plt.savefig('cloud_raw.png', dpi=150)
plt.show()

# 5. Стоп-слова + лемматизация, новое облако
stop_words = set(stopwords.words('russian'))
stop_words |= {'a', 'an', 'the', 'milk', 'bread'}  # свои стоп-слова

tokens = word_tokenize(text)
morph = pymorphy2.MorphAnalyzer()

lemmas = [
    morph.parse(w)[0].normal_form
    for w in tokens
    if w.isalpha() and w.lower() not in stop_words
]
clean_text = " ".join(lemmas)

cloud2 = WordCloud(width=800, height=400,
                   background_color='white',
                   stopwords=stop_words).generate(clean_text)

plt.figure(figsize=(10, 5))
plt.imshow(cloud2)
plt.axis('off')
plt.savefig('cloud_clean.png', dpi=150)
plt.show()

# 6. Работа с большим датасетом «Для отчета.csv»
big = pd.read_csv('LR5/Для отчета.csv', encoding='cp1251',
                  header=None, names=['date', 'id', 'product'])
print(big.head())

# уникальные товары
big_products = big['product'].dropna().str.strip().unique()
print("Уникальных товаров:", len(big_products))

# облако слов
big_text = " ".join(big['product'].dropna().str.strip())
cloud3 = WordCloud(width=1200, height=600,
                   background_color='black').generate(big_text)

plt.figure(figsize=(14, 7))
plt.imshow(cloud3)
plt.axis('off')
plt.savefig('cloud_big.png', dpi=150)
plt.show()

# частотный анализ топ-20 товаров
freq = big['product'].str.strip().value_counts().head(20)
print(freq)

freq.plot(kind='barh', figsize=(10, 6), color='steelblue')
plt.gca().invert_yaxis()
plt.title('Топ-20 товаров')
plt.tight_layout()
plt.savefig('top20.png', dpi=150)
plt.show()