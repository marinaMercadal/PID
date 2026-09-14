from sqlalchemy import select
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


def obtener_invitaciones_de_usuario(usuario_id):
    with Session() as sesion:
        consulta = select(JuntadaInvitadosTabla).where(
            JuntadaInvitadosTabla.usuario_id == usuario_id
        )
        return sesion.scalars(consulta).all()