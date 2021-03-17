from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from lab.models import Unidad, Prueba, Paciente, Orden, Resultado
from django.db.models import Q, Count
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
from . import forms
import json
from rolepermissions.mixins import HasRoleMixin
from django.core.paginator import Paginator

from django.contrib.auth.forms import PasswordChangeForm
from lab.util import AUX_CTX,PAG_CANT_FILAS, calculateAge

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
    def get(self, request) :
        cant_pac = Paciente.objects.all().count()
        cant_res = Resultado.objects.all().count()
        cant_ord = Orden.objects.all().count()
        grafico ={'labels':[], 'data':[]}
        datos = Orden.objects.values('fecha_alta').annotate(cantidad=Count('pruebas')).order_by('fecha_alta')#[:15]
        for dia in datos:
            grafico['labels'].append(dia['fecha_alta'].strftime("%d/%m/%Y"))
            grafico['data'].append(dia['cantidad'])
        ctx = {'obj' : {'pac':cant_pac, 'res':cant_res, 'ord':cant_ord, 'grafico':grafico}, 'aux':AUX_CTX['home']}
        return render(request, self.template_name, ctx)

class UnidAux():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aux'] = AUX_CTX['unidad']
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
            try:
                valInt=int(strval)
            except:
                valInt=None
            if valInt != None:
                query.add(Q(id=valInt), Q.OR)
            objects = Unidad.objects.filter(query).select_related().order_by('id')#[:10]
        else :
            objects = Unidad.objects.all().order_by('pk')#[:10]
        paginator = Paginator(objects, PAG_CANT_FILAS)
        objects = paginator.get_page(pag_nro)
        pags = list(range(1,objects.paginator.num_pages+1 ))
        f = '&filtrar='+strval if strval else '' #GET query param
        ctx = {'object_list' : objects, 'filtrar': strval, 'aux':AUX_CTX['unidad'],'pags':pags, 'f':f}
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
        context['aux'] = AUX_CTX['prueba']
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
            try:
                valInt=int(strval)
            except:
                valInt=None
            if valInt != None:
                query.add(Q(id=valInt), Q.OR)
            objects = Prueba.objects.filter(query).select_related().order_by('id')
        else :
            objects = Prueba.objects.all().order_by('pk')
        paginator = Paginator(objects, PAG_CANT_FILAS)
        objects = paginator.get_page(pag_nro)
        pags = list(range(1,objects.paginator.num_pages+1 ))
        f = '&filtrar='+strval if strval else '' #GET query param
        ctx = {'object_list' : objects, 'filtrar': strval, 'aux':AUX_CTX['prueba'],'pags':pags, 'f':f}
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
        context['aux'] = AUX_CTX['paciente']
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
            try:
                valInt=int(strval)
            except:
                valInt=None
            if valInt != None:
                query.add(Q(id=valInt), Q.OR)
            objects = Paciente.objects.filter(query).select_related().order_by('id')
        else :
            objects = Paciente.objects.all().order_by('pk')
        paginator = Paginator(objects, PAG_CANT_FILAS)
        objects = paginator.get_page(pag_nro)
        pags = list(range(1,objects.paginator.num_pages+1 ))
        f = '&filtrar='+strval if strval else '' #GET query param
        ctx = {'object_list' : objects, 'filtrar': strval, 'aux':AUX_CTX['paciente'],'pags':pags, 'f':f}
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
        context['aux'] = AUX_CTX['orden']
        return context
class OrdenResuListView(View):
    template_name = "lab/orden_list.html"
    def get(self, request, tipo, aux) :
        strval =  request.GET.get("filtrar", False)
        pag_nro = request.GET.get('pag')
        if strval :
            query = Q(paciente__nombre__icontains=strval)
            query.add(Q(paciente__apellido__icontains=strval), Q.OR)
            try:
                valInt=int(strval)
            except:
                valInt=None
            if valInt != None:
                query.add(Q(id=valInt), Q.OR)
            objects = Orden.objects.filter(query).select_related().order_by('-fecha_alta')
        else :
            objects = Orden.objects.all().order_by('-fecha_alta')
        paginator = Paginator(objects, PAG_CANT_FILAS)
        objects = paginator.get_page(pag_nro)
        pags = list(range(1,objects.paginator.num_pages+1 ))
        f = '&filtrar='+strval if strval else '' #GET query param

        ctx = {'object_list' : objects, 'filtrar': strval, 'aux':aux,'pags':pags, 'f':f, 'tipo':tipo}
        return render(request, self.template_name, ctx)

class OrdenListView(RecepcionRequired, OrdenResuListView, View):
    def get(self, request) :
        return super().get(request, 'O', AUX_CTX['orden'])
class OrdenCreate(OrdAux, RecepcionRequired,CreateView):
    model = Orden
    form_class = forms.OrdenForm
    success_url = reverse_lazy('orden-list')

class OrdenUpdate(OrdAux, RecepcionRequired,UpdateView):
    model = Orden
    form_class = forms.OrdenForm
    success_url = reverse_lazy('orden-list')

class OrdenDelete(OrdAux, RecepcionRequired,DeleteView):
    model = Orden
    success_url = reverse_lazy('orden-list')

class CargaView(LaboratorioRequired, OrdenResuListView, View):
    def get(self, request) :
        return super().get(request, 'C', AUX_CTX['carga'])
class ResultadoView(LoginRequired, OrdenResuListView, View):
    def get(self, request) :
        return super().get(request, 'R', AUX_CTX['resultado'])


class ResultadoDetalleView(LoginRequired, TemplateView):
    template_name = "layout-resultado.html"
    def get(self, request, pk, aux=None) :
        orden = get_object_or_404(Orden, id=pk)
        paciente=Paciente.objects.get(id=orden.paciente.id)
        res=Resultado.objects.filter(orden_id=pk)

        edad=str(calculateAge(paciente.fecha_nac))+' años'
        if aux==None:
            aux = AUX_CTX['resultado']

        ctx = { 'aux':aux, 'orden':orden, 'paciente':paciente, 'res':res, 'edad':edad}
        return render(request, self.template_name, ctx)


class CargaResultadoView(LaboratorioRequired, ResultadoDetalleView):
    template_name = "lab/carga_resultado.html"
    success_url = reverse_lazy('carga')
    def get(self, request, pk) :
        return super().get(request, pk, AUX_CTX['carga'])

    def post(self, request, pk) :

        obj = json.loads(request.POST.get('valores'))
        # print(obj)
        for k,v in obj.items():
            # print('{}:{}'.format(k, v))
            Resultado.objects.filter(pk=k).update(valor=v)
        # return redirect(reverse_lazy('carga')+'/'+str(pk))
        # return redirect(request.path)
        return redirect(self.success_url)

def register(request):
    if request.method == "POST":
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
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
            return redirect(reverse_lazy('changepass')+'?next='+request.POST['next']+'&success=1')
        else:
            messages.error(request, 'Atienda los errores indicados.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {'form': form, 'aux':AUX_CTX['changepass']})




