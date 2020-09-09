import re
import codecs
import json

import pymorphy2
import requests

from collections import Counter
from bs4 import BeautifulSoup

def main():
  morph = pymorphy2.MorphAnalyzer()

  with open("dom.txt", "r", encoding="utf-8") as infile:
    text = infile.read()
  
  text = re.sub(r"[^\w]|\n", " ", text)
  
  s = set()
  for word in re.split(r" +", text):
    lemma = morph.parse(word)[0].normal_form.lower()
    s.add(lemma)
  
  oo_words = sorted([w for w in s if re.sub(r"[^о]", "", w) == "оо"])
  with open("oo_list.txt", "w", encoding="utf-8") as ool:
    ool.write("\n".join(oo_words))
  
  urlin = "http://lib.ru/POEZIQ/PESSOA/lirika.txt"
  res = requests.get(urlin)
  Html = res.text
  soup = BeautifulSoup(Html)
  webtext = soup.get_text()
  delim = "=== [ Ф. ПЕССОА ] ====================================="
  webtext = webtext[webtext.find(delim) + len(delim):]
  
  webtext = re.sub(r"[^\w]|\n", " ", webtext.lower())
  lemma_list = [morph.parse(word)[0].normal_form.lower() for word in re.split(r" +", text) if word]

  c = Counter(lemma_list)
  o = {}

  for lemma in set(lemma_list):
    o[lemma] = c[lemma]
  
  with codecs.open('pessoa_dict.json', 'w', encoding='utf-8') as f:
    json.dump(o, f, ensure_ascii=False, sort_keys=True,
              indent=4, separators=(',', ': '))

  return None

if __name__ == "__main__":
  main()