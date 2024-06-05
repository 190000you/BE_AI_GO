from rest_framework.fields import SerializerMethodField, IntegerField
from rest_framework.serializers import ModelSerializer, CharField, DateTimeField, StringRelatedField
from rest_framework import serializers

from places.models import Place

from .models import Schedule, Plan, chatDb


class PlanNameSerializer(ModelSerializer):
    class Meta:
        model = Plan
        fields = ["name"]

class PlanSerializer(ModelSerializer):
    plan = Plan.objects.all()

    class Meta:
        model = Plan
        fields = "__all__"

class ScheduleModelSerializer(ModelSerializer):
    place = StringRelatedField()
    plan = StringRelatedField()
    latitude = SerializerMethodField()
    hardness = SerializerMethodField()

    class Meta:
        model = Schedule
        fields = "__all__"

    def get_latitude(self, obj):
        return obj.get_latitude()

    def get_hardness(self, obj):
        return obj.get_hardness()

class ScheduleCreateSerializer(ModelSerializer):
    start_date = DateTimeField()
    end_date = DateTimeField()
    place = Place.objects.all()
    plan = Plan.objects.all()

    class Meta:
        model = Schedule
        fields = "__all__"

class ScheduleDeleteSerializer(serializers.Serializer):
    plan_id = IntegerField()
    schedule_id = IntegerField()

class SchedulePatchSerializer(ModelSerializer):
    plan = Plan.objects.all()

class PlanModelSerializer(ModelSerializer):

    schedule = ScheduleModelSerializer(source="schedule_set", read_only=True, many=True)

    class Meta:
        model = Plan
        fields = "__all__"

class ChatSerializer(serializers.Serializer):
    user_input = serializers.CharField(max_length=1000)

class ChatDbSerializer(serializers.ModelSerializer):
    class Meta:
        model = chatDb
        fields = "__all__"