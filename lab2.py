# Векторное представление слов

import gensim
import re
from math import comb

from itertools import combinations

pat = re.compile("(.*)_NOUN")
word2vec = gensim.models.KeyedVectors.load_word2vec_format('cbow.txt', binary=False)

# фильтруем слова, оставляем только существительные
nouns = [
    word for word in word2vec.index_to_key
    if pat.fullmatch(word)
]

model = gensim.models.KeyedVectors(vector_size=word2vec.vector_size)
model.add_vectors(nouns, word2vec[nouns])

def find_combination(t1, t2):

    words1 = [
        word for word, _ in model.most_similar(t1, topn=100)
    ]

    words2 = [
        word for word, _ in model.most_similar(t2, topn=100)
    ]

    # объединяем и исключаем целевые слова
    candidates = list(
        (set(words1) | set(words2)) - {t1, t2}
    )

    total = comb(len(candidates), 2)

    # перебираем пары
    for i, (w1, w2) in enumerate(combinations(candidates, 2)):

        print(f"\rПрогресс: {i + 1}/{total}", end="", flush=True)

        # Пробуем различные знаки линейной комбинации
        for positive, negative in [
            ([w1, w2], []),
            ([w1], [w2]),
            ([w2], [w1])
        ]:
            result = model.most_similar(
                positive=positive,
                negative=negative,
                topn=10
            )

            result_words = [word for word, _ in result]

            if t1 in result_words and t2 in result_words:
                print()
                print(
                    "Комбинация: ", 
                    " + ".join(["", *positive]) + " - ".join(["", *negative])
                    )
                
                print("Ближайшие слова, ТОП-10: ")
                for res in result:
                    print(res) 
                return

target1 = "король_NOUN"
target2 = "церковь_NOUN"

find_combination(target1, target2)