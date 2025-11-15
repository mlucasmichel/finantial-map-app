from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def budget_home(request):
    return HttpResponse("Hello, Budget App!")
