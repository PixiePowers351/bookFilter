import json

books = open("books.json")
books = json.load(books)

#check words that appear in both
wordMap = {}

for book in books:
    for word in book['words']:
        if word not in wordMap:
            wordMap[word] = {"frequency":1,"score":book['rating'],'book':[book['name'] + " by " + book['author']]}
        
        else:
            wordMap[word]["frequency"] += 1
            wordMap[word]["score"] = ((wordMap[word]["frequency"]-1) * wordMap[word]["score"] + book["rating"]) / wordMap[word]["frequency"]
            wordMap[word]['book'].append(book['name'] + " by " + book['author'])

wordMap = {x:wordMap[x] for x in sorted(wordMap.keys(), key=lambda x:wordMap[x]["score"], reverse=False)}
""