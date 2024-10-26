from django.urls import path

from hello.views import HelloView

app_name = "hello"

urlpatterns = [
    path("", HelloView.as_view(), name="hello"),
]
