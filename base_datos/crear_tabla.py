from base_datos.configuracion import engine
from base_datos.usuario_tabla import Base

Base.metadata.create_all(engine)
print("tablas creadas!")