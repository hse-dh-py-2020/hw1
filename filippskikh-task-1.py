import string
import re
from pymystem3 import Mystem
import requests
import json

m = Mystem()

def get_words_from_text(text):
    res = re.sub('[^a-zA-Zа-яА-Я0-9 ]', ' ', text.lower())
    res = re.sub('\s+', ' ', res)
    return res.split()


def get_word_frequency(words):
    frequency = {}
    for w in words:
        if w in frequency:
            frequency[w] += 1
        else:
            frequency[w] = 1
    return frequency


def has_exactly_two_os(w):
    cnt = 0
    for c in w:
        if c == 'о':
            cnt += 1
    return cnt == 2

with open('dom.txt', 'r') as f:
    text = f.read()

words = get_words_from_text(text)
print(len(words))
print(len(set(words)))

frequency = get_word_frequency(words)

with open('word-frequency.csv', 'w+') as f:
    for w in frequency:
        cnt = frequency[w]
        f.write('%s,%s\n' % (w, cnt))
    f.flush()
    f.close()

lemmas = []
for w in words:
    ls = m.lemmatize(w)
    for l in ls:
        if l.isalpha():
            lemmas.append(l)

has_two_os = [w for w in lemmas if has_exactly_two_os(w)]
print(len(has_two_os), has_two_os)

with open("os.txt", 'w+') as f:
    for w in has_two_os:
        f.write('%s\n' % w)
    f.flush()
    f.close()

lirika_response = requests.get('http://lib.ru/POEZIQ/PESSOA/lirika.txt')
lirika_response.text
lirika = re.sub('<[^<]+?>', ' ', lirika_response.text)

lirika_words = get_words_from_text(lirika)
lirika_frequency = get_word_frequency(lirika_words)

with open('lirika-word-frequency.json', 'w+') as f:
    f.write(json.dumps(lirika_frequency))
    f.flush()
    f.close()