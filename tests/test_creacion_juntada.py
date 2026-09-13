from app.juntada.juntada import Juntada
import pytest


def test_creacion_correcta_de_juntada():
    datos = Juntada(2, "15/09/2026", "Juntada de Estudio", "18:00", "21:00", [1, 3, 5])
    resultado = datos.registrar_juntada()

    assert resultado == {
        "organizador": 2,
        "titulo_juntada": "Juntada de Estudio",
        "fecha": "2026-09-15",
        "hora_inicio": "18:00:00",
        "hora_fin": "21:00:00",
        "amigos_invitados": [1, 3, 5],
    }


def test_datos_hora_inicio_mayor_a_hora_fin_es_invalido():
    with pytest.raises(ValueError) as error:
        Juntada(2, "15/09/2026", "Juntada", "18:00", "17:00", [1, 3, 5])
    assert str(error.value) == "La hora de inicio no puede ser posterior a la hora de finalizacion"


def test_formato_fecha_invalido():
    with pytest.raises(ValueError) as error:
        Juntada(2, "15-09-2026", "Juntada", "18:00", "21:00", [1, 3, 5])
    assert str(error.value) == "Formato de fecha inválido: '15-09-2026' (se espera DD/MM/AAAA)"


def test_formato_horario_invalido():
    with pytest.raises(ValueError) as error:
        Juntada(2, "15/09/2026", "Juntada", "18", "21:00", [1, 3, 5])
    assert str(error.value) == "Formato de hora de inicio inválido: '18' (se espera HH:MM)"


def test_titulo_vacio_es_invalido():
    with pytest.raises(ValueError) as error:
        Juntada(2, "15/09/2026", "", "18:00", "21:00", [1, 3, 5])
    assert str(error.value) == "El campo titulo no puede estar vacío"


def test_organizador_vacio_es_invalido():
    with pytest.raises(ValueError) as error:
        Juntada(None, "15/09/2026", "Juntada", "18:00", "21:00", [1, 3, 5])
    assert str(error.value) == "El campo responsable no puede estar vacío"


def test_amigos_invitados_vacio_es_invalido():
    with pytest.raises(ValueError) as error:
        Juntada(2, "15/09/2026", "Juntada", "18:00", "21:00", [])
    assert str(error.value) == "La juntada debe tener al menos un invitado"


def test_organizador_no_puede_invitarse_a_si_mismo():
    with pytest.raises(ValueError) as error:
        Juntada(3, "15/09/2026", "Juntada", "18:00", "21:00", [1, 3, 5])
    assert str(error.value) == "El organizador no puede invitarse a si mismo"