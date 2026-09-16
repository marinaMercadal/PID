
#Solo a modo de prueba- para verificar su funcionamiento cambien el valor de los atributos.
#Necesitan tener el archivo credenciales.py
from dominio.agenda.agenda import Agenda
from base_datos.agenda_acciones import guardar, obtener_por_usuario

agenda = Agenda(usuario_id=1, fecha="20/09/2026", titulo_reunion="Prueba de guardado", hora_inicio="10:00", hora_fin="11:00")

guardar(agenda)
print("Agenda guardada!")

resultados = obtener_por_usuario(1)
for fila in resultados:
    print(fila.id, fila.titulo, fila.fecha, fila.hora_inicio, fila.hora_fin)
