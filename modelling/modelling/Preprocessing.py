import pandas as pd

df_area = pd.read_csv(r"C:\Users\jyjun\OneDrive\바탕 화면\모델링\data\tn_visit_area_info_방문지정보_B.csv", encoding="cp949", low_memory=False)
df_info = pd.read_csv(r"C:\Users\jyjun\OneDrive\바탕 화면\모델링\data\tn_traveller_master_여행객 Master_B.csv", encoding="cp949")
df_trip = pd.read_csv(r"C:\Users\jyjun\OneDrive\바탕 화면\모델링\data\tn_travel_여행_B.csv", encoding="cp949")
df_rec2_file = pd.read_csv(r"C:\Users\jyjun\OneDrive\바탕 화면\모델링\data\대구광역시_관광지_160개.csv", encoding='cp949')

df = pd.merge(df_area, df_trip, on='TRAVEL_ID', how="left")
df = pd.merge(df, df_info, on='TRAVELER_ID', how='left')

df_filter = df[~df['TRAVEL_MISSION_CHECK'].isnull()].copy()

df_filter.loc[:, 'TRAVEL_MISSION_INT'] = df_filter['TRAVEL_MISSION_CHECK'].str.split(';').str[0].astype(int)

df_filter = df_filter[[
    'GENDER',
    'AGE_GRP',
    'TRAVEL_STYL_1', 'TRAVEL_STYL_2', 'TRAVEL_STYL_3', 'TRAVEL_STYL_4', 'TRAVEL_STYL_5', 'TRAVEL_STYL_6', 'TRAVEL_STYL_7', 'TRAVEL_STYL_8',
    'TRAVEL_COMPANIONS_NUM',
    'VISIT_AREA_NM',
    'DGSTFN',
]]

df_filter = df_filter.dropna()

categorical_features_names = [
    'GENDER',
    # 'AGE_GRP',
    'TRAVEL_STYL_1', 'TRAVEL_STYL_2', 'TRAVEL_STYL_3', 'TRAVEL_STYL_4', 'TRAVEL_STYL_5', 'TRAVEL_STYL_6', 'TRAVEL_STYL_7', 'TRAVEL_STYL_8',
    # 'TRAVEL_COMPANIONS_NUM',
    'VISIT_AREA_NM',
    # 'DGSTFN',
]

df_filter[categorical_features_names[1:-1]] = df_filter[categorical_features_names[1:-1]].astype(int)
