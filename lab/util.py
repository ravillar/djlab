from datetime import date
from django.urls import reverse_lazy

PAG_CANT_FILAS=10

AUX_CTX = {
        'home':{ 'icon':'fas fa-home', 'titulo':'Home', 'singular':'', 'descrip':'Bienvenido al Sistema Lab !!'},
        'unidad':{ 'icon':'fas fa-ruler-combined', 'titulo':'Unidades', 'singular':'Unidad', 'descrip':'En las que se expresan las mediciones de las pruebas de laboratorio'},
        'prueba':{ 'icon':'fas fa-microscope', 'titulo':'Pruebas', 'singular':'Prueba', 'descrip':'Prácticas de laboratorio'},
        'paciente':{ 'icon':'fas fa-id-card', 'titulo':'Pacientes', 'singular':'Paciente', 'descrip':'Registro de personas a las que se le tomaron las muestras'},
        'orden':{ 'icon':'fas fa-file-medical', 'titulo':'Órdenes', 'singular':'Orden', 'descrip':'Estudios solicitados por profesionales médicos'},
        'resultado':{ 'icon':'fas fa-file-medical-alt', 'titulo':'Resultados', 'singular':'', 'descrip':'Publicación de los resultados'},
        'carga':{ 'icon':'fas fa-keyboard', 'titulo':'Carga de resultados', 'singular':'', 'descrip':'Carga de los resultados'},
        'changepass':{ 'icon':'fas fa-key', 'titulo':'Cambio de contraseña', 'singular':'', 'descrip':''},
}

DTP_ICONS= {
        'today': 'fas fa-calendar-check',
        'clear': 'fas fa-trash',
        'close': 'fas fa-times'
        }

DTP_TOOLTIPS= {
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


def calculateAge(born):
    today = date.today()
    try:
        birthday = born.replace(year = today.year)

    # raised when birth date is February 29
    # and the current year is not a leap year
    except ValueError:
        birthday = born.replace(year = today.year,
                  month = born.month + 1, day = 1)

    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year

