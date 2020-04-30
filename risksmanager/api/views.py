from rest_framework import viewsets
from .serializers import *
from basic.models import Project, Control, SecurityNeed, SecurityNeedValue, Tag

class ProjectViewSet(viewsets.ModelViewSet):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ControlViewSet(viewsets.ModelViewSet):

    queryset = Control.objects.all()
    serializer_class = ControlSerializer

class TagViewSet(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class UserViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

class SecurityNeedValueViewSet(viewsets.ModelViewSet):

    queryset = SecurityNeedValue.objects.all()
    serializer_class = SecurityNeedValueSerializer

class ProjectControlViewSet(viewsets.ModelViewSet):

    queryset = ProjectControl.objects.all()
    serializer_class = ProjectControlSerializer