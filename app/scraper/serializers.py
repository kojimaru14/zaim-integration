from dataclasses import field
from rest_framework import serializers
from .models import Rakuten, Zaim
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from common.util.encryption import encrypt

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

  def create(self, validated_data):
    rakuten = Rakuten.objects.create(**validated_data)
    rakuten.password = encrypt(validated_data['password'])
    rakuten.save()
    return rakuten

  def update(self, instance, validated_data):
    instance.login = validated_data['login']
    instance.password = encrypt(validated_data['password'])
    instance.save()
    return instance


class ZaimSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True)

  class Meta:
    model = Zaim
    fields = ('id', 'login', 'password', 'user')
    extra_kwargs = {'password': {'write_only': True, 'required': True}}

  def create(self, validated_data):
    zaim = Zaim.objects.create(**validated_data)
    zaim.password = encrypt(validated_data['password'])
    zaim.save()
    return zaim

  def update(self, instance, validated_data):
    instance.login = validated_data['login']
    instance.password = encrypt(validated_data['password'])
    instance.save()
    return instance