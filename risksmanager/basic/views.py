import plotly.offline as opy
import plotly.graph_objs as go

from django.urls import reverse_lazy
from django.http import JsonResponse

from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
    DetailView,
    TemplateView,
)

from .models import (
    Project,
    ProjectControl,
    SecurityNeedValue,
    SecurityNeed,
    Control,
    Tag,
)

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ProjectForm, ControlForm, TagForm, ProjectControlForm


class Graph(TemplateView):
    template_name = 'basic/graphs.html'

    def get_context_data(self, **kwargs):
        context = super(Graph, self).get_context_data(**kwargs)

        x = [-2,0,4,6,7]
        y = [q**2-q+3 for q in x]
        trace1 = go.Scatter(x=x, y=y, marker={'color': 'red', 'symbol': 104, 'size': 10},
                            mode="lines",  name='1st Trace')

        data=go.Data([trace1])
        layout=go.Layout(title="Meine Daten", xaxis={'title':'x1'}, yaxis={'title':'x2'})
        figure=go.Figure(data=data,layout=layout)
        div = opy.plot(figure, auto_open=False, output_type='div')

        context['graph'] = div

        return context


def create_project_control(self, form):
    controls = Control.objects.all()
    #ProjectControl.objects.filter(project=Project.objects.get(pk=form.instance.pk)).delete()
    for security_need in form.instance.security_needs.all():  # pour chaque besoin de sécurité du projet
        for control in controls:  # pour chaque controle
            for applicable_securityneedvalue in control.applicable_securityneedvalue.all():  # pour chaque besoin de sécurité applicable
                if (security_need == applicable_securityneedvalue):
                    for tag in form.instance.tags.all():
                        for controltag in control.applicable_tags.all():
                            if (tag == controltag):
                                if (ProjectControl.objects.filter(
                                        project=Project.objects.get(pk=form.instance.pk)).filter(
                                        control=Control.objects.get(pk=control.pk)).count() == 0):
                                    ProjectControl.objects.get_or_create(
                                        project=Project.objects.get(pk=form.instance.pk),
                                        control=Control.objects.get(pk=control.pk),
                                        applicable="A",
                                        status="NP",
                                    )

def create_control_project(self, form):
    print("Beginning Control Update to Projects")
    projects = Project.objects.all()
    #ProjectControl.objects.filter(project=Project.objects.get(pk=form.instance.pk)).delete()
    for security_need in form.instance.applicable_securityneedvalue.all():  # pour chaque besoin de sécurité applicable
        for project in projects:
            for project_securityneed in project.security_needs.all():
                if (security_need == project_securityneed):
                    for tag in form.instance.applicable_tags.all():
                        for projecttag in project.tags.all():
                            if (tag == projecttag):
                                if (ProjectControl.objects.filter(
                                        project=Project.objects.get(pk=project.pk)).filter(
                                        control=Control.objects.get(pk=form.instance.pk)).count() == 0):
                                            ProjectControl.objects.get_or_create(
                                                project=Project.objects.get(pk=project.pk),
                                                control=Control.objects.get(pk=form.instance.pk),
                                                applicable="A",
                                                status="NP",
                                            )
                                            print("Control Non Existant -> Applicable Project : " + str(project.code))

def get_data(self, form):
    return JsonResponse()


class portalnewListView(ListView):
    model = Project
    template_name = "basic/index.html"
    context_object_name = 'projects'

    def get(self, request):
        context = {
            'title': 'Security Policy - Policy Detail',
            'projects': Project.objects.all(),
        }

        return render(request, 'basic/index.html', context)

class portalListView(ListView):
    model = Project
    template_name = "basic/portal.html"
    context_object_name = 'projects'

    def get(self, request):
        context = {
            'title': 'Security Policy - Policy Detail',
            'projects': Project.objects.all(),
        }

        return render(request, 'basic/portal.html', context)

class projectListView(ListView):
    model = Project
    template_name = "basic/project.html"

    def get(self, request, id):
        context = {
            'project': Project.objects.get(pk=id),
            'projectcontrols': ProjectControl.objects.all(),
        }
        return render(request, 'basic/project.html', context)


class projectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    login_url = '/admin/'
    #fields = '__all__'
    form_class = ProjectForm


    def get_context_data(self, *args, **kwargs):
        context = super(projectCreateView, self).get_context_data(*args, **kwargs)

        context.update({
            'securityneedvalues': SecurityNeedValue.objects.all().values_list('value', flat=True).distinct(),
            'securityneed': SecurityNeed.objects.all().values_list('name', flat=True).distinct(),
        })

        return context



    def form_valid(self, form):
        response = super(projectCreateView, self).form_valid(form)
        create_project_control(self, form)
        form.instance.author = self.request.user
        #form.instance.contributors = self.request.user

        return response


class projectDeleteView(DeleteView):
    model = Project
    success_url = reverse_lazy('portal')


class projectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        response = super(projectUpdateView, self).form_valid(form)
        print("Update Form Valid")
        create_project_control(self, form)
        return response

class projectDetailView(UpdateView):
    model  = Project
    # form_class = ControlForm
    template_name = "basic/project.html"

    def get(self, request, id):
        context = {
            'project': Project.objects.get(pk=id),
            'projectcontrols': ProjectControl.objects.all(),
        }
        return render(request, 'basic/project.html', context)


class controlUpdateView(UpdateView):
    model = Control
    fields = '__all__'
   #form_class = ProjectForm

    def form_valid(self, form):
        response = super(controlUpdateView, self).form_valid(form)
        print("Update Form Valid")
        create_control_project(self, form)
        return response




class projectControlUpdateView(UpdateView):
    model = ProjectControl
    form_class = ProjectControlForm

class projectControlDeleteView(DeleteView):
    model = ProjectControl
    success_url = "/"




class controlListView(ListView):
    model = Control
    context_object_name = 'controls'

class controlDetailView(UpdateView):
    model  = Control
    form_class = ControlForm

    def form_valid(self, form):
        response = super(controlDetailView, self).form_valid(form)
        #create_project_control(self, form)
        return response

class controlCreateView(CreateView):
    model = Control
    fields = '__all__'

class securityNeedListValueView(ListView):
    model = SecurityNeedValue

class securityNeedListView(ListView):
    model = SecurityNeed

    '''def get_context_data(self, *args, **kwargs):
        context = super(securityNeedListView, self).get_context_data(*args, **kwargs)

        context.update({
            'securityneedvalue_list': SecurityNeedValue.objects.all().values_list('value', flat=True),
        })

        return context'''

class securityNeedCreateView(CreateView):
    model = SecurityNeed
    fields = '__all__'


class securityNeedDetailView(DetailView):
    model = SecurityNeed


class tagListView(ListView):
    model = Tag
    context_object_name = 'tags'

class tagDetailView(DetailView):
    model  = Tag
    form_class = TagForm

class tagCreateView(CreateView):
    model = Tag
    fields = '__all__'

class tagUpdateView(UpdateView):
    model = Tag
    form_class = TagForm

class tagDeleteView(DeleteView):
    model = Tag
    fields = '__all__'
    success_url = reverse_lazy('tags')




