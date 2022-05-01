from dataclasses import field
from rest_framework import serializers
from .models import Rakuten, Zaim
from django.contrib.auth.models import User

class UserSeralizer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'password')
    extra_kwargs = {'password': {'write_only': True, 'required': True}}
  
  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    return user

class RakutenSeralizer(serializers.ModelSerializer):
  class Meta:
    model = Rakuten
    fields = ('id', 'login', 'password', 'user')
    extra_kwargs = {'password': {'write_only': True, 'required': True}}

class ZaimSeralizer(serializers.ModelSerializer):
  class Meta:
    model = Zaim
    fields = ('id', 'login', 'password', 'user')
    extra_kwargs = {'password': {'write_only': True, 'required': True}}