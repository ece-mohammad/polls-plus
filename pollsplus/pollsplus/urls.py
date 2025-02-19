"""
URL configuration for pollsplus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from .views import custom_logout, contact_view, about_view


urlpatterns = [
    path("", include("home.urls")),
    path("contact/", contact_view, name="contact"),
    path("about/", about_view, name="about"),
    path("reloadinator/", include("reloadinator.urls")),
    path("admin/", admin.site.urls),
    path("polls/", include("polls.urls")),
    path("autos/", include("autos.urls")),
    path("cats/", include("cats.urls")),
    path("ads/", include("ads.urls")),
    path("shrt/", include("short_url.urls")),
    path("accounts/logout/", custom_logout, name="custom_logout"),
    path("accounts/", include("django.contrib.auth.urls")),
]

urlpatterns.extend(
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
)

urlpatterns.append(
    path("__debug__", include("debug_toolbar.urls")),
)
