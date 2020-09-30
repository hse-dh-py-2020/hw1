# Задание 1
import string
import csv
import json
import sys
import pymorphy2
import requests

try:
    with open('dom.txt') as f:
        text = f.read()
except IOError as e:
    print('Не удалось открыть файл с текстом: ', e)
    sys.exit()


def preprocess_text(text):
    text_lower = text.lower()

    # remove punctuation
    text_lower_no_punct = text_lower.translate(
        text_lower.maketrans('', '', string.punctuation))

    # weird way to remove tags without regexps and parsing
    text_no_latin = text_lower_no_punct.translate(
        text_lower.maketrans('', '', string.ascii_lowercase))

    # tokenize text
    tokens = text_no_latin.split()

    # remove escape-sequences (like '\ufeff' in the beginning of the file) and tags
    return list(filter(lambda t: t.isalnum(), tokens))


filtered_tokens = preprocess_text(text)

# create frequency dictionary


def create_freq_dict(tokens):
    freq_dict = {}
    for t in tokens:
        if t in freq_dict:
            freq_dict[t] += 1
        else:
            freq_dict[t] = 1
    return freq_dict


freq_dict = create_freq_dict(filtered_tokens)

# write frequncy dictionary to csv
try:
    with open('freq_dict.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(('Слово', 'Число употреблений'))
        for token, freq in freq_dict.items():
            writer.writerow((token, freq))
except IOError as e:
    print('Не удалось записать csv-файл: ', e)

# ===========================================================================
# Задание 2

# initialize pymorphy
morph = pymorphy2.MorphAnalyzer()

# lemmatize tokens
lemmas = list(map(lambda t: morph.parse(t)[0].normal_form, filtered_tokens))

# find lemmas with exact 2 cyrillic 'o'


def words_with_two_o(word):
    count = 0
    for c in list(word):
        if c == 'о':
            count += 1
    if count == 2:
        return True
    else:
        return False


#lemmas_two_o = list(filter(lambda l: words_with_two_o(l), lemmas))
unique_lemmas_two_o = list(set(filter(lambda l: words_with_two_o(l), lemmas)))

# write list of lemmas with 2 'о' to a file
try:
    with open('lemmas_with_two_o.txt', 'w') as f:
        for l in unique_lemmas_two_o:
            f.write('%s\n' % l)
except IOError as e:
    print('Не удалось записать txt-файл: ', e)


# load file by given url
url = 'http://lib.ru/POEZIQ/PESSOA/lirika.txt'

responce = requests.get(url)
text2 = responce.text

# preprocess text
filtered_tokens2 = preprocess_text(text2)

# create frequency dictionary for the 2nd text
freq_dict2 = create_freq_dict(filtered_tokens2)

# write frequency dictionary to json
try:
    with open('freq_dict2.json', 'w', encoding='utf8') as f:
        json.dump(freq_dict2, f, ensure_ascii=False)
except IOError as e:
    print('Не удалось записать json-файл: ', e)
