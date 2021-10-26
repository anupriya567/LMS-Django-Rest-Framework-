from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .models import Doubt,DoubtAnswers
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer
from core.serializers import UserSerializer
from courses.serializers import CourseSerializer


class DoubtSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = 'user.username',read_only = True)
    class Meta:
        model = Doubt
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user 
        chapter = validated_data['chapter']
        course = validated_data['course']

        msg = {"Doubt Not created" : "This chapter is not present in this course"}

        if (chapter.course != course):
            raise ValidationError(msg)
            # return Response(msg,status= status.HTTP_400_BAD_REQUEST) 
        doubt = Doubt(**validated_data)  
        doubt.save()
        return doubt    
    

class DoubtAnswersSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = 'user.username',read_only = True)
    class Meta:
        model = DoubtAnswers
        fields = '__all__'


    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['user'] = user 
        doubtanswer = DoubtAnswers(**validated_data)  
        doubtanswer.save()
        return doubtanswer      









# class DoubtSerializer(serializers.ModelSerializer):
#     user = serializers.CharField(source = 'user.username',read_only = True)
#     class Meta:
#         model = Doubt
#         fields = '__all__'

#     def create(self, validated_data):
#         user = self.context.get('request').user
#         validated_data['user'] = user 
#         chapter = validated_data['chapter']
#         course = validated_data['course']

#         msg = {"Not created" : "This chapter is not present in this course"}

#         if (chapter.course != course):
#             raise ValidationError(msg)
#             # return Response(msg,status= status.HTTP_400_BAD_REQUEST) 
#         doubt = Doubt(**validated_data)  
#         doubt.save()
#         return doubt
          
 
#     def update(self, instance, validated_data):
#         req_user = self.context.get('request').user
#         doubt_user = instance.user
#         msg = { "Not updated": "You have'nt added this doubt so you can't update this"}

#         if req_user == doubt_user:
#             instance.content = validated_data.get('content')
#             instance.save()
#             return instance
#         raise ValidationError(msg)

#     def destroy(self, request, *args, **kwargs):
#         print("in delete")
#         instance = self.get_object()
#         req_user = self.context.get('request').user
#         doubt_user = instance.user
#         msg = { "Not deleted": "You have'nt added this doubt so you can't delete this"}

#         if req_user == doubt_user:
#             self.perform_destroy(instance)
#             return Response(status=status.HTTP_204_NO_CONTENT)    
#         return Response(msg) 