from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from lab.models import Unidad, Prueba, Paciente, Orden
from django.db.models import Q
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
from . import forms

from rolepermissions.mixins import HasRoleMixin
from django.core.paginator import Paginator

aux_ctx = {
        'home':{'url':reverse_lazy('home'), 'icon':'fas fa-home', 'titulo':'Home', 'singular':'', 'descrip':'Bienvenido al Sistema Lab !!'},
        'unidad':{'url':reverse_lazy('unidad-list'), 'icon':'fas fa-ruler-combined', 'titulo':'Unidades', 'singular':'Unidad', 'descrip':'En las que se expresan las mediciones de las pruebas de laboratorio'},
        'prueba':{'url':reverse_lazy('prueba-list'), 'icon':'fas fa-microscope', 'titulo':'Pruebas', 'singular':'Prueba', 'descrip':'Prácticas de laboratorio'},
        'paciente':{'url':reverse_lazy('paciente-list'), 'icon':'fas fa-id-card', 'titulo':'Pacientes', 'singular':'Paciente', 'descrip':'Registro de personas a las que se le tomaron las muestras'},
        'orden':{'url':reverse_lazy('orden-list'), 'icon':'fas fa-file-medical', 'titulo':'Órdenes', 'singular':'Orden', 'descrip':'Estudios solicitados por profesionales médicos'},
        'resultado':{'url':reverse_lazy('home'), 'icon':'fas fa-file-medical-alt', 'titulo':'Resultados', 'singular':'', 'descrip':'Publicación de los resultados'},
        'carga':{'url':reverse_lazy('home'), 'icon':'fas fa-keyboard', 'titulo':'Carga de resultados', 'singular':'', 'descrip':'Carga de los resultados'},
}
pag_cant_filas=10

# para ser heredada por las clases de views genéricas que requieren autenticación
class LoginRequired(LoginRequiredMixin):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'

class RecepcionRequired(HasRoleMixin, LoginRequired):
    allowed_roles = 'recepcion'
class LaboratorioRequired(HasRoleMixin, LoginRequired):
    allowed_roles = 'laboratorio'

class HomePageView(LoginRequired, TemplateView):
    template_name = "lab/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aux'] = aux_ctx['home']
        return context
class ResultadoView(LoginRequired, TemplateView):
    template_name = "lab/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aux'] = aux_ctx['resultado']
        return context
class CargaView(LoginRequired, TemplateView):
    template_name = "lab/home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aux'] = aux_ctx['carga']
        return context

class UnidAux():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aux'] = aux_ctx['unidad']
        return context

class UnidadListView(LaboratorioRequired, View):
    template_name = "lab/unidad_list.html"

    def get(self, request) :
        strval =  request.GET.get("filtrar", False)
        pag_nro = request.GET.get('pag')
        if strval :
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(sigla__icontains=strval)
            query.add(Q(descrip__icontains=strval), Q.OR)
            objects = Unidad.objects.filter(query).select_related().order_by('id')#[:10]
        else :
            objects = Unidad.objects.all().order_by('pk')#[:10]
        paginator = Paginator(objects, pag_cant_filas)
        objects = paginator.get_page(pag_nro)
        pags = list(range(1,objects.paginator.num_pages+1 ))
        f = '&filtrar='+strval if strval else '' #GET query param
        ctx = {'object_list' : objects, 'filtrar': strval, 'aux':aux_ctx['unidad'],'pags':pags, 'f':f}
        return render(request, self.template_name, ctx)

class UnidadCreate(UnidAux, LaboratorioRequired,CreateView):
    model = Unidad
    fields = ['sigla', 'descrip']
    success_url = reverse_lazy('unidad-list')

class UnidadUpdate(UnidAux, LaboratorioRequired,UpdateView):
    model = Unidad
    fields = ['sigla', 'descrip']
    # template_name_suffix = '_update_form'
    success_url = reverse_lazy('unidad-list')

class UnidadDelete(UnidAux, LaboratorioRequired,DeleteView):
    model = Unidad
    success_url = reverse_lazy('unidad-list')
    # def post(self, request, *args, **kwargs):
    #     if "cancel" in request.POST:
    #         url = self.get_success_url()
    #         return HttpResponseRedirect(url)
    #     else:
    #         return super(UnidadDelete, self).post(request, *args, **kwargs)

class PrueAux():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aux'] = aux_ctx['prueba']
        return context

