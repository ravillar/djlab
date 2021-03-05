from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.
class Unidad(models.Model):
    sigla = models.CharField(max_length=10)
    descrip = models.CharField(max_length=100, verbose_name="Descripción")
    def __str__(self):
        return self.sigla + ' - ' + self.descrip
    class Meta:
        verbose_name_plural = "unidades"

class Paciente(models.Model):
    dni = models.IntegerField(unique=True)
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    fecha_nac = models.DateField(blank=False, null=False, verbose_name="Fecha de nacimiento")
    fecha_alta = models.DateField(auto_now_add=True, verbose_name="Fecha de ingreso")
    email = models.EmailField(default=None, blank=True, null=True)
    telefono = models.CharField(max_length=20, default=None, blank=True, null=True, verbose_name="Teléfono")
    direccion = models.TextField(default=None, blank=True, null=True,max_length=255, verbose_name="Dirección")
    def __str__(self):
        return str(self.dni) + ', ' + self.apellido + ', ' + self.nombre

class Prueba(models.Model):
    nombre = models.CharField(max_length=100)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE)
    minimo = models.FloatField(default=None, blank=True, null=True, verbose_name="Val. Ref. Mínimo")
    maximo = models.FloatField(default=None, blank=True, null=True, verbose_name="Val. Ref. Máximo")
    def __str__(self):
        return self.nombre + ' - ' + str(self.unidad)

class Orden(models.Model):
    fecha_alta = models.DateTimeField(verbose_name="Fecha", blank=True, null=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    # fecha_alta = models.DateTimeField(auto_now_add=True, verbose_name="Fecha")
    # fecha_pub = models.DatetimeField(auto_now=True)
    # pruebas = models.ManyToManyField(Prueba, related_name='pruebas')
    pruebas = models.ManyToManyField(Prueba, through='Resultado')
    # def save(self, *args, **kwargs):
    #     ''' On save, update timestamps '''
    #     if not self.id:
    #         self.fecha_alta = timezone.now()
    #     return super(Orden, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.paciente) + ' - ' + self.fecha_alta.strftime("%d/%m/%Y %H:%M") #str(self.fecha_alta)

    class Meta:
        verbose_name_plural = "órdenes"

class Resultado(models.Model):
    prueba = models.ForeignKey(Prueba, on_delete=models.CASCADE)
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    valor = models.FloatField(default=None, blank=True, null=True)
    class Meta:
        unique_together = [['prueba', 'orden']]

