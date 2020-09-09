# часть 1
import string,re

with open("dom.txt", "r", encoding="utf-8-sig") as f:
    dom = f.read()
dom = dom.lower()

for c in string.punctuation + "—–“”…«»№":
    dom = dom.replace(c, "")
dom = re.sub(" +"," ",dom.replace('\n',' '))

dom_words = dom.split()
dom_dict = dict()
for word in dom_words:
    if word in dom_dict:
        dom_dict[word]+=1
    else: 
        dom_dict[word]=1
        
with open('dom.csv', 'w') as f:
    for key in dom_dict.keys():
        f.write(key+","+str(dom_dict[key])+"\n") 

#часть 2
from pymystem3 import Mystem

m = Mystem()
lemmas = m.lemmatize(dom)
print(''.join(lemmas))

# б) найти такие леммы (не исходные словоформы), в которых было бы две (не больше, не меньше) буквы «о» 
# здесь должен быть цикл, который пройдется по всем леммам и выберет те, где две "о", но я не смогла его написать 


import requests
url = "http://lib.ru/POEZIQ/PESSOA/lirika.txt"
r = requests.get(url, allow_redirects=True)
open('lirika.txt', 'w').write(r.text)

with open("lirika.txt", "r") as f:
    lirika = f.read()
    
for c in string.punctuation:
    lirika = lirika.replace(c, "")

lirika_word = lirika.split()
lirika_dict = dict()
for word in lirika_word:
    if word in lirika_dict:
        lirika_dict[word]+=1
    else:
        lirika_dict[word]=1

import json
with open('lirika.json', 'w', encoding='utf-8') as f:
    json.dump(lirika_dict, f, ensure_ascii=False)


























