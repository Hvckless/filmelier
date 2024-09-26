from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import os
import requests
import shutil

option = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())
option.add_argument("--headless")

driver = webdriver.Chrome(service=service, options=option)
# file_path = 영화 목록 파일
# 영화 목록 파일이 있는 경로만 복사 해서 변경 해주면 된다.
file_path = os.path.join(os.getcwd(), 'src/filmelier/Crawling/crawling/movie_list.txt')
# default_url = 영화 검색 url
# 영화 리뷰 {} 라고 쓰여 있고, {} 부분에 title 을 하나씩 넣는다
default_url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%98%81%ED%99%94%20{}"
# file_path 에서 텍스트를 한 줄씩 읽어 movie_title 에 저장
with open(file_path, "r", encoding="utf-8") as file:
    movie_title = file.read().split('\n')


def download_image(img_url, file_path):
    try:
        response = requests.get(img_url, stream=True)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
            print(f"이미지 저장 완료 : {file_path}")
        else:
            print(f"이미지 다운 실패 : {img_url}")
    except Exception as e:
        print(f"이미지 다운 오류 발생 : {str(e)}")


# 영화 검색 코드
def process_movie(title):
    """
    file_path 에서 텍스트를 가져와 title 에 넣고,
    title 을 default_url 의 {} 에 넣어 검색 한다.
    검색된 블로그 링크를 탐색 한 뒤, title 이 링크의 텍스트에 포함된 링크만 가져 온다.
    그 다음 naver.com 이 들어간 url 만 가져온다.
    두번의 필터링 이후 가져온 링크로 들어가 내부의 p태그 요소만 가져 온다.
    이 때 네이버 블로그는 myframe 형식 으로 되어 있어서,
    ec.frame 을 사용 하여 mainFrame 으로 변환 하여 사용 하고 있다.
    이후 가져온 텍스트를 title 을 제목으로 하여 저장 한다.
    저장 할 때는 특수문자를 모두 _ 로 바꿔서 저장 하고 있다.

    :param title:영화 제목
    :return:영화 목록 파일을 읽고 영화의 블로그 리뷰를 가져오는 함수
    """
    title = title.strip()
    if title:
        base_url = default_url.format(title)
        driver.get(base_url)
        print("url :", base_url)

    print("페이지로드")
    time.sleep(5)

    # 블로그 링크를 가져오는 코드
    try:
        images = WebDriverWait(driver, 10).until(
            ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.detail_info > a > img')))
        for i, img in enumerate(images):
            img_url = img.get_attribute('src')
            # print(f"이미지 url : {img_url}")
            reset_title = (title
                           .replace('/', '_')
                           .replace('\\', '_')
                           .replace(':', '_')
                           .replace('*', '_')
                           .replace('?', '_')
                           .replace('"', '_')
                           .replace('<', '_')
                           .replace('>', '_')
                           .replace('|', '_'))
            file_name = f"src/filmelier/Crawling/crawling/image/{reset_title}.jpg"
            download_image(img_url, file_name)
    except Exception as e:
        print(f"검색 도중 오류발생{title}:{str(e)}")
        return


# 위의 movie_title 을 가져와 process_movie 의 title 에 전달
for titles in movie_title:
    print("test")
    process_movie(titles)

print("end")

driver.quit()
