# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home/home.html"
