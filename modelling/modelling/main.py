from Preprocessing import df_filter, df_rec2_file
from Recommend_1 import rec1_predict_areas, rec1_get_user_input
from Recommend_2 import rec2_recommend_places, korean_stop_words
from Langchain import chain
from catboost import CatBoostRegressor

def load_model(model_path):
    model = CatBoostRegressor()
    model.load_model(model_path)
    return model

def fun1(model, area_names, traveler):
    results = rec1_predict_areas(model, traveler, area_names)
    print(results)

def fun2(user_input):
    input_data = [user_input]
    results = rec2_recommend_places(df_rec2_file, input_data, korean_stop_words)
    print(results)

def main():
    # 모델과 지역 이름 로드
    model_path = "catboost_model.dump"
    model = load_model(model_path)
    area_names = df_filter[['VISIT_AREA_NM']].drop_duplicates()

    #사용자 입력 받기
    traveler = rec1_get_user_input()
    user_input = input("사용자: ")

    print("안녕하세요! 가볼까? 에서 몇가지 추천을 드릴게요")

    # Langchain 연동 결과 출력
    lanchain_result = chain.invoke({"input": user_input})
    print(lanchain_result)

    # 함수 1 실행
    fun1(model, area_names, traveler)
    
    # 함수 2 실행
    fun2(user_input)

if __name__ == "__main__":
    main()
