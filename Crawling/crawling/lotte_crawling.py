from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time

# 드라이버 설정
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
#options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(service=service, options=options)


url = "https://www.lottecinema.co.kr/NLCHS/Movie/MovieDetailView?movie=21315"
driver.get(url)
time.sleep(3)


try:
    review_btn = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.CSS_SELECTOR, "li.active > button"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", review_btn)
    driver.execute_script("arguments[0].click();", review_btn)
    print("'리뷰' 버튼 클릭 완료")
    time.sleep(2)
except Exception as e:
    print(f"'리뷰' 버튼 클릭 중 오류 발생: {e}")


def next_button(clicks):
    for i in range(clicks):
        try:
            print("=============================",ec.element_to_be_clickable((By.XPATH, '//button[@style="width: 490px; left: 50%; margin-left: 0px;"]')))
            next_btn = WebDriverWait(driver, 10).until(
                ec.element_to_be_clickable((By.XPATH, '//button[@style="width: 490px; left: 50%; margin-left: 0px;"]'))
            )

            driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
            time.sleep(10)  # 버튼이 완전히 로드되도록 잠시 대기
            driver.execute_script("arguments[0].click();", next_btn)
            print(f"{i+1}번째 '더보기' 버튼 클릭 완료")
            time.sleep(2)  # 댓글이 로드될 시간을 기다림
        except Exception as e:
            print(f"버튼 클릭 중 오류 발생: {e}")
            break



next_button(5)


def get_comments():
    comments = []
    try:
        # 댓글 요소 가져오기
        title_elements = WebDriverWait(driver, 10).until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, "div.review_info"))
        )
        print(f"댓글 {len(title_elements)}개 발견")
        for element in title_elements:
            html_content = element.get_attribute("outerHTML")
            print(f"댓글 HTML: {html_content}")
            comments.append(element.get_attribute('textContent'))
    except Exception as e:
        print(f"댓글 스크래핑 중 오류 발생: {e}")
    return comments


all_comments = get_comments()


for i, comment in enumerate(all_comments, 1):
    print(f"댓글 {i}: {comment}")


with open("Sucabaty_Soccer_lotte.txt", "w", encoding="utf-8") as file:
    for comment in all_comments:
        file.write(comment + "\n")




