#Solo a modo de prueba- para obtener los valores: id, nombre, email que ya estan cargados en la tabla usuario (UusarioTabla)
#Necesitan tener el archivo credenciales.py 

from base_datos.configuracion import Session
from base_datos.usuario_tabla import UsuarioTabla

with Session() as sesion:
    usuarios = sesion.query(UsuarioTabla).all()
    for u in usuarios:
        print(u.id, u.nombre, u.email)