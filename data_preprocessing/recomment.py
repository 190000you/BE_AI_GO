import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def recommend(input_text, csv_file_path, top_n=5):
    # CSV 파일 읽기
    df = pd.read_csv(csv_file_path, encoding= 'cp949')
    
    # TF-IDF 벡터화
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['tag'])
    
    # 입력 텍스트를 TF-IDF로 변환
    input_tfidf = tfidf_vectorizer.transform([input_text])
    
    # 코사인 유사도 계산
    similarities = cosine_similarity(input_tfidf, tfidf_matrix)
    
    # 유사도 순으로 상위 n개의 행 추출
    similar_row_indices = similarities.argsort(axis=1)[0][-top_n:][::-1]
    recommended_rows = df.loc[similar_row_indices]
    
    return recommended_rows

# 예시 사용법
input_text = "#한적한 #나들이 #자연"
csv_file_path = r"C:\Langchain\poat\langchain\대구광역시_관광지_완.csv"

recommendations = recommend(input_text, csv_file_path)
print("5개의 장소를 추천했어요: ")
print(recommendations)
