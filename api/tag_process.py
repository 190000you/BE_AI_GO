import pandas as pd

import django

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

django.setup()

from places.models import Tag

df = pd.read_excel(r"/Users/leehb/Desktop/BE_AI_GO/api/tag.xlsx", engine="openpyxl")

for index, row in df.iterrows():
    tag = Tag.objects.create(
        name = "#"+row["name"].replace("'","")
    )
    tag.save()
