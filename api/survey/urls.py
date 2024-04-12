from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from .views import AnswerView

namespace = "survey"

router_answer = routers.DefaultRouter()

router_answer.register(r"enroll", AnswerView)

urlpatterns = [
    path(r'', include(router_answer.urls)),
]