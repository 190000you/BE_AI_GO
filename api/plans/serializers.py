from rest_framework.serializers import ModelSerializer, CharField, DateTimeField, StringRelatedField

from places.serializers import SchedulePlaceSerializer
from places.models import Place

from .models import Schedule, Plan


class PlanNameSerializer(ModelSerializer):
    class Meta:
        model = Plan
        fields = ["name"]

class ScheduleModelSerializer(ModelSerializer):
    place = StringRelatedField()
    plan = StringRelatedField()

    class Meta:
        model = Schedule
        fields = "__all__"

class ScheduleCreateSerializer(ModelSerializer):
    start_date = DateTimeField()
    end_date = DateTimeField()
    place = Place.objects.all()
    plan = Plan.objects.all()

    class Meta:
        model = Schedule
        fields = "__all__"

class PlanModelSerializer(ModelSerializer):

    schedule = ScheduleModelSerializer(source="schedule_set", read_only=True, many=True)

    class Meta:
        model = Plan
        fields = "__all__"