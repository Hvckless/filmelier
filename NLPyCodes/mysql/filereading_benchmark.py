import os
import time

filepath:str = "../../csvfile/"
movielist = []

start_time = time.time()

for filename in os.listdir(filepath):
    movielist.append(filename.split("_categorized_words.csv")[0])


contentlist = []
for movie in movielist:
    with open(filepath+movie+"_categorized_words.csv", 'r', encoding="utf-8") as file:
        contentlist.append(file.read())


print(len(contentlist))

print(f"elapsed time : {time.time()-start_time}")