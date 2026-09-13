from sqlalchemy import select
from base_datos.configuracion import Session
from base_datos.usuario_tabla import UsuarioTabla
from dominio.usuario import Usuario

def guardar(usuario):
    if buscar_por_email(usuario.email) is not None:
        raise ValueError("Ya existe una cuenta registrada con ese email")
    
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

def buscar_por_email(email):
    sesion = Session()
    usuario_tabla = sesion.query(UsuarioTabla).filter_by(email=email).first()
    sesion.close()
    return usuario_tabla


def verificar_login(email, password):
    usuario_tabla = buscar_por_email(email)
    if usuario_tabla is None:
        return None
    if not Usuario.verificar_password(password, usuario_tabla.password):
        return None
    return usuario_tabla