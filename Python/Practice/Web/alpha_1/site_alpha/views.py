from django.shortcuts import render
from django.http import HttpResponse
import datetime

# Create your views here.


def default_page(request):
    return HttpResponse('<h2><B>This is a Test Web!</B></h2>')


def alpha_1(request):
    return render(request, 'alpha_1.html')


def my_page(request):
    return render(request, 'alpha_2.html')

