from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
 
Base = declarative_base()
 
 
class UsuarioTabla(Base):
    __tablename__ = "usuarios"
 
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    nombre = Column(String(255), nullable=False)