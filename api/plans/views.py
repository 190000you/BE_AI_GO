from django.shortcuts import render

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import GenericAPIView
from rest_framework import routers

from .serializers import ScheduleModelSerializer, PlanModelSerializer, ScheduleCreateSerializer
from .models import Schedule, Plan
# Create your views here.

class ScheduleApiView(GenericAPIView):
    serializer_class = ScheduleCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        start_date = request.data.get('start_date')
        end_date = request.data.get('end_date')
        place = request.data.get('place')
        plan = request.data.get('plan')

        if start_date > end_date:
            return Response({'error' : '올바른 시간을 입력하세요.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():
                data = {
                    "start_date" : start_date,
                    "end_date" : end_date,
                    "place" : place,
                    "plan" : plan
                }
                serializer.save()
                return Response(data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=400)
            
class PlanViewSet(ModelViewSet):
    serializer_class = PlanModelSerializer
    queryset = Plan.objects.all()
    