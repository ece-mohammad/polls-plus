from django.http import HttpRequest
from django.views.generic import TemplateView
from django.conf import settings


class HelloView(TemplateView):
    template_name = "hello/hello.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_count = self.request.session.get("view_count", 0) + 1
        self.request.session["view_count"] = view_count
        context["view_count"] = view_count
        return context

    def dispatch(self, request: HttpRequest, *args, **kwargs):
        rsp = super().dispatch(request, *args, **kwargs)
        dj4e_cookie = request.COOKIES.get("dj4e_cookie")
        if dj4e_cookie is None:
            rsp.set_cookie("dj4e_cookie", settings.DJ4E_USER_ID)
        return rsp
