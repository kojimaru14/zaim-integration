from dataclasses import field
from rest_framework import serializers
from .models import Rakuten, Zaim

class RakutenSeralizer(serializers.ModelSerializer):
  class Meta:
    model = Rakuten
    fields = ('id', 'login', 'password', 'user')

class ZaimSeralizer(serializers.ModelSerializer):
  class Meta:
    model = Zaim
    fields = ('id', 'login', 'password', 'user')