from app.extensions import db
from app.models.agenda_bloque import BloqueAgenda


class BloqueAgendaRepository:
    def crear(self, usuario_id: int, datos_validados: dict) -> BloqueAgenda:
        bloque = BloqueAgenda(usuario_id=usuario_id, **datos_validados)
        db.session.add(bloque)
        db.session.commit()
        return bloque

    def obtener_por_id(self, bloque_id: int) -> BloqueAgenda | None:
        return BloqueAgenda.query.get(bloque_id)

    def listar_por_usuario(self, usuario_id: int | None = None) -> list[BloqueAgenda]:
        query = BloqueAgenda.query
        if usuario_id is not None:
            query = query.filter_by(usuario_id=usuario_id)
        return query.all()

    def eliminar(self, bloque: BloqueAgenda) -> None:
        db.session.delete(bloque)
        db.session.commit()