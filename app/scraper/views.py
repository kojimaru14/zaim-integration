from django.http.response import JsonResponse
from django.http import HttpResponse
from celery.result import AsyncResult
import datetime

# Add "@basic_auth" decorator to a function with which you want to perform authentication
# More on decorators: https://blog.ikappio.com/decorating-specific-view-basic-authentication-in-django/
from app.decorators.basic_auth_decorator import basic_auth

# Create your views here.
SESSION_KEY = 'celery_tasks'

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from .models import Rakuten, Zaim
from app.scraper.serializers import RakutenSerializer, ZaimSerializer, UserSerializer
from rest_framework.decorators import action

from . import tasks

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def get_queryset(self):
    user = self.request.user
    return User.objects.filter(username=user)


class RakutenViewSet(viewsets.ModelViewSet):
  queryset = Rakuten.objects.all()
  serializer_class = RakutenSerializer
  authentication_classes = [TokenAuthentication, SessionAuthentication]
  permission_classes = (IsAuthenticated, )

  def get_queryset(self):
    return Rakuten.objects.filter(user=self.request.user)

  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  @action(detail=False, methods=['get'])
  def run(self, request):
    
    if request.method == "GET" and "year" in request.GET and "month" in request.GET:
      task = tasks.scrape_rakuten.delay(self.request.user.id, request.GET.get("year"), request.GET.get("month") )
    else:
      dt_now = datetime.datetime.now()
      task = tasks.scrape_rakuten.delay(self.request.user.id, dt_now.year, dt_now.month)

    # my_tasks = request.session.get(SESSION_KEY)

    # if not my_tasks:  # if no existing task, then save the task id as the value for the session key
    #   request.session[SESSION_KEY] = task.id
    # else:             # if there are existing tasks, then concatenate them with the new task.
    #   request.session[SESSION_KEY] = '{},{}'.format(my_tasks, task.id)
    
    return JsonResponse({
      "message": "Your task has been queued.",
      "task_id": task.id,
    })


class ZaimViewSet(viewsets.ModelViewSet):
  queryset = Zaim.objects.all()
  serializer_class = ZaimSerializer
  authentication_classes = [TokenAuthentication, SessionAuthentication]
  permission_classes = (IsAuthenticated, )

  def get_queryset(self):
    return Zaim.objects.filter(user=self.request.user)
        
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)

  @action(detail=False, methods=['get'])
  def run(self, request):

    if request.method == "GET" and "year" in request.GET and "month" in request.GET:
      task = tasks.scrape_and_upload.delay(self.request.user.id, request.GET.get("year"), request.GET.get("month") )
    else:
      dt_now = datetime.datetime.now()
      task = tasks.scrape_and_upload.delay(self.request.user.id, dt_now.year, dt_now.month)

    # my_tasks = request.session.get(self.request.user)

    # if not my_tasks:  # if no existing task, then save the task id as the value for the session key
    #   request.session[SESSION_KEY] = task.id
    # else:             # if there are existing tasks, then concatenate them with the new task.
    #   request.session[SESSION_KEY] = '{},{}'.format(my_tasks, task.id)
    
    return JsonResponse({
      "message": "Your task has been queued.",
      "task_id": task.id,
    })



# http://127.0.0.1:8000/zaim
def hello_world(request):

  if request.method == 'GET':
    return HttpResponse( "Hello world!" )

  return HttpResponse("Please use GET!!")


'''
View for adding tasks
'''
@basic_auth
def run_task(request, username='', password=''):

  if request.method == "GET" and "year" in request.GET and "month" in request.GET:
    task = tasks.scrape_and_upload.delay(username, password, request.GET.get("year"), request.GET.get("month") )
  else:
    dt_now = datetime.datetime.now()
    task = tasks.scrape_and_upload.delay(username, password, dt_now.year, dt_now.month)

  my_tasks = request.session.get(SESSION_KEY)

  if not my_tasks:  # if no existing task, then save the task id as the value for the session key
    request.session[SESSION_KEY] = task.id
  else:             # if there are existing tasks, then concatenate them with the new task.
    request.session[SESSION_KEY] = '{},{}'.format(my_tasks, task.id)
  
  return JsonResponse({
    "message": "Your task has been queued.",
    "task_id": task.id,
  })


@basic_auth
def run_rakuten_task(request, username='', password=''):

  if request.method == "GET" and "year" in request.GET and "month" in request.GET:
    task = tasks.scrape_rakuten.delay(username, password, request.GET.get("year"), request.GET.get("month") )
  else:
    dt_now = datetime.datetime.now()
    task = tasks.scrape_rakuten.delay(username, password, dt_now.year, dt_now.month)

  my_tasks = request.session.get(SESSION_KEY)

  if not my_tasks:  # if no existing task, then save the task id as the value for the session key
    request.session[SESSION_KEY] = task.id
  else:             # if there are existing tasks, then concatenate them with the new task.
    request.session[SESSION_KEY] = '{},{}'.format(my_tasks, task.id)
  
  return JsonResponse({
    "message": "Your task has been queued.",
    "task_id": task.id,
  })


'''
View for getting task status
'''
def list_tasks(request):

  result = {}
  task_ids = []

  if request.method == "GET" and "id" in request.GET:
    task_ids.append(request.GET.get("id"))
  else:
    my_tasks = request.session.get(SESSION_KEY)
    if my_tasks:
      task_ids = my_tasks.split(',')

  for task_id in task_ids:
    task_result = AsyncResult(task_id)

    result[task_id] = {
      'status': task_result.status,
      'result': str(task_result.result),
      'traceback': str(task_result.traceback),
    }

  return JsonResponse(result)