from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from Preprocessing import df_rec2_file

df_rec2_file = df_rec2_file

#불용어 처리
korean_stop_words = [
    "이", "그", "저", "에", "가", "을", "를", "의", "은", "는", "들", "를", "과", "와", "에게", "게",
    "합니다", "하는", "있습니다", "합니다", "많은", "많이", "많은", "많이", "모든", "모두", "한", "그리고", "그런데",
    "나", "너", "우리", "저희", "이런", "그런", "저런", "어떤", "어느", "그럴", "것", "그것", "이것", "저것", 
    "그러나", "그리하여", "그러므로", "그래서", "하지만", "그럼에도", "이에", "때문에", "그래서", "그러니까", 
    "이렇게", "그렇게", "저렇게", "어떻게", "왜", "무엇", "어디", "언제", "어떻게", "어느", "모두", "모든", 
    "그래도", "하지만", "그러면", "그런데", "하지만", "이러한", "그러한", "저러한", "이러한", "이렇게", "그렇게",
    "저렇게", "어떻게", "왜", "어디", "언제", "어떻게", "모두", "모든", "몇", "누구", "무슨", "어느", "얼마나",
    "무엇", "무슨", "아무", "여기", "저기", "거기", "그곳", "이곳", "저곳", "무엇", "아무", "모두", "마치",
    "보다", "보이다", "등", "등등", "등등등"
    ]

def rec2_get_user_input():
    user_input = input("어떤 추천을 원하나요? : ")
    input_data = [user_input]
    return input_data

def rec2_recommend_places(df_rec2_file, input_data, korean_stop_words):
    all_about_data = df_rec2_file['all about'].tolist()

    tfidf = TfidfVectorizer(stop_words=korean_stop_words)
    tfidf_matrix_input = tfidf.fit_transform(input_data)
    tfidf_matrix_all_about = tfidf.transform(all_about_data)

    # 코사인 유사도 계산
    cosine_sim = linear_kernel(tfidf_matrix_input, tfidf_matrix_all_about)

    # 상위 5개의 유사한 관광지 이름 출력
    top_place = cosine_sim.argsort()[0][-2:][::-1]

    for i, idx in enumerate(top_place, 5):
        print(f"{i}. {df_rec2_file['name'][idx]}")
    print("이렇게 추천해 드립니다! 감사합니다!!")