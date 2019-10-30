import re
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from string import punctuation
from pymystem3 import Mystem

# откроем файл, в котором скачаны тексты: каждый отдельный текст начинается с сочетания @$%, поэтому разбиваем/сплитим по нему
with open("complaints300.txt", "r", encoding='utf-8') as f:
    data = f.readlines()
    for line in data:
        sentences = line.split("@$%")

# почистим получившийся список от кавычек и удалим то, что в результате чистки превратилось в пустую строку
pure_sentences = []
for sentence in sentences:
    sentence = re.sub('"', '', sentence)
    pure_sentences.append(sentence)
    for sentence in pure_sentences:
        if sentence == '':
            pure_sentences.remove(sentence)
# для дебага:
# print(pure_sentences)

# определим язык стопслов и добавим кастомные
stop_words = stopwords.words('russian')
stop_words.append('здравствуйте')
stop_words.append('здравствовать')

# инициализируем лемматизатор и список для итоговых текстов
mystem = Mystem()
final_texts = []

# проведем лемматизацию и соберем в итоговый список тексты без стопслов и пунктуации со словами в начальной форме в нижнем регистре
for sentence in pure_sentences:
    tokens = mystem.lemmatize(sentence.lower())
    filtered_tokens = []
    for token in tokens:
        if token not in stop_words and token.strip() not in punctuation and token != " ":
            filtered_tokens.append(token)
    filtered_str = ' '.join(filtered_tokens)
    final_texts.append(filtered_str)
# для дебага:
# print(final_texts)

# инициализируем векторизатор и посчитаем вектор для получившихся текстов
vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform(final_texts)
# для дебага:
names = vectorizer.get_feature_names()
# print(names)

# разложим вектор на матрицы
u, s, vh = np.linalg.svd(np.array(tfidf.todense()), full_matrices=False)
# или так:
# tfidf_array = scipy.sparse.spmatrix.toarray(tfidf)
# u, s, vh = np.linalg.svd(tfidf_array)

# для дебага:
# print(pd.DataFrame(vh, columns=vectorizer.get_feature_names()).loc[2,:])

# выберем номера тем для каждого текста, которые наиболее релевантны ему
themes = []
for i in range(len(u)):
    themes.append(list(u[i]).index(max(u[i])))
# для дебага:
print(themes)

# визуализация (у меня scientific mode в pycharm с выводом графиков)
df = pd.DataFrame(themes)
df.hist()
plt.show()





