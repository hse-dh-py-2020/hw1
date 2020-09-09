#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re
from collections import Counter
import pymorphy2
import requests
from bs4 import BeautifulSoup
import json

def ReadFromFile(Name): #функция, которая читает текст из файла
    f = open(Name, 'r', encoding='utf-8')
    s = f.read()
    f.close()
    return s

def GetWords(s): #функция, которая создает и возвращает список слов из текста
    return [x.lower() for x in re.findall(r'[а-яёА-ЯЁa-zA-Z-]+', s) if x[0] != '-']

def OLemmaList(s): #функция, которая создает из списка слов список лемм, где ровно 2 "о", и преобразует его в удобный вид для записи в .txt
    l = GetWords(s)
    morph = pymorphy2.MorphAnalyzer()
    return '\n'.join([morph.parse(w)[0].normal_form for w in l if len(re.findall('о',morph.parse(w)[0].normal_form))==2])

def CSVFileContent(s): #функция, которая создает из списка слов частотный словарь и преобразует его в удобный вид для записи в .csv
    l = GetWords(s)
    L = Counter(l).most_common()
    S = 'Слово;Частотность\n'
    S += '\n'.join([';'.join([x[0],str(x[1])]) for x in L])
    S += '\n'
    return S

def JSONfileContent(Link): #функция, которая скачивает текст с web-страницы, делит его на слова, создает частотный словарь и записывает его в .json
    s = BeautifulSoup(requests.get(Link).text, "html.parser").getText()
    l = GetWords(s)
    L = Counter(l)
    jsonData = json.dumps(L, ensure_ascii=False)
    return jsonData

def WriteToFile(Name, s, filetype): #функция, которая записывает переданные ей данные в файл заданного формата
    f = open(Name + filetype, 'w')
    f.write(s)
    f.close

def Main():
    Dir = input('Рабочая директория> ')
    os.chdir(Dir)
    Name = input('Имя файла (без расширения)> ')
    s = ReadFromFile(Name + '.txt')

    WriteToFile(Name+'_csv', CSVFileContent(s), '.csv')
    print('Частотный словарь словоформ создан')

    WriteToFile(Name+'_lemms', OLemmaList(s), '.txt')
    print('Cписок лемм создан')

    Link = 'http://lib.ru/POEZIQ/PESSOA/lirika.txt'

    WriteToFile(Name+'_json', JSONfileContent(Link), '.json')
    print('JSON-словарь создан')

Main()