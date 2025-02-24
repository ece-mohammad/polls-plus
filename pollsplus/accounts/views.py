from django.contrib.auth import logout
from django.http import (
    HttpResponseRedirect,
    HttpRequest
)
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.generic import View

# Create your views here.


@method_decorator(never_cache, name='dispatch')
class CustomLogoutView(View):

    def post(self, request: HttpRequest, *args, **kwargs):
        return HttpResponseRedirect(
            reverse_lazy("account_logout")
        )

    def get(self, request, *args, **kwargs):
        next_page = request.GET.get('next', '/')
        logout(request)
        return redirect(next_page)
