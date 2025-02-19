from django.urls import path

from reloadinator.views import HelloView

app_name = "reloadinator"

urlpatterns = [
    path("", HelloView.as_view(), name="reloadinator"),
]
