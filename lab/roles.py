from rolepermissions.roles import AbstractUserRole

class Recepcion(AbstractUserRole):
    available_permissions = {
        'recepcion': True,
    }

class Laboratorio(AbstractUserRole):
    available_permissions = {
        'laboratorio': True,
}
