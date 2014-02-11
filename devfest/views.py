from django.shortcuts import render, HttpResponse

def test(request):
  return HttpResponse('Hey, %s!' % request.user.username)

def test_update(request):
  return [{'name':'username_change', 'model':User, 'params':{'pk':request.user.pk}, 'data':{'username':'object.username'}}]

# Create your views here.
