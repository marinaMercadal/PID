from dominio.modulo_utilidades.parseo_hora_fecha import parsear_fecha, parsear_hora
from dominio.modulo_utilidades.validador_de_tipo_evento import ValidadorDetipoEvento


class Juntada:
    def __init__(self, organizador, fecha, titulo_juntada, hora_inicio, hora_fin, amigos_invitados):
        self.organizador = organizador
        self.fecha = parsear_fecha(fecha)
        self.hora_inicio = parsear_hora(hora_inicio, "hora de inicio")
        self.hora_fin = parsear_hora(hora_fin, "hora de finalizacion")
        self.titulo_juntada = titulo_juntada
        self.amigos_invitados = amigos_invitados

        self.validar_juntada()
        self.validar_amigos_invitados()

    def validar_juntada(self):
        ValidadorDetipoEvento().validar(
            fecha=self.fecha,
            hora_inicio=self.hora_inicio,
            hora_fin=self.hora_fin,
            titulo=self.titulo_juntada,
            responsable=self.organizador,
        )

    def validar_amigos_invitados(self):
        if not self.amigos_invitados:
            raise ValueError("La juntada debe tener al menos un invitado")

        if self.organizador in self.amigos_invitados:
            raise ValueError("El organizador no puede invitarse a si mismo")

    def registrar_juntada(self):
        return {
            "organizador": self.organizador,
            "titulo_juntada": self.titulo_juntada,
            "fecha": self.fecha.isoformat(),
            "hora_inicio": self.hora_inicio.isoformat(),
            "hora_fin": self.hora_fin.isoformat(),
            "amigos_invitados": self.amigos_invitados,
        }
