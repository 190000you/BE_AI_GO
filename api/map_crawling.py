import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

import selenium #셀레니움
import pandas as pd #csv를 읽고 dataframe을 사용하기 위한 pandas
from selenium import webdriver #브라우저를 띄우고 컨트롤하기 위한 webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys #브라우저에 키입력 용
from selenium.webdriver.common.by import By #webdriver를 이용해 태그를 찾기 위함
from selenium.webdriver.support.ui import WebDriverWait #Explicitly wait을 위함
from webdriver_manager.chrome import ChromeDriverManager #크롬에서 크롤링 진행 크롬 웹 드라이버 설치시 필요
from selenium.webdriver.support import expected_conditions as EC #브라우저에 특정 요소 상태 확인을 위해
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,TimeoutException #예외처리를 위한 예외들 
import time
from difflib import SequenceMatcher
import re
from config import settings

df = pd.read_csv(r"C:\work_django\BE_AI_GO\api\dataset.csv", encoding='CP949')

chrom_options = Options()
chrom_options.add_experimental_option("detach", True)

chrom_options.add_experimental_option("excludeSwitches", ["enable-logging"])

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrom_options)
driver.get("https://map.naver.com/v5/")

driver.implicitly_wait(10)  # 로딩이 끝날 때까지 10초까지는 기다려줌
search = driver.find_element(By.CSS_SELECTOR,".input_search")
search.click()

for index, row in df.iterrows():
    search.click()
    search.clear()
    search.send_keys(row["street_name_address"])
    search.send_keys(Keys.ENTER)
    time.sleep(1)
    try:
        more_btn = driver.find_element(By.CLASS_NAME,"link_more")
        more_btn.click()
        time.sleep(1)

        # 유사도 측정
        best_ratio = 0 # temp ratio
        best_element = None
    
        names = driver.find_elements(By.CSS_SELECTOR, "#sub_panel > div > div > div > div > div > div > button > div > div > strong")
        for name in names:
            name_text = name.text
            ratio = SequenceMatcher(None, row["name"], name_text).ratio()
            if best_ratio < ratio:
                best_ratio = ratio
                best_element = name
            
        if best_ratio:
            best_element.click()
            time.sleep(1)
    except NoSuchElementException:
        pass
    # iframe으로 전환
    iframe = driver.find_element(By.CSS_SELECTOR, "iframe#entryIframe")
    driver.switch_to.frame(iframe)

    # 이미지 요소 찾기
    image_element = driver.find_element(By.CLASS_NAME, "K0PDV")

    # 이미지 스타일 속성 가져오기
    style_attribute = image_element.get_attribute("style")

    # 스타일 속성에서 이미지 URL 추출
    url_match = re.search(r"url\((.*?)\)", style_attribute)
    if url_match:
        image_url = url_match.group(1)
        url_without_quotes = re.sub(r'"', '', image_url)
        print(url_without_quotes)

        df.loc[index, "image"] = url_without_quotes

        # 데이터프레임의 특정 행 출력
        print(df.loc[df['name'] == row['name']])
        
        # iframe에서 기본 콘텐츠로 전환
        driver.switch_to.default_content()

    else:
        print("No matching element found.")
    
df.to_csv("C:\\Users\\als00\\Desktop\\캡스톤_files\\image_data.csv")

