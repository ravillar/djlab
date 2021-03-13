import csv  # https://docs.python.org/3/library/csv.html

# https://django-extensions.readthedocs.io/en/latest/runscript.html

# python3 manage.py runscript cargar_csv

from lab.models import Unidad, Prueba, Paciente, Orden, Resultado


def run():
    fhand = open('datos.csv')
    reader = csv.reader(fhand)
    next(reader)  #Evitar la línea del encabezado

    Unidad.objects.all().delete()
    Prueba.objects.all().delete()
    Paciente.objects.all().delete()
    Orden.objects.all().delete()
    Resultado.objects.all().delete()

    # Formato
    # valor,min_val,max_val,prueba,dni,apellido,nombre,email,telefono,direccion,unidad,unidad_desc
    # 6,2,10,Eosinófilos Segmentados,4428971,Mathews,Stewart,euismod.est@ipsumPhasellus.ca,(119) 723-5233,1261 Ipsum Avenue,%,...
    for row in reader:
        print(row)

        unidad, created = Unidad.objects.get_or_create(sigla=row[10], descrip=row[11])
        paciente, created = Paciente.objects.get_or_create(dni=row[4], apellido=row[5], nombre=row[6], email=row[7], telefono=row[8], direccion=row[9], fecha_nac=row[13])
        prueba, created = Prueba.objects.get_or_create(minimo=row[1], maximo=row[2], nombre=row[3], unidad=unidad)
        orden, created = Orden.objects.get_or_create(fecha_alta=row[12], paciente=paciente)
        resultado, created = Resultado.objects.get_or_create(orden=orden, prueba=prueba, valor=row[0])

