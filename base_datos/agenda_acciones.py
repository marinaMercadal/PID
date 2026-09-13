from sqlalchemy import select
from base_datos.configuracion import Session
from base_datos.agenda_tabla import AgendaTabla


def guardar(agenda):
    with Session() as sesion:
        agenda_tabla = AgendaTabla(
            usuario_id=agenda.usuario_id,
            titulo=agenda.titulo_reunion,
            fecha=agenda.fecha,
            hora_inicio=agenda.hora_inicio,
            hora_fin=agenda.hora_fin,
        )
        sesion.add(agenda_tabla)
        sesion.commit()
        
def obtener_por_usuario(usuario_id):
    with Session() as sesion:
        consulta = select(AgendaTabla).where(
            AgendaTabla.usuario_id == usuario_id
        )
        return sesion.scalars(consulta).all()