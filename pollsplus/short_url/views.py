from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from urllib.parse import urlunparse, urljoin
from short_url.forms import ShortUrlForm
from short_url.models import ShortURL


# Create your views here.

class HomePageView(CreateView):
    model = ShortURL
    form_class = ShortUrlForm
    success_url = reverse_lazy("short_url:home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug: str | None = self.request.session.get("slug")
        if slug:
            del self.request.session["slug"]
            url = urlunparse(
                (
                    self.request.scheme,
                    self.request.get_host(),
                    urljoin(self.request.path, slug),
                    "",
                    "",
                    ""
                )
            )
            context["url"] = url
            print(f"{url}")
        return context

    def form_valid(self, form):
        rsp = super().form_valid(form)
        self.request.session["slug"] = self.object.slug
        return rsp


class ShortUrlView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        short_url = kwargs.get("slug")
        url = get_object_or_404(ShortURL, slug=short_url)
        return HttpResponseRedirect(url.url)
