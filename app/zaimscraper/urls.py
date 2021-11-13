from django.urls import path, include
from . import views

app_name = 'password'
urlpatterns = [
    path('', views.hello_world, name="index"),
]