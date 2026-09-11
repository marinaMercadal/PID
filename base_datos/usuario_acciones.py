from sqlalchemy import select
from base_datos.configuracion import Session
from base_datos.usuario_tabla import UsuarioTabla


def guardar(usuario):
    sesion = Session()
    usuario_tabla = UsuarioTabla(
        email=usuario.email,
        password=usuario.password,
        nombre=usuario.nombre,
    )
    sesion.add(usuario_tabla)
    sesion.commit()
    sesion.close()

def buscarPorNombre(nombre):
    nombre=nombre.strip()
    if not nombre:
        return []
    with Session() as sesion:
        consulta=select(UsuarioTabla).where(
            UsuarioTabla.nombre.contains(nombre,autoescape=True)
        )
        return sesion.scalars(consulta).all()

    