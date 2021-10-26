from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView
from . models import Doubt,DoubtAnswers
from . serializers import DoubtAnswersSerializer,DoubtSerializer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from orders.models import Subscription
from rest_framework.views import APIView
from courses.models import Course
from chapters.models import Chapter
from . permissions import UpdateDeleteOwnDoubtOnly,UpdateDeleteOwnDoubtAnsOnly
from rest_framework.viewsets import ModelViewSet


class DoubtModelVS(ModelViewSet):
    queryset = Doubt.objects.all()
    serializer_class = DoubtSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,UpdateDeleteOwnDoubtOnly]
    filterset_fields = '__all__'


class DoubtAnswersModelVS(ModelViewSet):
    queryset = DoubtAnswers.objects.all()
    serializer_class = DoubtAnswersSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,UpdateDeleteOwnDoubtAnsOnly]
    filterset_fields = '__all__'

    # def get_queryset(self):
    #   doubt = self.kwargs['question']
    #   return DoubtAnswers.objects.filter(question = doubt)









# course wise doubt list (get)
# class DoubtsByCourse(ListAPIView):
#     queryset = Doubt.objects.all()
#     serializer_class = DoubtSerializer

#     def get(self, request, *args, **kwargs):
#         course_id = kwargs.get('course_id')
#         self.queryset = Doubt.objects.filter(course = Course( id = course_id))
#         # print(self.queryset) 
#         return self.list(request, *args, **kwargs)   

# chapter wise doubt list(get)
# class DoubtsByChapter(ListAPIView):
#     queryset = Doubt.objects.all()
#     serializer_class = DoubtSerializer
#     # permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         chapter_id = kwargs.get('chapter_id')
#         self.queryset = Doubt.objects.filter(chapter = Chapter( id = chapter_id))
#         # print(self.queryset) 
#         return self.list(request, *args, **kwargs)   
    
