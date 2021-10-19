from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', "last_name",
                  'email', 'username', 'is_superuser']

