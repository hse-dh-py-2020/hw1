import re
from collections import Counter

def main():
  with open("dom.txt", "r", encoding="utf-8") as infile:
    text = infile.read()
  text = re.sub(r"[^\w]|\n", " ", text.lower())
  c = Counter(re.split(r" +", text))
  with open("freq_dict.csv", "w", encoding="utf-8") as fd:
    fd.write("Token,Frequency\n")
    for token, count in c.most_common():
      fd.write(token + "," + str(count) + "\n")
  return None

if __name__ == "__main__":
  main()