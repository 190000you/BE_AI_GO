import pandas as pd
from catboost import CatBoostRegressor
from Preprocessing import df_filter

# 저장된 모델 불러오기
def load_model(model_path):
    model = CatBoostRegressor()
    model.load_model(model_path)
    return model

def rec1_get_user_input():
    traveler = {
        'GENDER': input("성별 (남/여): "),
        'AGE_GRP': float(input("나이대를 입력하세요 예) 20대, 30대 : ")),
        'TRAVEL_STYL_1': int(input("자연 VS 도시 (1-10): ")),
        'TRAVEL_STYL_2': int(input("숙박 VS 당일치기 (1-10): ")),
        'TRAVEL_STYL_3': int(input("새로운 지역 VS 익숙한 지역 (1-10): ")),
        'TRAVEL_STYL_4': int(input("편하지만 비싼 숙소 vs 불편하지만 저렴한 숙소 (1-10): ")),
        'TRAVEL_STYL_5': int(input("휴양/휴식 VS 체험활동 (1-10): ")),  
        'TRAVEL_STYL_6': int(input("잘 알려지지 않은 방문지 VS 알려진 방문지 (1-10): ")), 
        'TRAVEL_STYL_7': int(input("계획 VS 즉흥 (1-10): ")),  
        'TRAVEL_STYL_8': int(input("사진활영 중요하지 않음 VS 중요 (1-10): ")), 
        # 'TRAVEL_MOTIVE_1': int(input("Travel Motive (1-10): ")),
        'TRAVEL_COMPANIONS_NUM': float(input("동반자 수 예) 나홀로 여행객은 0: "))
        # 'TRAVEL_MISSION_INT': int(input("Travel Mission (as a number): ")),
    }
    return traveler

def rec1_predict_areas(model, traveler, area_names):
    results = pd.DataFrame([], columns=['AREA'])

    for area in area_names['VISIT_AREA_NM'].to_list():
    # DataFrame의 형태로 입력 데이터를 구성
        input_data = pd.DataFrame([traveler.values()], columns=traveler.keys())
        input_data['VISIT_AREA_NM'] = area
    
    # 모델 예측
        score = model.predict(input_data)[0]  # 첫 번째 값으로 예측 결과를 스칼라 값으로 사용
    
    # 결과 DataFrame에 추가
        results = pd.concat([results, pd.DataFrame([{'AREA': area, 'SCORE' : score }])], ignore_index=True)
    
    top_results = results.sort_values('SCORE', ascending=False).head(2).reset_index(drop=True)

    for idx, area in enumerate(top_results['AREA'], start=3):
        print(f"{idx}. {area}")

model_path = "catboost_model.dump"
model = load_model(model_path)
area_names = df_filter[['VISIT_AREA_NM']].drop_duplicates()