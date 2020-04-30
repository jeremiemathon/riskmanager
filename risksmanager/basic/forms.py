from django import forms
from .models import Project, SecurityNeedValue, Tag, Control, ProjectControl

class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        success_url = '/'
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        #self.fields['author'].widget = forms.HiddenInput()

        self.fields["security_needs"].widget = forms.widgets.SelectMultiple()
        #self.fields["security_needs"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["security_needs"].queryset = SecurityNeedValue.objects.all()
        # self.fields["contributors"].widget = forms.CheckboxSelectMultiple()

        wtf = SecurityNeedValue.objects.all();
        w = self.fields['security_needs'].widget
        choices = []
        for choice in wtf:
            choices.append((choice.id, choice))
        w.choices = choices

        tag = Tag.objects.all();
        t = self.fields['tags'].widget
        choices2 = []
        for choice2 in tag:
            choices2.append((choice2.id, choice2.name))
        t.choices2 = choices2


class ControlForm(forms.ModelForm):

    class Meta:
        model = Control
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ControlForm, self).__init__(*args, **kwargs)
        self.fields["applicable_securityneedvalue"].widget = forms.widgets.SelectMultiple()
        self.fields["applicable_securityneedvalue"].queryset = SecurityNeedValue.objects.all()

        self.fields["applicable_tags"].widget = forms.widgets.SelectMultiple()
        self.fields["applicable_tags"].queryset = Tag.objects.all()


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = '__all__'


class ProjectControlForm(forms.ModelForm):

    class Meta:
        model = ProjectControl
        #fields = '__all__'
        fields = ['control', 'project', 'applicable', 'status']

    def __init__(self, *args, **kwargs):
        super(ProjectControlForm, self).__init__(*args, **kwargs)
        self.fields['project'].widget.attrs['readonly'] = True
        #self.fields['project'].widget = forms.widgets.TextInput(attrs={'readonly':'readonly'})

        self.fields['control'].widget.attrs['readonly'] = True