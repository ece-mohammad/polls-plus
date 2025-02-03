# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView
from home.models import Project
from django.http import HttpResponseRedirect


class HomePageView(ListView):
    model = Project

