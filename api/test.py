import pandas as pd

# 프로젝트에 startapps 명령어로 생성되지 않은 파일에서 장고에 등록된 모델이나 함수를 사용할 때 다음과 같은 에러가 발생한다.

# django.core.exceptions.ImproperlyConfigured: Requested setting INSTALLED_APPS, but settings are not configured.
# You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.

# 이를 해결하기 위해선 환경을 장고에 맞춰주기 위해서 다음과 같은 코드를 from user.models import model 과 같은 파일 위쪽에 선언해준다.

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from places.models import Place, Tag

import time

from config import settings

# Read csv file.
df = pd.read_csv(r"C:\Users\horai\Desktop\BE_AI_GO\api\dataset.csv", encoding='utf-8')

for index, row in df.iterrows():
    tag_list = list(row["tag"].split())
    print(index, tag_list)