class PruebaListView(LaboratorioRequired, View):
    template_name = "lab/prueba_list.html"
    def get(self, request) :
        strval =  request.GET.get("filtrar", False)
        pag_nro = request.GET.get('pag')
        if strval :
            query = Q(nombre__icontains=strval)
            query.add(Q(unidad__sigla__icontains=strval), Q.OR)
            query.add(Q(unidad__descrip__icontains=strval), Q.OR)
            objects = Prueba.objects.filter(query).select_related().order_by('id')
        else :
            objects = Prueba.objects.all().order_by('pk')
        paginator = Paginator(objects, pag_cant_filas)
        objects = paginator.get_page(pag_nro)
        pags = list(range(1,objects.paginator.num_pages+1 ))
        f = '&filtrar='+strval if strval else '' #GET query param
        ctx = {'object_list' : objects, 'filtrar': strval, 'aux':aux_ctx['prueba'],'pags':pags, 'f':f}
        return render(request, self.template_name, ctx)
class PruebaCreate(PrueAux, LaboratorioRequired,CreateView):
    model = Prueba
    fields = '__all__' #['nombre', 'unidad', 'minimo', 'maximo']
    success_url = reverse_lazy('prueba-list')

class PruebaUpdate(PrueAux, LaboratorioRequired,UpdateView):
    model = Prueba
    fields = '__all__'
    # template_name_suffix = '_update_form'
    success_url = reverse_lazy('prueba-list')

class PruebaDelete(PrueAux, LaboratorioRequired,DeleteView):
    model = Prueba
    success_url = reverse_lazy('prueba-list')
class PacAux():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aux'] = aux_ctx['paciente']
        return context
class PacienteListView(RecepcionRequired, View):
    template_name = "lab/paciente_list.html"
    def get(self, request) :
        strval =  request.GET.get("filtrar", False)
        pag_nro = request.GET.get('pag')
        if strval :
            query = Q(nombre__icontains=strval)
            query.add(Q(apellido__icontains=strval), Q.OR)
            query.add(Q(email__icontains=strval), Q.OR)
            query.add(Q(telefono__icontains=strval), Q.OR)
            objects = Paciente.objects.filter(query).select_related().order_by('id')
        else :
            objects = Paciente.objects.all().order_by('pk')
        paginator = Paginator(objects, pag_cant_filas)
        objects = paginator.get_page(pag_nro)
        pags = list(range(1,objects.paginator.num_pages+1 ))
        f = '&filtrar='+strval if strval else '' #GET query param
        ctx = {'object_list' : objects, 'filtrar': strval, 'aux':aux_ctx['paciente'],'pags':pags, 'f':f}
        return render(request, self.template_name, ctx)
class PacienteCreate(PacAux, RecepcionRequired,CreateView):
    model = Paciente
    form_class = forms.PacienteForm
    # fields = '__all__'
    success_url = reverse_lazy('paciente-list')

class PacienteUpdate(PacAux, RecepcionRequired,UpdateView):
    model = Paciente
    form_class = forms.PacienteForm
    # fields = '__all__'
    success_url = reverse_lazy('paciente-list')

class PacienteDelete(PacAux, RecepcionRequired,DeleteView):
    model = Paciente
    success_url = reverse_lazy('paciente-list')

class OrdAux():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aux'] = aux_ctx['orden']
        return context
class OrdenListView(RecepcionRequired, View):
    template_name = "lab/orden_list.html"
    def get(self, request) :
        strval =  request.GET.get("filtrar", False)
        pag_nro = request.GET.get('pag')
        if strval :
            query = Q(paciente__nombre__icontains=strval)
            query.add(Q(paciente__apellido__icontains=strval), Q.OR)
            objects = Orden.objects.filter(query).select_related().order_by('-fecha_alta')
        else :
            objects = Orden.objects.all().order_by('-fecha_alta')
        paginator = Paginator(objects, pag_cant_filas)
        objects = paginator.get_page(pag_nro)
        pags = list(range(1,objects.paginator.num_pages+1 ))
        f = '&filtrar='+strval if strval else '' #GET query param
        ctx = {'object_list' : objects, 'filtrar': strval, 'aux':aux_ctx['orden'],'pags':pags, 'f':f}
        return render(request, self.template_name, ctx)

class OrdenCreate(OrdAux, RecepcionRequired,CreateView):
    model = Orden
    # fields = '__all__'
    form_class = forms.OrdenForm
    success_url = reverse_lazy('orden-list')

class OrdenUpdate(OrdAux, RecepcionRequired,UpdateView):
    model = Orden
    # fields = '__all__'
    form_class = forms.OrdenForm
    success_url = reverse_lazy('orden-list')

class OrdenDelete(OrdAux, RecepcionRequired,DeleteView):
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
            return redirect('home')
    else:
        form = forms.RegisterForm()
    return render(request, "registration/register.html", {"form":form})

def changepass(request):
    if request.method == 'POST':
        form = forms.ChangepassForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Contraseña cambiada satisfactoriamente.')
            # return redirect(reverse_lazy('home'))
            return redirect('changepass')
        else:
            messages.error(request, 'Atienda los errores indicados.')
    else:
        form = forms.ChangepassForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form})



