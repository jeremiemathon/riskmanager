from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
)
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User


# Create your views here.
class loginView(LoginView):
    template_name = 'users/login.html'
    def get_redirect_url(self):
        return super().get_redirect_url()

    def get_success_url(self):
        return super().get_success_url()


class registerView(TemplateView):
    template_name = 'users/register.html'


class profileView(TemplateView, LoginRequiredMixin):
    template_name = 'users/profile.html'

class logoutView(LogoutView, LoginRequiredMixin):
    template_name = 'users/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

class userListView(ListView):
    template_name = "users/list.html"
    model = User
