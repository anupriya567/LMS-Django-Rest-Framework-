from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Order, OrderItem,Subscription
from courses.models import Course
from coupons.models import Coupon
from coupons.serializers import CouponSerializer
from courses.serializers import CourseSerializer
from core.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer


def validateCouponCode(coupon):
        if Coupon.objects.filter(code = coupon).count() > 0: 
            return Response("coupon exists")
        else:    
            return Response("Coupon is not valid")

class OrderCreateSerializer(Serializer):
    courses = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True, required=False)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=False)
    coupon = serializers.CharField(required=False, validators=[validateCouponCode])

    def validate(self, attrs):
        data = dict(attrs)
        course = data.get('course')
        courses = data.get('courses')
        
        error = ValidationError(
            {
            "course": "any one course or courses is required",
            "courses": "any one course or courses is required",
            }
        )

        if (course and courses) or (not course and not courses):
            raise error
    
        return super().validate(attrs)  

class OrderItemSerializer(ModelSerializer):
    course = serializers.CharField(source = 'course.title')
    coupon = serializers.CharField(source = 'coupon.code')
  
    class Meta:
        model= OrderItem
        fields = '__all__'

class OrderSerializer(ModelSerializer):
    order_id = serializers.CharField(max_length=30, required=False)
    user = UserSerializer(read_only=True)
    coupon = CouponSerializer(read_only=True)
    order_items = OrderItemSerializer(read_only=True, many = True)
    class Meta:
        model = Order
        fields = '__all__'

class OrderValidateSerializer(Serializer):
    razorpay_payment_id  = serializers.CharField()
    razorpay_order_id = serializers.CharField()
    razorpay_signature = serializers.CharField()

  
class SubscriptionSerializer(ModelSerializer):
    # course = serializers.CharField(source = 'course.title')
    course = CourseSerializer(read_only = True)
    order = OrderSerializer(read_only = True)
  
    class Meta:
        model = Subscription
        fields = '__all__'

    def to_representation(self, instance):
        json = super().to_representation(instance)
        json.pop('user')
        return json

    
    
