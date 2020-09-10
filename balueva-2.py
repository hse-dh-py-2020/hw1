#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re
from collections import Counter
import pymorphy2
import requests
from bs4 import BeautifulSoup
import json

def read_from_file(name): #функция, которая читает текст из файла
    file = open(name, 'r', encoding='utf-8')
    text = file.read()
    file.close()
    return text

def get_words(text): #функция, которая создает и возвращает список слов из текста
    return [word.lower() for word in re.findall(r'[а-яёА-ЯЁa-zA-Z-]+', text) if word[0] != '-']

def o_lemma_list(s): #функция, которая создает из списка слов список лемм, где ровно 2 "о", и преобразует его в удобный вид для записи в .txt
    wordlist = get_words(s)
    morph = pymorphy2.MorphAnalyzer()
    lemmlist = []
    for w in wordlist:
        lemma = morph.parse(w)[0].normal_form
        if len(re.findall('о', lemma)) == 2:
            lemmlist.append(lemma)
    return '\n'.join(lemmlist)

def json_file_content(link): #функция, которая скачивает текст с web-страницы, делит его на слова, создает частотный словарь и записывает его в .json
    text = BeautifulSoup(requests.get(link).text, "html.parser").getText()
    wordlist = get_words(text)
    freqdict = Counter(wordlist)
    json_data = json.dumps(freqdict, ensure_ascii=False)
    return json_data

def write_to_file(name, s, filetype): #функция, которая записывает переданные ей данные в файл заданного формата
    file = open(name + filetype, 'w')
    file.write(s)
    file.close

def main():
    wdir = input('Рабочая директория> ')
    os.chdir(wdir)
    name = input('Имя файла (без расширения)> ')
    text = read_from_file(name + '.txt')

    write_to_file(name+'_lemms', o_lemma_list(text), '.txt')
    print('Cписок лемм создан')

    link = 'http://lib.ru/POEZIQ/PESSOA/lirika.txt'

    write_to_file(name+'_json', json_file_content(link), '.json')
    print('JSON-словарь создан')

main()