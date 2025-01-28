"""
URL configuration for pollsplus project.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("", include("home.urls")),
    path("hello/", include("hello.urls")),
    path("admin/", admin.site.urls),
    path("polls/", include("polls.urls")),
    path("autos/", include("autos.urls")),
    path("cats/", include("cats.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("__debug__", include("debug_toolbar.urls")),
]

urlpatterns.extend(
    static("site/", document_root=settings.SITE_ROOT, show_indexes=True)
)
