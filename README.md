# Sistema Lab
Proyecto de sistema para las tareas administrativas de un laboratorio de análisis clínicos.
Ver online https://ravillar.pythonanywhere.com
### Roles de usuarios
    python manage.py sync_roles
Hace que los roles y permisos definidos en ``roles.py`` sean accesibles inmediatamente a través del administrador de usuarios de django.
Documentación https://django-role-permissions.readthedocs.io/en/stable/admin.html#management-commands
### Datos en .csv
    python manage.py runscript cargar_csv
Este script carga datos ficticios para pruebas. 
