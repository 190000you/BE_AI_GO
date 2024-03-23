import os
import pandas as pd
import django

# Django 설정을 로드합니다.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from places.models import Place, Tag

# CSV 파일을 읽어옵니다.
df = pd.read_csv(r"C:\Users\horai\Desktop\BE_AI_GO\api\dataset_test.csv", encoding='utf-8')

# CSV 파일의 각 행에 대해 반복합니다.
for index, row in df.iterrows():
    # 태그 문자열을 공백을 기준으로 분리하여 리스트로 변환합니다.
    tag_list = list(str(row["tag"]).split())
    
    # 주차 여부에 따라 불리언 값을 설정합니다.
    parking_bool = (row["parking"] == "유")
    
    # 장소 인스턴스를 생성합니다.
    place = Place.objects.create(
        name=row["name"],
        image=None,
        classification=row["classification"],
        street_name_address=row["street_name_adress"],
        parking=parking_bool,
        info=row["info"],
        call=row["call"],
        hardness=row["hardness"],
        latitude=row["latitude"],
        time=row["time"]
    )
    
    # 장소와 태그를 연결합니다.
    for tag_name in tag_list:
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        place.tag.add(tag)

    place.save()  # 장소를 저장합니다.
