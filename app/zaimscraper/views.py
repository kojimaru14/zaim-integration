from django.shortcuts import render
from django.http import HttpResponse, Http404

# Create your views here.

import json
# http://127.0.0.1:8000/zaim
def hello_world(request):

  if request.method == 'GET':
    return HttpResponse( "Hello world!" )

  return HttpResponse("Please use GET!!")