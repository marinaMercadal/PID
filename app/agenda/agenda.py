from app.modulo_utilidades.parseo_hora_fecha import parsear_fecha, parsear_hora
from app.modulo_utilidades.validador_de_tipo_evento import ValidadorDetipoEvento


class Agenda:
    def __init__(self, usuario, fecha, titulo_reunion, hora_inicio, hora_fin):
        self.usuario = usuario
        self.fecha = parsear_fecha(fecha)
        self.hora_inicio = parsear_hora(hora_inicio, "hora de inicio")
        self.hora_fin = parsear_hora(hora_fin, "hora de finalizacion")
        self.titulo_reunion = titulo_reunion
       
        
        self.validar_agenda()

    def validar_agenda(self):
        ValidadorDetipoEvento().validar(
            fecha=self.fecha,
            hora_inicio=self.hora_inicio,
            hora_fin=self.hora_fin,
            titulo=self.titulo_reunion,
            responsable=self.usuario,
    )

    def registrar_agenda(self):
        return {
            "usuario": self.usuario,
            "titulo_reunion": self.titulo_reunion,
            "fecha": self.fecha.isoformat(),
            "hora_inicio": self.hora_inicio.isoformat(),
            "hora_fin": self.hora_fin.isoformat(),
        }