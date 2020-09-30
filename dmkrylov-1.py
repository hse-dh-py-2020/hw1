#!/usr/bin/env python
# coding: utf-8

# In[1]:


#1)
with open ("C:\\Users\\Arseny\\Desktop\\Downloads\\dom.txt", 'r', encoding='utf-8') as dom:
    dom = dom.read()

#1а)
dom = dom.lower()[8:]
print(dom)

#1б)
punct = "!\"#$%&'()*+,-./:;<=>?@[\]^_`…”{|}~„“«»†*–—/\-"
words = [x.strip(punct) for x in dom.split()]
print(' '.join(words))

#1в)
import csv
counts = {}
for word in words:
    if word in counts:
        counts[word] += 1
    else:
        counts[word] = 1
sorted_counts = (sorted(counts.items(), key=lambda x: x[1], reverse=True))[1:]
with open ("C:\\Users\\Arseny\\Desktop\\repository\\DH-homeworks\\word-frequency-pairs.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    for pair in sorted_counts:
        writer.writerow(pair)
print(sorted_counts)


#2a)
l_w=[]
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
for word in dom.split():
	l_w.append(morph.parse(word)[0].normal_form)
print(' '.join(l_w))


#2б)


import re
oo_words=[]
with open ("C:\\Users\\Arseny\\Desktop\\repository\\DH-homeworks\\oo.txt", 'w', encoding='utf8') as oo:
	for lemma in l_w:
		lemma = lemma.strip("!\"#$%&'()*+,-./:;<=>?@[\]^_`…”{|}~„“«»†*–—/\-")
		if (len(re.findall("о",lemma))==2) and (lemma not in oo_words):
			oo.write(lemma+'\n')
			oo_words.append(lemma)


print (oo_words)

#2в)
import urllib.request
lyrics = urllib.request.urlopen('http://lib.ru/POEZIQ/PESSOA/lirika.txt')
charset =(lyrics.info().get_content_charset())
document = lyrics.read().decode(charset)
document = re.sub('<.*>','',document)

document = document.lower()

#2г)
dictionary = []
for word in document.split():
	word = word.strip("!\"#$%&'()*+,-./:;<=>?@[\]^_`…”{|}~„“«»†*–—/\-")
	if morph.parse(word)[0].normal_form in dictionary:
		pass
	else:
		dictionary.append(morph.parse(word)[0].normal_form)
dictionary = sorted(dictionary)
print(dictionary)

#2д)

import json
with open('C:\\Users\\Arseny\\Desktop\\repository\\DH-homeworks\\dict.json', 'w', encoding='utf-8') as f:
    json.dump(dictionary, f, ensure_ascii=False)
