from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
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

from rolepermissions.mixins import HasRoleMixin

# para ser heredada por las clases de views genéricas que requieren autenticación
class LoginRequired(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'

class RecepcionRequired(HasRoleMixin, LoginRequired):
    allowed_roles = 'recepcion'
class LaboratorioRequired(HasRoleMixin, LoginRequired):
    allowed_roles = 'laboratorio'

class HomePageView(TemplateView):
    template_name = "lab/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['latest_articles'] = Article.objects.all()[:5]
        return context

class UnidadListView(LaboratorioRequired,ListView):
    model = Unidad
    # paginate_by = 100  # if pagination is desired

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['now'] = timezone.now()
    #     return context

class UnidadCreate(LaboratorioRequired,CreateView):
    model = Unidad
    fields = ['sigla', 'descrip']
    success_url = reverse_lazy('unidad-list')

class UnidadUpdate(LaboratorioRequired,UpdateView):
    model = Unidad
    fields = ['sigla', 'descrip']
    # template_name_suffix = '_update_form'
    success_url = reverse_lazy('unidad-list')

class UnidadDelete(LaboratorioRequired,DeleteView):
    model = Unidad
    success_url = reverse_lazy('unidad-list')
    # def post(self, request, *args, **kwargs):
    #     if "cancel" in request.POST:
    #         url = self.get_success_url()
    #         return HttpResponseRedirect(url)
    #     else:
    #         return super(UnidadDelete, self).post(request, *args, **kwargs)

class PruebaListView(LaboratorioRequired,ListView):
    model = Prueba
class PruebaCreate(LaboratorioRequired,CreateView):
    model = Prueba
    fields = '__all__' #['nombre', 'unidad', 'minimo', 'maximo']
    success_url = reverse_lazy('prueba-list')

class PruebaUpdate(LaboratorioRequired,UpdateView):
    model = Prueba
    fields = '__all__'
    # template_name_suffix = '_update_form'
    success_url = reverse_lazy('prueba-list')

class PruebaDelete(LaboratorioRequired,DeleteView):
    model = Prueba
    success_url = reverse_lazy('prueba-list')
    # def post(self, request, *args, **kwargs):
    #     if "cancel" in request.POST:
    #         url = self.get_success_url()
    #         return HttpResponseRedirect(url)
    #     else:
    #         return super(UnidadDelete, self).post(request, *args, **kwargs)
class PacienteListView(RecepcionRequired,ListView):
    model = Paciente
class PacienteCreate(RecepcionRequired,CreateView):
    model = Paciente
    form_class = forms.PacienteForm
    # fields = '__all__'
    success_url = reverse_lazy('paciente-list')

class PacienteUpdate(RecepcionRequired,UpdateView):
    model = Paciente
    form_class = forms.PacienteForm
    # fields = '__all__'
    success_url = reverse_lazy('paciente-list')

class PacienteDelete(RecepcionRequired,DeleteView):
    model = Paciente
    success_url = reverse_lazy('paciente-list')

class OrdenListView(RecepcionRequired,ListView):
    model = Orden
    ordering = ['-fecha_alta']

class OrdenCreate(RecepcionRequired,CreateView):
    model = Orden
    # fields = '__all__'
    form_class = forms.OrdenForm
    success_url = reverse_lazy('orden-list')

class OrdenUpdate(RecepcionRequired,UpdateView):
    model = Orden
    # fields = '__all__'
    form_class = forms.OrdenForm
    success_url = reverse_lazy('orden-list')

class OrdenDelete(RecepcionRequired,DeleteView):
    model = Orden
    success_url = reverse_lazy('orden-list')

def register(request):
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # return redirect(reverse_lazy('home'))
            return redirect(home)
    else:
        form = forms.RegisterForm()
    return render(request, "registration/register.html", {"form":form})

def changepass(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Contraseña cambiada satisfactoriamente.')
            # return redirect(reverse_lazy('home'))
            return redirect('changepass')
        else:
            messages.error(request, 'Atienda los errors indicados.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})
