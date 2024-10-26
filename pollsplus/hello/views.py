from django.http import HttpRequest
from vanilla import TemplateView


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
            rsp.set_cookie("dj4e_cookie", "c3d67032")
        return rsp
