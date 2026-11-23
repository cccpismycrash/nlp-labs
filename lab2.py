# Векторное представление слов

import gensim
import re
import random

from math import comb
from itertools import combinations

pat = re.compile("(.*)_NOUN")

model = gensim.models.KeyedVectors.load("nouns.kv", mmap="r")

def find_combination(t1, t2, exclude: list, rand=False, random_state=None):

    words1 = [
        word for word, _ in model.most_similar(t1, topn=100)
    ]

    words2 = [
        word for word, _ in model.most_similar(t2, topn=100)
    ]

    # объединяем и исключаем целевые слова
    candidates = list(
        (set(words1) | set(words2)) - {t1, t2, *exclude}
    )

    candidates = sorted(candidates)

    if rand:
        rng = random.Random(random_state)
        rng.shuffle(candidates)

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

while True:
    try:
        target1 = input("Введите первое слово: ")
        target2 = input("Введите второе слово: ")
        exclude = input("Введите слова для исключения (через пробел): ").strip().lower()

        target1 += "_NOUN"
        target2 += "_NOUN"
        exclude = [word + "_NOUN" for word in exclude.split()]
        rand = input("Перемешать? (y/n): ").strip().lower() == "y"
        random_state = None

        if rand:
            random_state = int(input("Seed (если "", то случайный сид): ").strip())

        print()
        find_combination(target1, target2, [], rand, random_state)
        print()

    except KeyboardInterrupt:
        print("\nОкончание работы")
        break