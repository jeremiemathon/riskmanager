
from django.contrib import admin
from django import forms
from .forms import ProjectForm

from .models import (
    Control,
    Project,
    ProjectControl,
    SecurityNeed,
    SecurityNeedValue,
    Tag,
)
class ProjectControlAdmin(admin.ModelAdmin):
    model = ProjectControl
    list_display = ("get_name","control","applicable","status")

    def get_name(self, obj):
        return obj.project.name

    get_name.short_description = 'Project Name'  # Renames column head


# class ProjectForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(ProjectForm, self).__init__(*args, **kwargs)
#         wtf = SecurityNeedValue.objects.all();
#         w = self.fields['security_needs'].widget
#         choices = []
#         for choice in wtf:
#             choices.append((choice.id, choice))
#         w.choices = choices
#
#         tag = Tag.objects.all();
#         t = self.fields['tags'].widget
#         choices2 = []
#         for choice2 in tag:
#             choices2.append((choice2.id, choice2.name))
#         t.choices2 = choices2


class ProjectAdmin(admin.ModelAdmin):
    list_per_page = 100
    ordering = ['code',] # didnt have this one in the example, sorry
    search_fields = ['code', 'name', 'description', 'tags']
    filter_horizontal = ('security_needs', 'tags')
    form = ProjectForm


admin.site.register(Control)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectControl, ProjectControlAdmin)
admin.site.register(SecurityNeed)
admin.site.register(SecurityNeedValue)
admin.site.register(Tag)
