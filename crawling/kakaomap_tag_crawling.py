import json
import csv
import time
from time import sleep

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from itertools import zip_longest

url = 'https://map.kakao.com/'
driver = webdriver.Chrome()
driver.get(url)

# CSV 파일 불러오기
input_csv_file = r"C:\Langchain\poat\langchain\대구광역시_관광지1111.csv"
data = pd.read_csv(input_csv_file, encoding='cp949')

# dictionary 생성
adress_name_dict = {'이름정보': []}
adress_dict = {'태그정보': []}

# css 찾을때 까지 10초대기
def time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, '태그를 찾지 못하였습니다.')
        driver.quit()
    return wait

# 장소 이름
def adress_name_print():

    time.sleep(0.2)

    place_list = driver.find_element(By.CSS_SELECTOR, '.head_item > .tit_name > .link_name')
    place = place_list.text.strip()

    # dict에 데이터 집어넣기
    dict_temp = {'place': place}
    adress_name_dict['이름정보'].append(dict_temp)

    print(f'{place} ...완료')


# 태그
def adress_tag_print():

    time.sleep(0.2)

    place_tags = driver.find_elements(By.CSS_SELECTOR, '.placeinfo_default > .location_detail > .txt_tag')

    if not place_tags:

        dict_temp = {'tag': '태그 없음'}
        adress_dict['태그정보'].append(dict_temp)

        print("태그 없음 ...완료")
        return

    for tag_element in place_tags:
        try:
            tag = tag_element.text.strip()
        except:
            tag = "Null"

        # dict에 데이터 집어넣기
        dict_temp = {'tag': tag}
        adress_dict['태그정보'].append(dict_temp)

        print(f'{tag} ...완료')

# csv 파일로 저장
def save_to_csv(name_data, tag_data, filename):
    with open(filename, 'w', newline='', encoding='cp949') as csvfile:
        fieldnames = ['place', 'tag']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for name_item, tag_item in zip(name_data, tag_data):
            writer.writerow({'place': name_item['place'], 'tag': tag_item['tag']})

# css를 찾을때 까지 10초 대기
time_wait(10, 'div.box_searchbar > input.query')

base = driver.find_element(By.CSS_SELECTOR, r"div.inner_coach_layer")
base.click()

# CSV 파일의 name 칼럼의 요소를 가져와 검색
for index, row in data.iterrows():
    name = row.iloc[0]
    # 검색창 찾기
    search = driver.find_element(By.CSS_SELECTOR, 'div.box_searchbar > input.query')
    search.clear()  # 검색창 초기화
    search.send_keys(name)  # 검색어 입력
    search.send_keys(Keys.ENTER)  # 엔터버튼 누르기

    sleep(1)

    # 장소 탭 클릭
    place_tab = driver.find_element(By.CSS_SELECTOR, '#info\.main\.options > li.option1 > a')
    place_tab.send_keys(Keys.ENTER)

    sleep(1)

    # 리스트 출력
    adress_name_print()

    sleep(1)

    # 상세정보
    more_tab = driver.find_element(By.CSS_SELECTOR, '.info_item > .contact.clickArea > .moreview')
    more_tab.send_keys(Keys.ENTER)

    sleep(1)

    # 새로운 탭으로 이동
    driver.switch_to.window(driver.window_handles[1])

    sleep(1)

    # 리스트 출력
    adress_tag_print()

    sleep(1)

    # 탭 닫기
    driver.close()

    sleep(1)

    # 탭 이동
    driver.switch_to.window(driver.window_handles[0])

    sleep(1)

# CSV 파일로 저장
output_csv_file = r'C:\Langchain\poat\langchain\관광지 태그3333.csv'
save_to_csv(adress_name_dict['이름정보'], adress_dict['태그정보'], output_csv_file)

# 드라이버 종료
driver.quit()