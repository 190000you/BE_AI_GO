import pandas as pd
import nltk
from nltk.tokenize import word_tokenize

# NLTK의 토크나이저를 다운로드합니다.
nltk.download('punkt')

def extract_words_from_tags(csv_file_path):
    # CSV 파일 읽기
    df = pd.read_csv(csv_file_path, encoding = 'cp949')
    
    # 모든 단어를 저장할 빈 리스트
    all_words = []
    
    # 각 행의 "tag" 열을 토큰화하여 단어를 추출합니다.
    for tag in df['tag']:
        words = word_tokenize(tag)
        all_words.extend(words)
    
    # 중복된 단어 제거
    unique_words = list(set(all_words))
    
    return unique_words

# 예시 사용법
csv_file_path = r"C:\Langchain\poat\langchain\대구광역시_관광지_완.csv"
tags = extract_words_from_tags(csv_file_path)
print("Extracted words from tags:")
print(tags)