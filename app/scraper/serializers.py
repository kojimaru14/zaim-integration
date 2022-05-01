from dataclasses import field
from rest_framework import serializers
from .models import Rakuten, Zaim
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'username', 'password')
    extra_kwargs = {'password': {'write_only': True, 'required': True}}
  
  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    token = Token.objects.create(user=user)
    return user


class RakutenSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)

  class Meta:
    model = Rakuten
    fields = ('id', 'login', 'password', 'user')
    extra_kwargs = {'password': {'write_only': True, 'required': True}}


class ZaimSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)

  class Meta:
    model = Zaim
    fields = ('id', 'login', 'password', 'user')
    extra_kwargs = {'password': {'write_only': True, 'required': True}}