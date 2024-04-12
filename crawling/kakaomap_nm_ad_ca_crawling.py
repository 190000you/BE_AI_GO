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



url = 'https://map.kakao.com/'
driver = webdriver.Chrome() 
driver.get(url)

# CSV 파일 불러오기
input_csv_file = "C:\Langchain\poat\langchain\대구광역시_관광지.csv"
data = pd.read_csv(input_csv_file, encoding='cp949')

# dictionary 생성
adress_dict = {'주소정보': []}

# css 찾을때 까지 10초대기
def time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, '태그를 찾지 못하였습니다.')
        driver.quit()
    return wait

# 주소 정보 출력
def adress_list_print():

    time.sleep(0.2)

    # 장소 목록
    adress_list = driver.find_elements(By.CSS_SELECTOR, '.placelist > .PlaceItem')

    for index in range(len(adress_list)):
        print(index)

        #이름
        place_list = driver.find_element(By.CSS_SELECTOR, '.head_item > .tit_name > .link_name')
            
        # 주소
        try:
            address_list = driver.find_elements(By.CSS_SELECTOR, '.info_item > .addr')
            address = address_list.__getitem__(index).find_elements(By.CSS_SELECTOR, 'p')
        except:
            address = "주소 없음"

        # 전화번호
        try:
            phone_number = driver.find_elements(By.CSS_SELECTOR, '.info_item > .contact.clickArea > .phone')
        except:
            phone_number = "Null"
        
        # 태그
        try:
            place_tag = driver.find_elements(By.CSS_SELECTOR, '.info_item > .contact.clickArea > .phone')
        except:
            place_tag = "Null"

        palce_name = place_list[index].text
        print(palce_name)

        addr1 = address.__getitem__(0).text
        print(addr1)

        addr2 = address.__getitem__(1).text[5:]
        print(addr2)

        phone_number = phone_number[index].text
        print(phone_number)
            
        tag = place_tag[index].text
        print(tag)

        # dict에 데이터 집어넣기
        dict_temp = {
            'place' : palce_name,
            'address1': addr1,
            'address2': addr2,
            'phone_number': phone_number,
            'tag' : tag
        }

        adress_dict['주소정보'].append(dict_temp)
        print(f'{palce_name} ...완료')

# csv 파일로 저장
def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='cp949') as csvfile:
        fieldnames = ['place', 'address1', 'address2', 'phone_number']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for item in data:
            writer.writerow(item)

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

    # 상세정보
    more_tab = driver.find_element(By.CSS_SELECTOR, '.info_item > .contact.clickArea > .moreview')
    more_tab.send_keys(Keys.ENTER)

    # 리스트 출력
    adress_list_print()

    # 탭 닫기
    driver.close()

    # 탭 이동
    driver.switch_to.window(driver.window_handles[0])

# json 파일로 저장
#with open('data/parking_data.json', 'w', encoding='utf-8') as f:
    #json.dump(parking_dict, f, indent=4, ensure_ascii=False)

# CSV 파일로 저장
output_csv_file = 'C:\Langchain\poat\langchain\관광지 주소 태그 전번.csv'
save_to_csv(adress_dict['주소정보'], output_csv_file)

# 드라이버 종료
driver.quit()