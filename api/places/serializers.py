from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField

from .models import Place, Tag, Review


class TagModelSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

    def create(self, data):
        tag_name = data.get("name")

        if "#" not in tag_name:
            tag_name = "#" + tag_name
        data["name"] = tag_name

        return super().create(data)


class ReviewModelSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class PlaceModelSerializer(ModelSerializer):
    ## 장고에서 자동으로  related_name 을 review_set으로 설정해줌
    reviews = ReviewModelSerializer(source="review_set", read_only=True, many=True)

    class Meta:
        model = Place
        fields = "__all__"
    
# class PlaceSearchSerializer(ModelSerializer):
#     name = CharField(write_only=True, max_length=150)

#     class Meta:
#         model = Place
#         fields = ["name"]

#     def validate(self, data):
#         name = data.get("name")

#         place = Place.objects.filter(name=name)
#         if not place.exists():
#             serializers.ValidationError("Invalid Place")
#         data['place'] = PlaceModelSerializer(place, many=True).data
#         return data

class PlaceSearchSerializer(ModelSerializer):
    name = CharField(write_only=True, max_length=150)

    class Meta:
        model = Place
        fields = ["name"]

class SchedulePlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = ["name"]


