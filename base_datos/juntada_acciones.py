from sqlalchemy import select, update, delete, func, case
from base_datos.configuracion import Session
from base_datos.juntada_tabla import JuntadaTabla
from base_datos.juntada_invitados_tabla import JuntadaInvitadosTabla
from base_datos.usuario_tabla import UsuarioTabla


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

        if resultado.rowcount == 1 and nueva_respuesta == "No":
            _borrar_si_todos_rechazaron(sesion, juntada_id)

        sesion.commit()

        return resultado.rowcount == 1


def _borrar_si_todos_rechazaron(sesion, juntada_id):
    consulta = select(JuntadaInvitadosTabla.estado).where(JuntadaInvitadosTabla.juntada_id == juntada_id)
    estados = sesion.scalars(consulta).all()

    if estados and all(estado == "No" for estado in estados):
        sesion.execute(delete(JuntadaInvitadosTabla).where(JuntadaInvitadosTabla.juntada_id == juntada_id))
        sesion.execute(delete(JuntadaTabla).where(JuntadaTabla.id == juntada_id))


def obtener_organizadas_del_dia(usuario_id, fecha, fecha_fin=None):
    with Session() as sesion:
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


def obtener_invitados_organizador(usuario_id, fecha, fecha_fin=None):
    with Session() as sesion:
        consulta = (
            select(JuntadaInvitadosTabla.juntada_id, UsuarioTabla.nombre)
            .join(JuntadaTabla, JuntadaTabla.id == JuntadaInvitadosTabla.juntada_id)
            .join(UsuarioTabla, UsuarioTabla.id == JuntadaInvitadosTabla.usuario_id)
            .where(
                JuntadaTabla.organizador_id == usuario_id,
                JuntadaTabla.fecha.between(fecha, fecha_fin or fecha)
            )
            .order_by(UsuarioTabla.nombre)
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
