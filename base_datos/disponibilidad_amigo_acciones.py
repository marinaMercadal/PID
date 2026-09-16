from sqlalchemy import select
from base_datos.configuracion import Session
from base_datos.agenda_tabla import AgendaTabla
from base_datos.juntada_tabla import JuntadaTabla
from base_datos.juntada_invitados_tabla import JuntadaInvitadosTabla
from base_datos.solicitud_acciones import obtener_amigos_de_usuario


def obtener_disponibilidad(usuario_solicitante_id, amigo_id, fecha):
    amigos_ids = obtener_amigos_de_usuario(usuario_solicitante_id)
    if amigo_id not in amigos_ids:
        raise ValueError("Solo puedes ver la disponibilidad de tus amigos")  

    with Session() as sesion:
        ocupados = []

        consulta_agenda = select(AgendaTabla).where(
            AgendaTabla.usuario_id == amigo_id,
            AgendaTabla.fecha == fecha
        )
        for bloque in sesion.scalars(consulta_agenda).all():
            ocupados.append({"hora_inicio": bloque.hora_inicio, "hora_fin": bloque.hora_fin})

      
        consulta_juntada_amigo_organizador =select(JuntadaTabla).where(
            JuntadaTabla.organizador_id==amigo_id,
            JuntadaTabla.fecha==fecha
        )
        for bloque in sesion.scalars(consulta_juntada_amigo_organizador).all():
            ocupados.append({"hora_inicio": bloque.hora_inicio, "hora_fin": bloque.hora_fin})

        
        consulta_juntada_amigo_como_invitado = (
            select(JuntadaTabla)
            .join(JuntadaInvitadosTabla, JuntadaTabla.id==JuntadaInvitadosTabla.juntada_id).where(
            JuntadaInvitadosTabla.usuario_id==amigo_id,
            JuntadaInvitadosTabla.estado=="Si",
            JuntadaTabla.fecha==fecha
        ))

        for bloque in sesion.scalars(consulta_juntada_amigo_como_invitado).all():
                    ocupados.append({"hora_inicio": bloque.hora_inicio, "hora_fin": bloque.hora_fin})
        return ocupados