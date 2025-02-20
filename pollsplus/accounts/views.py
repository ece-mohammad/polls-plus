from django.contrib.auth import logout
from django.contrib.auth.views import (
    LoginView
)
from django.http import (
    HttpResponseNotAllowed
)
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from accounts.forms import CustomAuthenticationForm


# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = CustomAuthenticationForm


class CustomLogoutView(View):

    @method_decorator(never_cache)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return HttpResponseNotAllowed(['GET'])
        return self.get(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        next_page = request.GET.get('next', '/')
        logout(request)
        return redirect(next_page)
