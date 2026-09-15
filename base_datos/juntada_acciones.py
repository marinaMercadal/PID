from sqlalchemy import select, update, func, case
from base_datos.configuracion import Session
from base_datos.juntada_tabla import JuntadaTabla
from base_datos.juntada_invitados_tabla import JuntadaInvitadosTabla


def guardar(juntada):
    with Session() as sesion:
        juntada_tabla = JuntadaTabla(
            organizador_id=juntada.organizador,
            titulo=juntada.titulo_juntada,
            fecha=juntada.fecha,
            hora_inicio=juntada.hora_inicio,
            hora_fin=juntada.hora_fin,
        )
        sesion.add(juntada_tabla)
        sesion.flush()

        for usuario_id in juntada.amigos_invitados:
            invitado = JuntadaInvitadosTabla(
                juntada_id=juntada_tabla.id,
                usuario_id=usuario_id,
                estado="Pendiente",
            )
            sesion.add(invitado)

        sesion.commit()

        return juntada_tabla.id

def obtener_por_id(juntada_id):
    with Session() as sesion:
        return sesion.get(JuntadaTabla, juntada_id)

def obtener_organizadas_por_usuario(usuario_id):
    with Session() as sesion:
        consulta = select(JuntadaTabla).where(
            JuntadaTabla.organizador_id == usuario_id
        )
        return sesion.scalars(consulta).all()

def obtener_invitaciones_de_usuario(usuario_id):
    with Session() as sesion:
        consulta = select(JuntadaInvitadosTabla).where(
            JuntadaInvitadosTabla.usuario_id == usuario_id
        )
        return sesion.scalars(consulta).all()

def obtener_invitados_de_juntada(juntada_id):
    with Session() as sesion:
        consulta = select(JuntadaInvitadosTabla).where(
            JuntadaInvitadosTabla.juntada_id == juntada_id
        )
        return sesion.scalars(consulta).all()

def responder_invitacion(juntada_id, usuario_id, nueva_respuesta):
    if nueva_respuesta not in ("Si", "No", "Tal vez"):
        return False

    with Session() as sesion:
        consulta = (
            update(JuntadaInvitadosTabla)
            .where(
                (JuntadaInvitadosTabla.juntada_id == juntada_id) &
                (JuntadaInvitadosTabla.usuario_id == usuario_id) &
                (JuntadaInvitadosTabla.estado.in_(["Tal vez","Pendiente"]))
            )
            .values(estado=nueva_respuesta)
        )

        resultado = sesion.execute(consulta)
        sesion.commit()

        return resultado.rowcount == 1


def obtener_organizadas_del_dia(usuario_id, fecha, fecha_fin=None):
    with Session() as sesion:
        # Contamos todos los invitados juntos, sin una consulta por juntada.
        resumen=(
            select(
                JuntadaInvitadosTabla.juntada_id,
                func.count().label("total"),
                func.sum(case((JuntadaInvitadosTabla.estado=="Si",1),else_=0)).label("confirmados")
            )
            .join(JuntadaTabla,JuntadaTabla.id==JuntadaInvitadosTabla.juntada_id)
            .where(JuntadaTabla.organizador_id==usuario_id,JuntadaTabla.fecha.between(fecha,fecha_fin or fecha))
            .group_by(JuntadaInvitadosTabla.juntada_id)
            .subquery()
        )
        consulta=(
            select(JuntadaTabla,func.coalesce(resumen.c.confirmados,0),func.coalesce(resumen.c.total,0))
            .outerjoin(resumen,resumen.c.juntada_id==JuntadaTabla.id)
            .where(JuntadaTabla.organizador_id==usuario_id,JuntadaTabla.fecha.between(fecha,fecha_fin or fecha))
        )
        return sesion.execute(consulta).all()


def obtener_invitaciones_del_calendario(usuario_id, fecha, fecha_fin=None):
    with Session() as sesion:
        consulta=(
            select(JuntadaInvitadosTabla,JuntadaTabla)
            .join(JuntadaTabla,JuntadaTabla.id==JuntadaInvitadosTabla.juntada_id)
            .where(
                JuntadaInvitadosTabla.usuario_id==usuario_id,
                JuntadaInvitadosTabla.estado!="No",
                (JuntadaTabla.fecha.between(fecha,fecha_fin or fecha)) |
                JuntadaInvitadosTabla.estado.in_(["Pendiente","Tal vez"])
            )
        )
        return sesion.execute(consulta).all()
