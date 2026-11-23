# Предобработка текста

import sys
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import pymorphy3

# nltk.download('punkt')
morph = pymorphy3.MorphAnalyzer()

text = sys.stdin.read()

if not text.strip():
    print("Передайте содержимое текста в программу: py -u lab1.py < text.txt")
    sys.exit()

# with open('Преступление и наказание первая часть глава первая.txt', 'r') as file:
#     text = file.read()

# проводим сегментацию
sentences = sent_tokenize(text, language='russian')

allowed_pos = {'NOUN', 'ADJF'}

def agree_condition(tag1, tag2):
        # у двух слов определено число либо число одинаковое
        same_number = (
            tag1.number is not None
            and tag2.number is not None
            and tag1.number == tag2.number
        )

        # у двух слов определен падеж либо падеж одинаковый
        same_case = (
            tag1.case is not None
            and tag2.case is not None
            and tag1.case == tag2.case
        )

        # либо два слова в множ. числе, либо род у двух слов одинаковый (если род определен) 
        same_gender = (
            (tag1.number == 'plur' and tag2.number == 'plur')
            or (
                tag1.gender is not None
                and tag2.gender is not None
                and tag1.gender == tag2.gender
            )
        )

        return same_number and same_case and same_gender      

# основной цикл
for sentence in sentences:
    # токенизация предложения
    tokens = word_tokenize(sentence, language='russian')

    for i in range(1, len(tokens)):
        first_parses = [
             p for p in morph.parse(tokens[i-1]) 
             if p.tag.POS in allowed_pos
             and 'Apro' not in p.tag 
             and p.score >= 0.1
             ]
        second_parses = [
             p for p in morph.parse(tokens[i])
             if p.tag.POS in allowed_pos
             and 'Apro' not in p.tag
             and p.score >= 0.1
             ]

        candidates = [
            (p1, p2)
            for p1 in first_parses
            for p2 in second_parses
            if agree_condition(p1.tag, p2.tag)
        ]

        if candidates:
            p1, p2 = max(
                candidates,
                key=lambda x: (
                    x[0].score * x[1].score,
                    x[0].tag.POS == 'ADJF' and x[1].tag.POS == 'NOUN',
                    x[0].tag.POS == 'NOUN' and x[1].tag.POS == 'ADJF',
                    x[0].tag.POS == 'ADJF' and x[1].tag.POS == 'ADJF',
                    x[0].tag.POS == 'NOUN' and x[1].tag.POS == 'NOUN',
                )
            )

            print(p1.normal_form, p2.normal_form)