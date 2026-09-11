from datetime import datetime
from app.validador_de_agenda import ValidadorDeAgenda 


class Agenda:
    def __init__(self,usuario,fecha, titulo_reunion,hora_inicio, hora_fin):
        self.usuario= usuario
        
        self.fecha = self._parsear_fecha(fecha)
        self.hora_inicio = self._parsear_hora(hora_inicio, "hora de inicio")
        self.hora_fin = self._parsear_hora(hora_fin, "hora de finalizacion")
        
        self.titulo_reunion = titulo_reunion
        
        self.validar_agenda()
        
    def _parsear_fecha(self, fecha):
        if not fecha:
            raise ValueError("El campo fecha no puede estar vacío")
        try:
            return datetime.strptime(fecha, "%d/%m/%Y").date()
        except ValueError:
            raise ValueError(f"Formato de fecha inválido: '{fecha}' (se espera DD/MM/AAAA)")

    def _parsear_hora(self, hora, tipo_de_horario):
        if not hora:
            raise ValueError(f"El campo {tipo_de_horario} no puede estar vacío")
        try:
            return datetime.strptime(hora, "%H:%M").time()
        except ValueError:
            raise ValueError(f"Formato de {tipo_de_horario} inválido: '{hora}' (se espera HH:MM)")


    def validar_agenda(self):
        ValidadorDeAgenda().validador(self)
        
        
    def registrar_agenda(self):
        return {
                    "usuario": self.usuario,
                    "titulo_reunion": self.titulo_reunion,
                    "fecha": self.fecha.isoformat(),
                    "hora_inicio": self.hora_inicio.isoformat(),
                    "hora_fin": self.hora_fin.isoformat(),
                }
        
