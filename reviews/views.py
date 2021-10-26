from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from . models import Review
from . serializers import ReviewSerializer
from rest_framework.response import Response
from rest_framework import status
from orders.models import Subscription
from rest_framework.views import APIView
from courses.models import Course
from rest_framework.viewsets import ModelViewSet
from . permissions import AddOwnReviewOnly,AddUpdateReviewToEnrolledCourseOnly,DeleteOwnReviewOnly
# Create your views here.

class ReviewsByCourse(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        course = kwargs.get('course')
        # print(course)
        user = request.user
        self.queryset = Review.objects.filter(course__title = course)
        print(self.queryset)
        return self.list(request, *args, **kwargs)  

class ReviewViewSet(ModelViewSet):
    
    permission_classes = [(IsAuthenticated & AddOwnReviewOnly),
                          (IsAuthenticated & AddUpdateReviewToEnrolledCourseOnly),
                          (IsAuthenticated & DeleteOwnReviewOnly)]

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

    
        

