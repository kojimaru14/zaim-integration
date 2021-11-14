from django.urls import path, include
from . import views

app_name = 'zaim'

urlpatterns = [
    path('', views.hello_world, name="index"),
    path('task', views.task, name="task"),
]