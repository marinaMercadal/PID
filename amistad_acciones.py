from amistad import GestorAmistades
from base_datos.solicitud_acciones import obtenerTodas, guardar, actualizarEstado


def enviarSolicitud(emisorID,receptorID):
    solicitudes=obtenerTodas()
    gestor=GestorAmistades(solicitudes)

    solicitud=gestor.enviarSolicitud(emisorID,receptorID)

    if solicitud is not None:
        guardar(solicitud)

    return solicitud

def aceptarSolicitud(solicitudID,usuarioID):
    return actualizarEstado(solicitudID,usuarioID,"Aceptada")


def rechazarSolicitud(solicitudID,usuarioID):
    return actualizarEstado(solicitudID,usuarioID,"Rechazada")