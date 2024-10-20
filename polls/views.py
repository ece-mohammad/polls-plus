from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

# Create your views here.
def index(request: HttpRequest):
    return HttpResponse("Hello, world. You're at the polls index. ( from 3e809dd3 )")
