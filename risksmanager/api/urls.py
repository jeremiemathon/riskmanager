from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'project', views.ProjectViewSet)
router.register(r'securityneedvalue', views.SecurityNeedValueViewSet)
router.register(r'projectcontrol', views.ProjectControlViewSet)
router.register(r'control', views.ControlViewSet)
router.register(r'tag', views.TagViewSet)
router.register(r'user', views.UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
