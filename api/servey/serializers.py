from rest_framework.serializers import ModelSerializer, CharField, DateTimeField, StringRelatedField

from .models import Answer

class EnrollmentSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"
        