from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base_datos.usuario_tabla import Base, UsuarioTabla
from base_datos import solicitud_acciones
from amistad_acciones import enviarSolicitud, aceptarSolicitud


def test_guardar_y_aceptar(monkeypatch):
    engine=create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    SessionPrueba=sessionmaker(bind=engine)

    monkeypatch.setattr(solicitud_acciones,"Session",SessionPrueba)

    with SessionPrueba() as sesion:
        sesion.add_all([
            UsuarioTabla(
                id=1,email="ana@example.com",
                password="prueba",nombre="Ana"
            ),
            UsuarioTabla(
                id=2,email="luz@example.com",
                password="prueba",nombre="Luz"
            )
        ])
        sesion.commit()

    enviarSolicitud(1,2)

    filas=solicitud_acciones.obtenerTodas()
    assert len(filas)==1
    assert filas[0].estado=="Pendiente"
    assert enviarSolicitud(1,2) is None
    assert enviarSolicitud(2,1) is None
    assert len(solicitud_acciones.obtenerTodas())==1

    solicitudID=filas[0].id

    assert aceptarSolicitud(solicitudID,1) is False
    assert aceptarSolicitud(solicitudID,2) is True

    guardada=solicitud_acciones.obtenerPorID(solicitudID)
    assert guardada.estado=="Aceptada"
    assert enviarSolicitud(1,2) is None
    assert enviarSolicitud(2,1) is None
    assert len(solicitud_acciones.obtenerTodas())==1

    engine.dispose()