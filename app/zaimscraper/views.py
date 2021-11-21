from django.http.response import JsonResponse
from django.http import HttpResponse
from celery.result import AsyncResult

# Create your views here.
SESSION_KEY = 'celery_tasks'

# http://127.0.0.1:8000/zaim
def hello_world(request):

  if request.method == 'GET':
    return HttpResponse( "Hello world!" )

  return HttpResponse("Please use GET!!")

from . import tasks
'''
View for adding tasks
'''
def run_task(request):
  task = tasks.add.delay(20, 30)

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
      'result': task_result.result,
      'traceback': task_result.traceback,
    }

  return JsonResponse(result)