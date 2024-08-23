import pandas as pd
from collections import defaultdict
import math

df = pd.read_csv('output.csv')

with open('martian.txt', 'r', encoding='utf-8') as file:
    movieDict = file.read()

    items = movieDict.split(",")


definedCategory = defaultdict(lambda: [0, ""])
totCnt = 0
definedList = []
undefinedList = []

for item in items:
    if item in df['term'].values:
        filtered_df = df[df['term'] == item]

        for context in filtered_df['category'].tolist():
            definedCategory[context][0] += 1
            totCnt += 1
        
        definedList.append(item)
    else:
        undefinedList.append(item)

for key in definedCategory:
    definedCategory[key][1] = str(math.floor((definedCategory[key][0]/totCnt)*1000)/1000)+"%"



print("등장빈도")
print(definedCategory)
print("정의된 단어")
print(definedList)
print("정의되지 않은 단어")
print(undefinedList)