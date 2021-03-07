from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django_select2 import forms as s2forms
from tempus_dominus.widgets import DateTimePicker,  DatePicker #, TimePicker,
from lab.models import Orden, Paciente

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
                "fecha_alta": DateTimePicker(options={'locale':'es','sideBySide':True,'format':'DD/MM/YYYY HH:mm', 'buttons':{'showToday': True,'showClose': True}})
        }

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = "__all__"
        widgets = {
                "fecha_nac": DatePicker(options={'locale':'es','sideBySide':True,'format':'DD/MM/YYYY', 'buttons':{'showToday': True,'showClose': True}})#,'showClear': True
        }
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
