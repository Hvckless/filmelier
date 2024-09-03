from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import os

# configuration start

movieListFilepath = "undefined"
reviewFolderpath = "undefined"

def setMovieListFilepath(filepath:str):
    movieListFilepath = filepath

def setReviewFolderpath(folderpath:str):
    reviewFolderpath = folderpath

# 🎈 해당 컴퓨터 경로에 맞춰서 설정

# 영화 목록 텍스트 파일 경로
setMovieListFilepath('src/filmelier/Crawling/crawling/blog_review/엄복동.txt')
# 영화 리뷰 저장 위치 설정
setReviewFolderpath('src/filmelier/Crawling/crawling/blog_review/')

# configuration end



option = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=option)
# file_path = 영화 목록 파일
# 영화 목록 파일이 있는 경로만 복사 해서 변경 해주면 된다.
file_path = os.path.join(os.getcwd(),movieListFilepath)

# default_url = 영화 검색 url
# 영화 리뷰 {} 라고 쓰여 있고, {} 부분에 title 을 하나씩 넣는다
default_url = "https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=%EC%98%81%ED%99%94%20%EB%A6%AC%EB%B7%B0%20{}"
# file_path 에서 텍스트를 한 줄씩 읽어 movie_title 에 저장
with open(file_path, "r", encoding="utf-8") as file:
    movie_title = file.read().split('\n')


# 영화 검색 코드
def process_movie(title):
    title = title.strip()
    all_text = []
    if title:
        base_url = default_url.format(title)
        driver.get(base_url)
        print("url :", base_url)

    print("페이지로드")
    time.sleep(5)

    blog_links = []
    # 블로그 링크를 가져오는 코드
    try:
        links = WebDriverWait(driver,10).until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.title_area > a')))
        for link in links:
            # 블로그 링크의 텍스트 안에 title 이 있는 링크만 가져옴
            link_text = link.get_attribute('innerText')
            if title in link_text:
                url = link.get_attribute('href')
                # naver.com 이 들어간 url 만 가져옴
                if 'blog.naver.com' in url:
                    blog_links.append(url)
                    print("blog:", len(blog_links))
            # 링크를 20개 가져오면 멈춤
            if len(blog_links) >= 20:
                print("blog_url :", blog_links)
                break
        if len(blog_links) == 0:
            print(f"검색결과가 없습니다:{title}")
            return
    except Exception as e:
        print(f"검색 도중 오류발생{title}:{str(e)}")
        return

    # 가져온 블로그 링크에 접속하여 내부의 텍스트를 가져오는 코드
    for i, blog_url in enumerate(blog_links):
        driver.get(blog_url)

        time.sleep(5)

        # p태그만 가져오되, 세번째 문단에서부터 가져옴
        try:
            WebDriverWait(driver,10).until(ec.frame_to_be_available_and_switch_to_it("mainFrame"))

            p_tags = driver.find_elements(By.CSS_SELECTOR, "p")
            texts = [p.text for p in p_tags if p.text.strip()]
            all_text.extend(texts[2:])

        except Exception as e:
            print(f"파일 오류{blog_url}: {str(e)}")

    # 위의 file_path 에서 가져온 텍스트의 특수문자 처리
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
    # 위의 reset_title 을 파일명으로 자동 생성
    # 파일 저장하고싶은 경로 {reset_title}_review.txt 의 앞부분에 작성
    file_name = f"{reviewFolderpath}{reset_title}_review.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write('\n'.join(all_text))
        print("text :", all_text)


# 위의 movie_title 을 가져와 process_movie 의 title 에 전달
for titles in movie_title:
    print("test")
    process_movie(titles)
print("end")