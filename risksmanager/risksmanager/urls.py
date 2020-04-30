"""risksmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from basic.views import (
    portalListView,
    portalnewListView,
    projectListView,
    projectCreateView,
    projectDeleteView,
    projectUpdateView,
    projectControlUpdateView,
    projectControlDeleteView,
    projectDetailView,
    controlListView,
    controlDetailView,
    controlCreateView,
    controlUpdateView,
    securityNeedListView,
    securityNeedCreateView,
    securityNeedDetailView,
    securityNeedListValueView,
    tagCreateView,
    tagDetailView,
    tagListView,
    tagDeleteView,
    tagUpdateView,
    Graph,
)
from django.conf import settings
from basic import views

from rest_framework import routers
# from risksmanager.api.views import (
#     ProjectViewSet,
# )
#
# router = routers.DefaultRouter()
# router.register(r'project', ProjectViewSet)

urlpatterns = [
    path('new', portalnewListView.as_view(), name='newportal'),
    path('', portalListView.as_view(), name='portal'),
    path('project/<int:pk>/delete', projectDeleteView.as_view(), name='projectdelete'),
    path('project/<int:pk>/update', projectUpdateView.as_view(), name='projectupdate'),
    path('project/<int:id>', projectDetailView.as_view(), name='project'),
    path('project/new', projectCreateView.as_view(), name='projectnew'),

    path('controls', controlListView.as_view(), name='controls'),
    path('control/<int:pk>', controlUpdateView.as_view(), name='control'),
    path('control/new', controlCreateView.as_view(), name='controlnew'),

    path('projectcontrol/<int:pk>/update', projectControlUpdateView.as_view(), name='projectcontrolupdate'),
    path('projectcontrol/<int:pk>/delete', projectControlDeleteView.as_view(), name='projectcontroldelete'),

    path('needs',securityNeedListView.as_view(), name="needs"),
    path('need/<int:pk>',securityNeedDetailView.as_view(), name="need"),
    path('need/new',securityNeedCreateView.as_view(), name="neednew"),

    path('needvalues', securityNeedListValueView.as_view(), name="needvalues"),
    path('needvalue/<int:pk>', securityNeedDetailView.as_view(), name="needvalue"),
    path('needvalue/new', securityNeedCreateView.as_view(), name="needvaluenew"),

    path('tags',tagListView.as_view(), name="tags"),
    path('tag/<int:pk>',tagDetailView.as_view(), name="tag"),
    path('tag/new',tagCreateView.as_view(), name="tagnew"),
    path('tag/<int:pk>/delete',tagDeleteView.as_view(), name="tagdelete"),
    path('tag/<int:pk>/update',tagUpdateView.as_view(), name="tagupdate"),

    path('graphs', Graph.as_view(), name="graphs"),

    path('admin/', admin.site.urls, name="admin"),
    path('api/', include('api.urls')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),

        # For django versions before 2.0:
        # url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns


