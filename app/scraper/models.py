from django.db import models
from django.contrib.auth.models import User
from encrypted_fields.fields import EncryptedTextField

class Zaim(models.Model):
  login = models.EmailField()
  password = EncryptedTextField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  class Meta:
    unique_together = (('user','login'),)
    index_together = (('user','login'),)

class Rakuten(models.Model):
  login = models.EmailField()
  password = EncryptedTextField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  class Meta:
    unique_together = (('user','login'),)
    index_together = (('user','login'),)

