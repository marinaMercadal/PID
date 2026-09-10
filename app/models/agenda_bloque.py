from app.extensions import db
from datetime import datetime, timezone


class BloqueAgenda(db.Model):
    __tablename__ = "bloques_agenda"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)
    creado_en = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "titulo": self.titulo,
            "fecha": self.fecha.isoformat(),
            "hora_inicio": self.hora_inicio.isoformat(),
            "hora_fin": self.hora_fin.isoformat(),
        }

    def __repr__(self) -> str:
        return f"<BloqueAgenda {self.id} '{self.titulo}' {self.fecha}>"