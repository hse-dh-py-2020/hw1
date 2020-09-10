#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re
from collections import Counter

def read_from_file(name): #функция, которая читает текст из файла
    file = open(name, 'r', encoding='utf-8')
    text = file.read()
    file.close()
    return text

def get_words(text): #функция, которая создает и возвращает список слов из текста
    return [word.lower() for word in re.findall(r'[а-яёА-ЯЁa-zA-Z-]+', text) if word[0] != '-']

def csv_file_content(text): #функция, которая создает из списка слов частотный словарь и преобразует его в удобный вид для записи в .csv
    wordlist = get_words(text)
    freqdict = Counter(wordlist).most_common()
    content = 'Слово;Частотность\n'
    content += '\n'.join([';'.join([x[0],str(x[1])]) for x in freqdict])
    content += '\n'
    return content

def write_to_file(name, content): #функция, которая записывает переданные ей данные в файл заданного формата
    file = open(name, 'w')
    file.write(content)
    file.close

def main():
    wdir = input('Рабочая директория> ')
    os.chdir(wdir)
    name = input('Имя файла (без расширения)> ')
    text = read_from_file(name + '.txt')

    write_to_file(name+'.csv', csv_file_content(text))
    print('Частотный словарь словоформ создан')

main()