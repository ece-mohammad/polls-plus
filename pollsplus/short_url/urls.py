from django.urls import path, re_path

from short_url.views import HomePageView, ShortUrlView

app_name = "short_url"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    re_path(r"^(?P<slug>[a-zA-Z0-9_\-=]+)$", ShortUrlView.as_view(), name="expand"),
]
