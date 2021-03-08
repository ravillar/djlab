from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm,  UserCreationForm
from django.contrib.auth.models import User

from django_select2 import forms as s2forms
from tempus_dominus.widgets import DateTimePicker,  DatePicker #, TimePicker,
from lab.models import Orden, Paciente
dtpIcons= {
        'today': 'fas fa-calendar-check',
        'clear': 'fas fa-trash',
        'close': 'fas fa-times'
        }
dtpTooltips= {
        'today': 'Hoy',
        'clear': 'Limpiar selección',
        'close': 'Cerrar',
        'selectMonth': 'Seleccionar mes',
        'prevMonth': 'Mes anterior',
        'nextMonth': 'Mes siguiente',
        'selectYear': 'Seleccionar año',
        'prevYear': 'Año anterior',
        'nextYear': 'Año siguiente',
        'selectDecade': 'Seleccionar década',
        'prevDecade': 'Década anterior',
        'nextDecade': 'Década siguiente',
        'prevCentury': 'Siglo anterior',
        'nextCentury': 'Siglo siguiente',
        'incrementHour': 'Incrementar hora',
        'pickHour': 'Seleccionar hora',
        'decrementHour':'Decrementar hora',
        'incrementMinute': 'Incrementar minuto',
        'pickMinute': 'Seleccionar ninuto',
        'decrementMinute':'Decrementar minuto',
        'incrementSecond': 'Incrementar segundo',
        'pickSecond': 'Seleccionar segundo',
        'decrementSecond':'Decrementar segundo'

        }
class PruebasWidget(s2forms.Select2MultipleWidget):
    search_fields = [
        "nombre__icontains",
    ]

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = "__all__"
        # readonly_fields = ["fecha_alta"]
        widgets = {
                "pruebas": PruebasWidget(),
                "fecha_alta": DateTimePicker(options={'tooltips': dtpTooltips, 'icons':dtpIcons,'locale':'es','sideBySide':True,'format':'DD/MM/YYYY HH:mm', 'buttons':{'showToday': True,'showClose': True}})
        }

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = "__all__"
        widgets = {
                "fecha_nac": DatePicker(options={'tooltips': dtpTooltips, 'icons':dtpIcons, 'locale':'es','sideBySide':True,'format':'DD/MM/YYYY', 'buttons':{'showToday': True,'showClose': True}})#,'showClear': True
        }
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class ChangepassForm(PasswordChangeForm):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['aux'] ={'url':reverse_lazy('home'), 'icon':'fas fa-file-medical-alt', 'titulo':'Resultados', 'singular':'', 'descrip':'Publicación de los resultados'}
        return context
