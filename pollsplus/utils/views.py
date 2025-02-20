from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


class OwnerMixin(LoginRequiredMixin):
    """
    A Mixin to limit the user access to only their ads
    """

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class AuthorMixin(LoginRequiredMixin):

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user)


class UserListView(ListView):
    ...


class UserDetailView(DetailView):
    ...


class LoggedInUserCreateView(LoginRequiredMixin, CreateView):
    ...


class AuthorUpdateView(AuthorMixin, UpdateView):
    ...


class AuthorDeleteView(AuthorMixin, DeleteView):
    ...
