from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Review
from rest_framework.serializers import ModelSerializer, Serializer
from core.serializers import UserSerializer
from courses.serializers import CourseSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source = 'user.username')
    class Meta:
        model = Review
        fields = '__all__'

    def create(self, validated_data):
        user = self.context.get('request').user
        course = validated_data.get('course')
        try:
            review = user.reviews.all().get(course=course)
            return super().update(review, validated_data=validated_data)
        except Review.DoesNotExist:
            pass

        return super().create(validated_data)    

# class CreateReviewSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     course = CourseSerializer(read_only=True)
#     class Meta:
#         model = Review
#         fields = '__all__'


