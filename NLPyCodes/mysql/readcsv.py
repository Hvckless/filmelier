import time

start_time = time.time()

filepath:str = "../../csvfile/FBI_ 마약전쟁_categorized_words.csv"

with open(filepath, 'r', encoding="utf-8") as file:
    content = file.read()

print(content)

print(f"elapsed time : {time.time()-start_time}")