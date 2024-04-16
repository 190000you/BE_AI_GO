from rest_framework.serializers import ModelSerializer, CharField, DateTimeField, StringRelatedField
from rest_framework.response import Response
from rest_framework import status

from .models import Answer
from account.models import User

from django.utils.crypto import get_random_string

class EnrollmentSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"
        
    def create(self, validated_data):
        # 요청에서 userId 추출
        user_id = self.context['request'].data.get('userId')
        
        # userId가 없는 경우 새로운 사용자 생성
        if not user_id:
            user = User.objects.create_user(username=get_random_string(), password=None)
        else:
            # userId가 있는 경우 해당 사용자 검색
            try:
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                # userId에 해당하는 사용자가 없는 경우 새로운 사용자 생성
                user = User.objects.create_user(username=get_random_string(), password=None)
        
        # userId 필드에 사용자 객체 할당
        validated_data['userId'] = user
        
        # Answer 인스턴스 생성
        answer_instance = Answer.objects.create(**validated_data)
        
        # 생성된 Answer 인스턴스와 사용자 객체 연결
        user.survey = answer_instance
        user.save()
        
        return answer_instance