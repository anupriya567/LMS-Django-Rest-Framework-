from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Course, Category, Tag
from chapters.models import Chapter
from rest_framework.serializers import ModelSerializer


class CategorySerializer(ModelSerializer):
    courses = serializers.StringRelatedField(many=True)
    class Meta:
        model = Category
        fields = '__all__'

class CourseSerializer(ModelSerializer):
    tags = serializers.StringRelatedField(many=True,read_only=True)
    category = serializers.CharField(source = 'category.title')
    # students_enrolled = serializers.SerializerMethodField()
    # category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'
    
    # def get_students_enrolled(self,instance):
    #     course = instance
    #     return course.cal_students_enrolled()  
        

         
    def to_representation(self, instance):
        data = super().to_representation(instance)

        request = self.context.get('request')
        user = request.user
        course = instance
        data['is_enrolled'] = course.is_user_enrolled(user)
        data['students_enrolled'] = course.cal_students_enrolled()
        return data    

class TagSerializer(ModelSerializer):
    # to view full details of course 
    # course = CourseSerializer(read_only=True) 
    course = serializers.CharField(source = 'course.title')
    class Meta:
        model = Tag
        fields = '__all__'


