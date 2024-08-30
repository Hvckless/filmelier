from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
import time

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=service, options=options)


url = "http://www.cgv.co.kr/movies/detail-view/?midx=88437"
driver.get(url)

print("페이지 로드")
time.sleep(3)

def get_comment():
    comments = []
    try:
        title = WebDriverWait(driver, 10).until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, "div.box-comment > p"))
        )
        print(f"댓글 {len(title)}개 발견")
        for article in title:
            comments.append(article.text)
    except Exception as e:
        print(f"댓글 오류 발생:{e}")
    return comments

all_comments = []
for page in range(1,11):
    print("페이지 스크랩")

    comments = get_comment()
    all_comments.extend(comments)

    try:
        next_btn = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.CSS_SELECTOR,f"#paging_point > li:nth-child({page+1}) > a"))
        )
        next_btn.click()
        time.sleep(3)
    except Exception as e:
        print(f"{page}에서 버튼이 없습니다 :{e}")
        break

for i, comment in enumerate(all_comments, 1):
    print(f"댓글{i}: {comment}")

with open("comments1.txt", "w", encoding="utf-8") as file:
    for comment in all_comments:
        file.write(comment + "\n")

driver.quit()

