import json
import csv
import time
import requests



for page in range(513):
    page = page + 1
    url = f"https://koreanname.me/api/rank/2008/2024/{page}"
    print("현재 페이지:", page)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        names = [entry['name'] for entry in data['male']]
        with open("save_name.txt", "a", encoding='utf-8') as file:
            for name in names:
                file.write(name + "\n")

    else:
        print(f"파일을 열지 못했습니다{page}, 코드오류{response.status_code}")


print("파일 저장 완료")

