from sqlalchemy import select, update, case
from base_datos.configuracion import Session
from base_datos.solicitud_tabla import SolicitudTabla
from base_datos.usuario_tabla import UsuarioTabla


def guardar(solicitud):
    with Session() as sesion:
        fila=SolicitudTabla(
            emisorID=solicitud.emisorID,
            receptorID=solicitud.receptorID,
            estado=solicitud.estado
        )
        sesion.add(fila)
        sesion.commit()

def obtenerTodas():
    with Session() as sesion:
        consulta=select(SolicitudTabla)
        solicitudes=sesion.scalars(consulta).all()
        return solicitudes

def obtenerPorID(solicitudID):
    with Session() as sesion:
        solicitud=sesion.get(SolicitudTabla,solicitudID)
        return solicitud

def actualizarEstado(solicitudID,usuarioID,nuevoEstado):
    if nuevoEstado not in ("Aceptada","Rechazada"):
        return False

    with Session() as sesion:
        consulta=(
            update(SolicitudTabla)
            .where(
                SolicitudTabla.id==solicitudID,
                SolicitudTabla.receptorID==usuarioID,
                SolicitudTabla.estado=="Pendiente"
            )
            .values(estado=nuevoEstado)
        )

        resultado=sesion.execute(consulta)
        sesion.commit()

        return resultado.rowcount==1
    
def obtenerRecibidas(usuarioID):
    with Session() as sesion:
        consulta=select(SolicitudTabla).join(UsuarioTabla,UsuarioTabla.id==SolicitudTabla.emisorID).where(
            UsuarioTabla.activo.is_(True),
            SolicitudTabla.receptorID==usuarioID,
            SolicitudTabla.estado=="Pendiente"
        )
        return sesion.scalars(consulta).all()

def obtener_amigos_de_usuario(usuarioID):
    with Session() as sesion:
        consulta=select(SolicitudTabla).join(UsuarioTabla,UsuarioTabla.id==case(
            (SolicitudTabla.emisorID==usuarioID,SolicitudTabla.receptorID),
            else_=SolicitudTabla.emisorID
        )).where(
            UsuarioTabla.activo.is_(True),
            SolicitudTabla.estado=="Aceptada",
            (SolicitudTabla.emisorID==usuarioID) | (SolicitudTabla.receptorID==usuarioID)
        )
        solicitudes=sesion.scalars(consulta).all()

    return [
        solicitud.receptorID if solicitud.emisorID==usuarioID else solicitud.emisorID
        for solicitud in solicitudes
    ]