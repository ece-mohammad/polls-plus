# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "home/home.html"
    extra_context = {
        "app_name": "Home",
        "app_url" : reverse_lazy("home:home")
    }
