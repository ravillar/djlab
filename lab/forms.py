from django import forms
from django.contrib.auth.forms import AuthenticationForm,  UserCreationForm
from django.contrib.auth.models import User

from django_select2 import forms as s2forms
from tempus_dominus.widgets import DateTimePicker,  DatePicker #, TimePicker,
from lab.models import Orden, Paciente
from lab.util import DTP_ICONS, DTP_TOOLTIPS
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, Button
from django.urls import reverse

class PruebasWidget(s2forms.Select2MultipleWidget):
    search_fields = [
        "nombre__icontains",
    ]
class PacienteWidget(s2forms.Select2Widget):
    search_fields = [
        "paciente__icontains",
    ]

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = "__all__"
        # readonly_fields = ["fecha_alta"]
        widgets = {
                "pruebas": PruebasWidget(),
                "paciente": PacienteWidget(),
                "fecha_alta": DateTimePicker(options={'tooltips': DTP_TOOLTIPS, 'icons':DTP_ICONS,'locale':'es','sideBySide':True,'format':'DD/MM/YYYY HH:mm', 'buttons':{'showToday': True,'showClose': True}})
        }

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = "__all__"
        widgets = {
                "fecha_nac": DatePicker(options={'tooltips': DTP_TOOLTIPS, 'icons':DTP_ICONS, 'locale':'es','sideBySide':True,'format':'DD/MM/YYYY', 'buttons':{'showToday': True,'showClose': True}})#,'showClear': True
                , 'direccion':forms.Textarea(attrs={'rows': '3'})
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('dni', css_class='form-group col-md-4 mb-0'),
                Column('apellido', css_class='form-group col-md-4 mb-0'),
                Column('nombre', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('fecha_nac', css_class='form-group col-md-4 mb-0'),
                Column('email', css_class='form-group col-md-4 mb-0'),
                Column('telefono', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column(
                    'direccion', css_class='form-group mb-0'),
                css_class='form-row'
            ),
            Div(
                Button('button','Cancelar', css_class='btn btn-secondary',  onclick="location.href='"+reverse('paciente-list')+"'"),
                Submit('submit', 'Guardar'), css_class='modal-footer')
            )
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


