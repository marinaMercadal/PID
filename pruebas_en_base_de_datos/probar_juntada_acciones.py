# Solo a modo de prueba - para verificar su funcionamiento cambien el valor de los atributos.
# Necesitan tener el archivo credenciales.py
from app.juntada.juntada import Juntada
from base_datos.juntada_acciones import guardar, obtener_invitaciones_de_usuario

juntada = Juntada(
    organizador=1,
    fecha="20/09/2026",
    titulo_juntada="Prueba de guardado",
    hora_inicio="10:00",
    hora_fin="11:00",
    amigos_invitados=[2, 3],
)

guardar(juntada)
print("Juntada guardada!")

resultados = obtener_invitaciones_de_usuario(2)
for fila in resultados:
    print("id de invitacion:",fila.id, " id de juntada:",fila.juntada_id," id del invitado:",fila.usuario_id, "id del estado: ",fila.estado)