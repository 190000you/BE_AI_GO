import os
import pandas as pd
import django
from django.core.files import File

# Django 설정을 로드
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from places.models import Place, Tag

# CSV 파일 로드
df = pd.read_csv(r"dataset.csv", encoding='cp949')

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

    if "image_name" in row:
        image_name = row["image_name"]
    else:
        image_name = f'{row["name"]}.jpg'

    # 이미지 파일 경로
    IMAGE_DIR = 'media/이미지'

    image_path = os.path.join(IMAGE_DIR, image_name)

    # 이미지 파일 존재 여부 확인 및 File 객체 생성
    if os.path.exists(image_path):
        image_file = File(open(image_path, 'rb'), name=image_name)
    else:
        image_file = None

    # db에 넣기
    place = Place.objects.create(
        name=row["name"],
        image=image_file,
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

    # 이미지 파일이 열려 있으면 닫기
    if image_file:
        image_file.close()

    place.save()  # 장소를 저장
