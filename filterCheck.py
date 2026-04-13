#unzip book.epub
import ebooklib
from ebooklib import epub
import os
import re
import json

import warnings
warnings.filterwarnings("ignore")

bookNames = os.listdir("books")
filterListPunct = [" "]
spaceFilter = ["?","!","/"]
dashException = ["-"]
removeIfNotMiddle = ["'",'"']
""""#$%&'()*+/:;<=>@[\]^_{|}~`"""

#?? add rule to replace dashes - if one of the splitting words is small (less than 2 characters), we keep the word as it is, otherwise we keep it

books = open("books.json","r")
books = json.load(books)

for bookName in bookNames:
    wordFrequency = {}
    print(bookName)
    bookName = f"books/{bookName}"
    book = epub.read_epub(bookName)
    text = []
    pureText = []
    index = 0

    for doc in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        t = str(doc.content)

        #filter out tags / control characters / punctuation
        t = re.sub('<.*?>'," ", t)
        t = re.sub('{.*?}'," ", t)
        t = t.replace('\\r',"").replace('\\n',"")

        t = t.encode().decode("unicode-escape").encode("latin-1").decode("utf-8")

        t = t.replace(','," ")
        t = ' '.join(t.split())

        #seperate to sentences
        t = re.split('([\?|.|!])',t) + [""]
        t = [t[x+0] + t[x+1] for x in range(0, len(t), 2)]

        pure = t.copy()

        t = [x.replace("’","'").replace('“','"').replace('”','"').replace("—","-") for x in t]

        for r in spaceFilter:
            t = [x.replace(r, " ") for x in t]

        t = [x.strip().lower() for x in t]

        #check for remove if not middle
        for r in removeIfNotMiddle:
            t = [re.sub(f"\s{r}"," ",x) for x in t]
            t = [re.sub(f"{r}\s"," ",x) for x in t]

            t = [x[1:] if len(x) > 0 and x[0] == r else x for x in t ]
            t = [x[:-1] if len(x) != 0  and x[-1] == r else x for x in t ]

        #remove dashes if not coincided with very short length words
        for r in dashException:
            for i in range(len(t)):
                w = t[i].split()
                for x in range(len(w)):
                    wordBlurb = [y for y in w[x].split(r) if y.strip() != ""]
                    if len(wordBlurb) > 1:
                        if min([len(x) for x in wordBlurb]) > 1:
                            w[x] = w[x].replace(r," ")

                    w[x] = w[x].strip()
                
                    if len(w[x]) > 0 and w[x][-1] == r:
                        w[x] = w[x][:-1]
                    
                    if len(w[x]) > 0 and w[x][0] == r:
                        w[x] = w[x][1:]

                t[i] = " ".join(w)

        t = ["".join(y for y in x if y.upper() != y.lower() or y in filterListPunct+dashException+removeIfNotMiddle or y.isnumeric()).lower().strip() for x in t]
        t = [" ".join([x for x in x.split() if not x.isnumeric()]) for x in t]
        
        text.append(t.copy())
        pureText.append(pure.copy())

    wordsAll = []

    #process words
    for chapterIndex in range(len(text)):
        for sentencePos in range(len(text[chapterIndex])):
            for word in text[chapterIndex][sentencePos].split():

                word = "".join(x for x in word if x.isalnum())
                if word == "":
                    continue

                if word not in wordsAll:
                    wordsAll.append(word)

    wordsAll = sorted(wordsAll)

    books.append({'name':"",
                  "author":"",
                  "words":wordsAll.copy(),
                  "rating":3})
    
    #log new words
    f = open('books.json',"w", encoding="utf-8")
    json.dump(books, f, indent=4, ensure_ascii=False)
    f.close()

    input("Done")