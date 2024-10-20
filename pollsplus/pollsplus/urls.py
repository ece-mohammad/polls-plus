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
from polls.views import owner_view, PollsHomeView

urlpatterns = [
    path("", PollsHomeView.as_view(), name="index"),
    path("admin/", admin.site.urls),
    path("polls/", include("polls.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("owner/", owner_view, name="owner"),
]

urlpatterns.extend(
    static("site/", document_root=settings.SITE_ROOT, show_indexes=True)
)

urlpatterns.append(
    path("__debug__", include("debug_toolbar.urls")),
)
