from base_datos.configuracion import engine
from base_datos.usuario_tabla import Base
from base_datos.solicitud_tabla import SolicitudTabla

Base.metadata.create_all(engine)
print("tablas creadas!")