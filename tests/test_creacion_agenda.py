from app.agenda import Agenda
import pytest


def test_creacion_correcta_de_agenda():
    datos=Agenda("Martina","15/09/2026","Juntada","18:00","21:00")
    resultado=datos.registrar_agenda()
    
    assert resultado=={
        "usuario": "Martina",
        "titulo_reunion": "Juntada",
        "fecha": "2026-09-15",
        "hora_inicio": "18:00:00",
        "hora_fin": "21:00:00",
    }

def test_datos_hora_inicio_mayor_a_hora_fin_es_invalido():
    with pytest.raises(ValueError) as error:
        Agenda("Martina","15/09/2026","Juntada","18:00","17:00")
    assert str(error.value) == "La hora de inicio no puede ser posterior a la hora de finalizacion"
    
def test_formato_fecha_invalido():
    with pytest.raises(ValueError) as error:
        Agenda("Martina","15-09-2026","Juntada","18:00","17:00")
    assert str(error.value) == "Formato de fecha inválido: '15-09-2026' (se espera DD/MM/AAAA)"
    
def test_formato_horario_invalido():
    with pytest.raises(ValueError) as error:
        Agenda("Martina","15/09/2026","Juntada","18","17:00")
    assert str(error.value) == "Formato de hora de inicio inválido: '18' (se espera HH:MM)"
    
def test_titulo_vacio_es_invalido():
    with pytest.raises(ValueError) as error:
        Agenda("Martina", "15/09/2026", "", "18:00", "21:00")
    assert str(error.value) == "El campo titulo de la reunion no puede estar vacío"


def test_usuario_vacio_es_invalido():
    with pytest.raises(ValueError) as error:
        Agenda("", "15/09/2026", "Juntada", "18:00", "21:00")
    assert str(error.value) == "El campo usuario no puede estar vacío"