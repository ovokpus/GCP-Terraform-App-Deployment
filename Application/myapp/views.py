from django.shortcuts import render
from .models import Course
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.

def index(request):
    return HttpResponse("Hello")

def listData(request):
    course = Course.objects.all()
    return render(request, 'courses_view.html', {'course' : course})

@csrf_exempt     
def searchCourse(request):
    content = request.POST['query']
    items = Course.objects.filter(title__icontains=content)
    return render(request, 'courses_view.html', {'course' : items})
