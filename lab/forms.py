from django import forms
from django_select2 import forms as s2forms

from lab.models import Orden

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
        }
