from django.shortcuts import render

# Create your views here.
# from django.http import HttpResponse
# def index(request):
#     return HttpResponse('Hello, world. You\'re at the lab index.<br><a href="unidad">Unidad</a>')

from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from lab.models import Unidad, Prueba, Paciente, Orden

from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
from . import forms
class HomePageView(TemplateView):
    template_name = "lab/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['latest_articles'] = Article.objects.all()[:5]
        return context

class UnidadListView(ListView):

    model = Unidad
    # paginate_by = 100  # if pagination is desired

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context

class UnidadCreate(CreateView):
    model = Unidad
    fields = ['sigla', 'descrip']
    success_url = reverse_lazy('unidad-list')

class UnidadUpdate(UpdateView):
    model = Unidad
    fields = ['sigla', 'descrip']
    # template_name_suffix = '_update_form'
    success_url = reverse_lazy('unidad-list')

class UnidadDelete(DeleteView):
    model = Unidad
    success_url = reverse_lazy('unidad-list')
    # def post(self, request, *args, **kwargs):
    #     if "cancel" in request.POST:
    #         url = self.get_success_url()
    #         return HttpResponseRedirect(url)
    #     else:
    #         return super(UnidadDelete, self).post(request, *args, **kwargs)

class PruebaListView(ListView):
    model = Prueba
class PruebaCreate(CreateView):
    model = Prueba
    fields = '__all__' #['nombre', 'unidad', 'minimo', 'maximo']
    success_url = reverse_lazy('prueba-list')

class PruebaUpdate(UpdateView):
    model = Prueba
    fields = '__all__'
    # template_name_suffix = '_update_form'
    success_url = reverse_lazy('prueba-list')

class PruebaDelete(DeleteView):
    model = Prueba
    success_url = reverse_lazy('prueba-list')
    # def post(self, request, *args, **kwargs):
    #     if "cancel" in request.POST:
    #         url = self.get_success_url()
    #         return HttpResponseRedirect(url)
    #     else:
    #         return super(UnidadDelete, self).post(request, *args, **kwargs)
class PacienteListView(ListView):
    model = Paciente
class PacienteCreate(CreateView):
    model = Paciente
    fields = '__all__'
    success_url = reverse_lazy('paciente-list')

class PacienteUpdate(UpdateView):
    model = Paciente
    fields = '__all__'
    success_url = reverse_lazy('paciente-list')

class PacienteDelete(DeleteView):
    model = Paciente
    success_url = reverse_lazy('paciente-list')






class OrdenListView(ListView):
    model = Orden
    ordering = ['-fecha_alta']

class OrdenCreate(CreateView):
    model = Orden
    # fields = '__all__'
    form_class = forms.OrdenForm
    success_url = reverse_lazy('orden-list')

class OrdenUpdate(UpdateView):
    model = Orden
    # fields = '__all__'
    form_class = forms.OrdenForm
    success_url = reverse_lazy('orden-list')

class OrdenDelete(DeleteView):
    model = Orden
    success_url = reverse_lazy('orden-list')

