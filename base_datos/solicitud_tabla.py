from sqlalchemy import Column, Integer, String, ForeignKey
from base_datos.usuario_tabla import Base


class SolicitudTabla(Base):
    __tablename__="solicitudes"

    id=Column(Integer,primary_key=True)
    emisorID=Column(Integer,ForeignKey("usuarios.id"),nullable=False)
    receptorID=Column(Integer,ForeignKey("usuarios.id"),nullable=False)
    estado=Column(String(20),nullable=False,default="Pendiente")