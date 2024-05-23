import os
import pandas as pd
import django

# Django 설정을 로드
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from places.models import Place, Tag

# CSV
# df = pd.read_csv(r"/Users/leehb/Desktop/BE_AI_GO/api/dataset.csv", encoding='cp949')
df = pd.read_csv(r"/srv/BE_AI_GO/api/dataset.csv", encoding='cp949')

for index, row in df.iterrows():
    # 공백 기준으로 list로 불러오기
    tag_list = list(str(row["tag"]).split())
    
    # 주차 여부 bool로 넣기
    parking_bool = (row["parking"] == "유")
    
    if row["hardness"] == '-':
        save_hardness = 0.0
    else:
        save_hardness = row["hardness"]

    if row["latitude"] == '-':
        save_latitude = 0.0
    else:
        save_latitude = row["latitude"]

    # db에 넣기
    place = Place.objects.create(
        name=row["name"],
        image=None,
        classification=row["classification"],
        street_name_address=row["street_name_adress"],
        parking=parking_bool,
        info=row["info"],
        call=row["call"],
        hardness=save_hardness,
        latitude=save_latitude,
        time=row["time"]
    )
    
    # 태그 추가
    for tag_name in tag_list:
        tag, _ = Tag.objects.get_or_create(name=tag_name)
        place.tag.add(tag)

    place.save()  # 장소를 저장합니다.
