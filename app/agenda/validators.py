from datetime import datetime


class BloqueAgendaInvalido(Exception):
    pass


class BloqueAgendaValidator:
    CAMPOS_REQUERIDOS = ["titulo", "fecha", "hora_inicio", "hora_fin"]

    def __init__(self, data: dict):
        self.data = data

    def validar(self) -> dict:
        self._validar_campos_presentes()
        fecha = self._parsear_fecha()
        hora_inicio, hora_fin = self._parsear_horas()
        self._validar_orden_horario(hora_inicio, hora_fin)

        return {
            "titulo": self.data["titulo"],
            "fecha": fecha,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin,
        }

    def _validar_campos_presentes(self):
        for campo in self.CAMPOS_REQUERIDOS:
            if not self.data.get(campo):
                raise BloqueAgendaInvalido(f"Falta el campo '{campo}'")

    def _parsear_fecha(self):
        try:
            return datetime.strptime(self.data["fecha"], "%Y-%m-%d").date()
        except ValueError:
            raise BloqueAgendaInvalido("Formato de fecha inválido (esperado YYYY-MM-DD)")

    def _parsear_horas(self):
        try:
            hora_inicio = datetime.strptime(self.data["hora_inicio"], "%H:%M").time()
            hora_fin = datetime.strptime(self.data["hora_fin"], "%H:%M").time()
            return hora_inicio, hora_fin
        except ValueError:
            raise BloqueAgendaInvalido("Formato de hora inválido (esperado HH:MM)")

    def _validar_orden_horario(self, hora_inicio, hora_fin):
        if hora_fin <= hora_inicio:
            raise BloqueAgendaInvalido("La hora de fin debe ser posterior a la de inicio")