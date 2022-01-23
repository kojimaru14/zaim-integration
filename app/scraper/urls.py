from django.urls import path, include
from . import views

app_name = 'zaim'

urlpatterns = [
    path('', views.hello_world, name="index"),
    path('run', views.run_task, name="run_task"),
    path('rakuten', views.run_rakuten_task, name="run_rakuten"),
    path('tasks', views.list_tasks, name="list_tasks")
]