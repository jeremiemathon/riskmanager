from django.urls import path
from django.conf.urls import url, include

from .views import (
    loginView,
    registerView,
    profileView,
    logoutView,
    userListView,
)


urlpatterns = [
    path('login', loginView.as_view(), name='login'),
    path('register', registerView.as_view(), name='register'),
    path('profile', profileView.as_view(), name='profile'),
    path('logout', logoutView.as_view(), name='logout'),
    path('list', userListView.as_view(), name='userlist'),
    
]
