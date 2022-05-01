from django.urls import path, include
from . import views
from rest_framework import routers

app_name = 'zaim'

router = routers.DefaultRouter()
router.register('users', views.UserViewSet)
router.register('rakuten', views.RakutenViewSet)
router.register('zaim', views.ZaimViewSet)

urlpatterns = [
    # path('', views.hello_world, name="index"),
    path('', include(router.urls)),
    path('run', views.run_task, name="run_task"),
    path('rakuten', views.run_rakuten_task, name="run_rakuten"),
    path('tasks', views.list_tasks, name="list_tasks")
]