from base_datos.solicitud_acciones import obtener_amigos_de_usuario
from base_datos.usuario_acciones import buscarPorID

for usuario_id in range(1, 10):
    usuario = buscarPorID(usuario_id)
    if usuario is None:
        continue
    amigos_ids = obtener_amigos_de_usuario(usuario_id)
    nombres_amigos = [buscarPorID(a).nombre for a in amigos_ids if buscarPorID(a) is not None]
    print(f"{usuario_id} {usuario.nombre}: amigos = {amigos_ids} ({nombres_amigos})")