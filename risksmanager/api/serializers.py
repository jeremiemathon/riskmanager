from rest_framework import serializers
from basic.models import (
    Project,
    Control,
    ProjectControl,
    SecurityNeed,
    SecurityNeedValue,
    Tag,
    User,
)


class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    # controls = serializers.ModelSerializer(source='projectcontrol_set')
    class Meta:
        model = Project
        fields = "__all__"
        fields = (  
                'url',
                'name',
                'code',
                'description',
                'author',
                'security_needs',
                'tags',
                'contributors',
                'projectcontrol_set',
                )

class ControlSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Control
        fields = "__all__"

class TagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id','username',)

class SecurityNeedValueSerializer(serializers.HyperlinkedModelSerializer):
    attribute = serializers.CharField(source='attribute.name')
    class Meta:
        model = SecurityNeedValue
        fields = ('attribute','value',)

class ProjectControlSerializer(serializers.HyperlinkedModelSerializer):
    # project_id = serializers.CharField(source='project.pk')
    control_id = serializers.CharField(source='control.pk')

    class Meta:
        model = ProjectControl
        fields = ('project','control_id','applicable','status',)

