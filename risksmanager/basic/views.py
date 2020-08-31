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
from plotly.offline import plot
from plotly.graph_objs import Scatter, Pie, Data, Layout, Figure
from django.db.models import Q



def create_project_control(self, form):
    myproject = Project.objects.get(pk=form.instance.pk)
    print(myproject.projectcontrol_set.all())
    controls = Control.objects.all()
    # ProjectControl.objects.filter(project=Project.objects.get(pk=form.instance.pk)).delete()
    for security_need in form.instance.security_needs.all():  # pour chaque besoin de sécurité du projet
        for control in controls:  # pour chaque controle
            # pour chaque besoin de sécurité applicable
            for applicable_securityneedvalue in control.applicable_securityneedvalue.all():
                if (security_need == applicable_securityneedvalue):
                    for tag in form.instance.tags.all():
                        for controltag in control.applicable_tags.all():
                            if (tag == controltag):
                                if (
                                        ProjectControl.objects.filter(
                                        project=Project.objects.get(pk=form.instance.pk)).filter(
                                        control=Control.objects.get(pk=control.pk)).count() == 0
                                    ):
                                    ProjectControl.objects.get_or_create(
                                        project=Project.objects.get(
                                            pk=form.instance.pk),
                                        control=Control.objects.get(
                                            pk=control.pk),
                                        applicable="A",
                                        status="NP",
                                    )
                                # form.instance.controls.add(control)
                                    
                                


def create_control_project(self, form):
    print("Beginning Control Update to Projects")
    projects = Project.objects.all()
    # ProjectControl.objects.filter(project=Project.objects.get(pk=form.instance.pk)).delete()
    # pour chaque besoin de sécurité applicable
    for security_need in form.instance.applicable_securityneedvalue.all():
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
                                        project=Project.objects.get(
                                            pk=project.pk),
                                        control=Control.objects.get(
                                            pk=form.instance.pk),
                                        applicable="A",
                                        status="NP",
                                    )
                                    print(
                                        "Control Non Existant -> Applicable Project : " + str(project.code))
                                
                            


def get_data(self, form):
    return JsonResponse()


class portalnewListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "basic/index.html"
    context_object_name = 'projects'

    def get(self, request):
        context = {
            'title': 'Security Policy - Policy Detail',
            'projects': Project.objects.all(),
        }

        return render(request, 'basic/index.html', context)


class portalListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = "basic/portal.html"
    context_object_name = 'projects'

    def calculate_summary(self):
        projects = Project.objects.all()
        for project in projects:
            print(project.name)
            project.done = ProjectControl.objects.filter(Q(project=project.id) & Q(status="D")).count()
            project.notplanned = ProjectControl.objects.filter(Q(project=project.id) & Q(status="NP")).count()
            project.planned = ProjectControl.objects.filter(Q(project=project.id) & Q(status="P")).count()
            project.total = project.done + project.notplanned + project.planned
            if ( project.done == 0 | project.total == 0 | project.notplanned == 0):
                project.complete = '%02d' % 0
                project.planned = '%02d' % 0
                project.notplanned = '%02d' % 100
            else:
                project.complete = '%02d' % (project.done / project.total * 100)
                project.planned = '%02d' % (project.planned / project.total * 100)
                project.notplanned = '%02d' % (project.notplanned / project.total * 100)
            print(project.complete)
        return(projects)


    def get(self, request):
        context = {
            'title': 'Security Policy - Policy Detail',
            'projects': self.calculate_summary(),
        }

        return render(request, 'basic/portal.html', context)


class projectListView(LoginRequiredMixin, ListView):
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
    # login_url = '/admin/'
    #fields = '__all__'
    form_class = ProjectForm

    def get_context_data(self, *args, **kwargs):
        context = super(projectCreateView, self).get_context_data(
            *args, **kwargs)

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


class projectDeleteView(LoginRequiredMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('portal')


class projectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm

    def form_valid(self, form):
        response = super(projectUpdateView, self).form_valid(form)
        print("Update Form Valid")
        create_project_control(self, form)
        return response


class projectDetailView(LoginRequiredMixin, UpdateView):
    model = Project
    # form_class = ControlForm
    template_name = "basic/project.html"

    def get(self, request, id):
        layout = Layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
        )
        x_data = [0, 1, 2, 3]
        y_data = [x**2 for x in x_data]
        labels = ['Done', 'Not Planned', 'Planned']

        done = ProjectControl.objects.filter(Q(project=id) & Q(status="D")).count()
        notplanned = ProjectControl.objects.filter(Q(project=id) & Q(status="NP")).count()
        planned = ProjectControl.objects.filter(Q(project=id) & Q(status="P")).count()
        
        values = [done, notplanned, planned]
        # plot_div = plot([Scatter(x=x_data, y=y_data,
        #                          mode='lines', name='test',
        #                          opacity=0.8, marker_color='green')],
        #                 output_type='div')

        data = Data([Pie(labels=labels, values=values,
                             opacity=0.8)])
        fig = Figure(data=data, layout=layout)   
        plot_div = plot(fig, output_type='div')

        context = {
            'project': Project.objects.get(pk=id),
            # 'projectcontrols': ProjectControl.objects.all(),
            'plot_div': plot_div,
        }
        return render(request, 'basic/project.html', context)


class controlUpdateView(LoginRequiredMixin, UpdateView):
    model = Control
    fields = '__all__'
   #form_class = ProjectForm

    def form_valid(self, form):
        response = super(controlUpdateView, self).form_valid(form)
        print("Update Form Valid")
        create_control_project(self, form)
        return response


class projectControlUpdateView(LoginRequiredMixin, UpdateView):
    model = ProjectControl
    form_class = ProjectControlForm


class projectControlDeleteView(LoginRequiredMixin, DeleteView):
    model = ProjectControl
    success_url = "/"


class controlListView(LoginRequiredMixin, ListView):
    model = Control
    context_object_name = 'controls'


class controlDetailView(LoginRequiredMixin, UpdateView):
    model = Control
    form_class = ControlForm

    def form_valid(self, form):
        response = super(controlDetailView, self).form_valid(form)
        #create_project_control(self, form)
        return response


class controlCreateView(LoginRequiredMixin, CreateView):
    model = Control
    fields = '__all__'


class securityNeedListValueView(LoginRequiredMixin, ListView):
    model = SecurityNeedValue


class securityNeedListView(LoginRequiredMixin, ListView):
    model = SecurityNeed

    '''def get_context_data(self, *args, **kwargs):
        context = super(securityNeedListView, self).get_context_data(*args, **kwargs)

        context.update({
            'securityneedvalue_list': SecurityNeedValue.objects.all().values_list('value', flat=True),
        })

        return context'''


class securityNeedCreateView(LoginRequiredMixin, CreateView):
    model = SecurityNeed
    fields = '__all__'


class securityNeedDetailView(LoginRequiredMixin, DetailView):
    model = SecurityNeed


class tagListView(LoginRequiredMixin, ListView):
    model = Tag
    context_object_name = 'tags'


class tagDetailView(LoginRequiredMixin, DetailView):
    model = Tag
    form_class = TagForm


class tagCreateView(LoginRequiredMixin, CreateView):
    model = Tag
    fields = '__all__'


class tagUpdateView(LoginRequiredMixin, UpdateView):
    model = Tag
    form_class = TagForm


class tagDeleteView(LoginRequiredMixin, DeleteView):
    model = Tag
    fields = '__all__'
    success_url = reverse_lazy('tags')
