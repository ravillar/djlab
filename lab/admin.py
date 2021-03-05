from django.contrib import admin

# Register your models here.
from .models import Unidad, Prueba, Paciente, Orden, Resultado

admin.site.register(Unidad)
admin.site.register(Prueba)
admin.site.register(Paciente)
# admin.site.register(Orden)
# admin.site.register(Resultado)

class ResultadoInline(admin.TabularInline):
    model = Orden.pruebas.through
    extra = 1
class OrdenAdmin(admin.ModelAdmin):
    inlines = (ResultadoInline, )
admin.site.register(Orden, OrdenAdmin)
