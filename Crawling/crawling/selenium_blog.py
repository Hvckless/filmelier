from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
import os

option = webdriver.ChromeOptions()
service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=option)
file_path = os.path.join(os.getcwd(),'src/filmelier/Crawling/crawling/movie_filterList.txt')

default_url = "https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=%EC%98%81%ED%99%94%20%EB%A6%AC%EB%B7%B0%20{}"
with open(file_path, "r", encoding="utf-16") as file:
    movie_title = file.read().split('\n')

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
    try:
        links = WebDriverWait(driver,10).until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.title_area > a')))
        for link in links:
            url = link.get_attribute('href')
            if 'blog.naver.com' in url:
                blog_links.append(url)
                print("blog:",len(blog_links))
            if len(blog_links) < 1:
                break
            if len(blog_links) >= 2:
                print("blog_url :", blog_links)
                break
        if len(blog_links) == 0:
            print(f"검색결과가 없습니다:{title}")
            return
    except Exception as e:
        print(f"검색 도중 오류발생{title}:{str(e)}")
        return

    for i, blog_url in enumerate(blog_links):
        driver.get(blog_url)

        time.sleep(5)

        try:
            WebDriverWait(driver,10).until(ec.frame_to_be_available_and_switch_to_it("mainFrame"))

            p_tags = driver.find_elements(By.CSS_SELECTOR, "p")
            texts = [p.text for p in p_tags if p.text.strip()]
            all_text.extend(texts[2:])

        except Exception as e:
            print(f"파일 오류{blog_url}: {str(e)}")

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
    file_name = f"src/filmelier/Crawling/crawling/blog_review/{reset_title}_review.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write('\n'.join(all_text))
        print("text :", all_text)


for titles in movie_title:
    print("test")
    process_movie(titles)
print("end")

#https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=%EC%98%81%ED%99%94% EA%B7%B9%ED%95%9C%EC%A7%81%EC%97%85%
#https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=%EC%98%81%ED%99%94% EB%A7%88%EC%85%98%
#https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%98%81%ED%99%94%EC%8A%A4%EB%AC%BC%
#https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%98%81%ED%99%94%EB%A6%AC%EB%B7%B0
#EB%A6%AC%EB%B7%B0
#EB%A6%AC%EB%B7%B0
#EB%A6%AC%EB%B7%B0
#%EC%98%81%ED%99%94%EB%A6%AC%EB%B7%B0
#%EC%98%81%ED%99%94%20%EB%A6%AC%EB%B7%B0