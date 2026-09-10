from app.agenda.repository import BloqueAgendaRepository
from app.agenda.validators import BloqueAgendaValidator


class AgendaService:
    def __init__(self, repository: BloqueAgendaRepository = None):
        self.repository = repository or BloqueAgendaRepository()

    def crear_bloque(self, usuario_id: int, data: dict) -> dict:
        validador = BloqueAgendaValidator(data)
        datos_validados = validador.validar()
        bloque = self.repository.crear(usuario_id, datos_validados)
        return bloque.to_dict()

    def listar_bloques(self, usuario_id: int | None = None) -> list[dict]:
        bloques = self.repository.listar_por_usuario(usuario_id)
        return [b.to_dict() for b in bloques]