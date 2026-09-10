import pytest
from app.agenda.service import AgendaService
from app.agenda.validators import BloqueAgendaInvalido


class TestAgendaService:
    def test_crear_bloque_valido(self, app):
        with app.app_context():
            service = AgendaService()
            resultado = service.crear_bloque(1, {
                "titulo": "Reunión de equipo",
                "fecha": "2026-09-15",
                "hora_inicio": "10:00",
                "hora_fin": "11:00",
            })
            assert resultado["titulo"] == "Reunión de equipo"
            assert resultado["usuario_id"] == 1

    def test_crear_bloque_horario_invalido(self, app):
        with app.app_context():
            service = AgendaService()
            with pytest.raises(BloqueAgendaInvalido):
                service.crear_bloque(1, {
                    "titulo": "Bloque inválido",
                    "fecha": "2026-09-15",
                    "hora_inicio": "11:00",
                    "hora_fin": "10:00",
                })