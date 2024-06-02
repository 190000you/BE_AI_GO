
from django.db import models
from places.models import Place

from django.contrib.auth import get_user_model

User = get_user_model()

class Schedule(models.Model):
    start_date = models.DateTimeField(verbose_name='일정시작시각')
    end_date = models.DateTimeField(verbose_name='일정종료시각')
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    plan = models.ForeignKey(to='Plan', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.place.name

    def get_hardness(self):
        return self.place.hardness

    def get_latitude(self):
        return self.place.latitude
    
class Plan(models.Model):
    name = models.CharField(verbose_name='플랜명', max_length= 50)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class chatDb(models.Model):
    user_input = models.TextField(verbose_name="유저 질문")
    chat_response = models.TextField(verbose_name="AI 답변")
    user_input_date = models.DateTimeField(auto_now_add=True)
    chat_response_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)