from datetime import datetime


def parsear_fecha(fecha):
    if not fecha:
        raise ValueError("El campo fecha no puede estar vacío")
    try:
        return datetime.strptime(fecha, "%d/%m/%Y").date()
    except ValueError:
        raise ValueError(f"Formato de fecha inválido: '{fecha}' (se espera DD/MM/AAAA)")


def parsear_hora(hora, tipo_de_horario):
    if not hora:
        raise ValueError(f"El campo {tipo_de_horario} no puede estar vacío")
    try:
        return datetime.strptime(hora, "%H:%M").time()
    except ValueError:
        raise ValueError(f"Formato de {tipo_de_horario} inválido: '{hora}' (se espera HH:MM)")