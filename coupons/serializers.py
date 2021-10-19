from django.db.models import fields
from django.db.models.base import Model
from coupons.models import Coupon
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class CouponSerializer(ModelSerializer):
    course = serializers.StringRelatedField()
    class Meta:
        model = Coupon
        fields = '__all__'

        