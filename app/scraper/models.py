from enum import unique
from turtle import ondrag
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Zaim(models.Model):
  login = models.EmailField()
  password = models.CharField(max_length=32)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  class Meta:
    unique_together = (('user','login'),)
    index_together = (('user','login'),)

class Rakuten(models.Model):
  login = models.EmailField()
  password = models.CharField(max_length=32)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  class Meta:
    unique_together = (('user','login'),)
    index_together = (('user','login'),)