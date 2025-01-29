from django.urls import path
from ads.views import HomePageView, AdDetailView, AdCreateView, AdUpdateView, AdDeleteView

app_name = "ads"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("ad/<int:pk>/", AdDetailView.as_view(), name="ad_details"),
    path("ad/create/", AdCreateView.as_view(), name="ad_create"),
    path("ad/<int:pk>/update/", AdUpdateView.as_view(), name="ad_update"),
    path("ad/<int:pk>/delete/", AdDeleteView.as_view(), name="ad_delete"),
]