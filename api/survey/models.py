from django.db import models

# Create your models here.
    # 추가 할 수도 있음
    # class Question(models.Model):
    #     #    content = models.TextField(verbose_name="리뷰내용")

    #     gender = models.TextField(verbose_name="성별")
    #     ageGrp = models.TextField(verbose_name="나이대")
    #     travelStyl1 = models.TextField(verbose_name="장소")
    #     travelStyl2 = models.TextField(verbose_name="기간")
    #     travelStyl3 = models.TextField(verbose_name="숙소")
    #     travelStyl4 = models.TextField(verbose_name="활동")
    #     travelStyl5 = models.TextField(verbose_name="방문지")
    #     travelStyl6 = models.TextField(verbose_name="계획")
    #     travelStyl7 = models.TextField(verbose_name="사진")
    #     travelStyl8 = models.TextField(verbose_name="동반자")
        
    #     class Meta:
    #         verbose_name = "설문조사 질문"
    #         verbose_name_plural = "설문조사 질문 모음"
    #     'GENDER': input("성별 (남/여): "),
    #     'AGE_GRP': float(input("나이대를 입력하세요 예) 20대, 30대 : ")),
    #     'TRAVEL_STYL_1': int(input("자연 VS 도시 (1-10): ")),
    #     'TRAVEL_STYL_2': int(input("숙박 VS 당일치기 (1-10): ")),
    #     'TRAVEL_STYL_3': int(input("새로운 지역 VS 익숙한 지역 (1-10): ")),
    #     'TRAVEL_STYL_4': int(input("편하지만 비싼 숙소 vs 불편하지만 저렴한 숙소 (1-10): ")),
    #     'TRAVEL_STYL_5': int(input("휴양/휴식 VS 체험활동 (1-10): ")),  
    #     'TRAVEL_STYL_6': int(input("잘 알려지지 않은 방문지 VS 알려진 방문지 (1-10): ")), 
    #     'TRAVEL_STYL_7': int(input("계획 VS 즉흥 (1-10): ")),  
    #     'TRAVEL_STYL_8': int(input("사진활영 중요하지 않음 VS 중요 (1-10): ")), 
    #     # 'TRAVEL_MOTIVE_1': int(input("Travel Motive (1-10): ")),
    #     'TRAVEL_COMPANIONS_NUM': float(input("동반자 수 예) 나홀로 여행객은 0: "))
    #     # 'TRAVEL_MISSION_INT': int(input("Travel Mission (as a number): ")),

class Answer(models.Model):
    userId = models.OneToOneField('account.User', on_delete=models.CASCADE) 
    gender = models.TextField(verbose_name="성별", null=True, default='')
    ageGrp = models.IntegerField(verbose_name="나이대", null=True, default=0)
    travelStyl1 = models.IntegerField(verbose_name="장소", null=True, default=0)
    travelStyl2 = models.IntegerField(verbose_name="기간", null=True, default=0)
    travelStyl3 = models.IntegerField(verbose_name="숙소", null=True, default=0)
    travelStyl4 = models.IntegerField(verbose_name="활동", null=True, default=0)
    travelStyl5 = models.IntegerField(verbose_name="방문지", null=True, default=0)
    travelStyl6 = models.IntegerField(verbose_name="계획", null=True, default=0)
    travelStyl7 = models.IntegerField(verbose_name="사진", null=True, default=0)
    travelStyl8 = models.IntegerField(verbose_name="동반자", null=True, default=0)
