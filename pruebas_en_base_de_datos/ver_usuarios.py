

from base_datos.configuracion import Session
from base_datos.usuario_tabla import UsuarioTabla

with Session() as sesion:
    usuarios = sesion.query(UsuarioTabla).all()
    for u in usuarios:
        print(u.id, u.nombre, u.email)
