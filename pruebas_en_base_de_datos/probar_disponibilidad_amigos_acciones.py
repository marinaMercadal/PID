# Solo a modo de prueba - para verificar su funcionamiento cambien el valor de los atributos.
# Necesitan tener el archivo credenciales.py

from datetime import date
from dominio.agenda.agenda import Agenda
from base_datos.agenda_acciones import guardar as guardar_agenda
from base_datos.disponibilidad_amigo_acciones import obtener_disponibilidad

FECHA_PRUEBA = "25/09/2026"

# Le cargamos un bloque de agenda a juan (id 7), para tener algo que ver
agenda_de_juan = Agenda(
    usuario_id=7,
    fecha=FECHA_PRUEBA,
    titulo_reunion="Dentista",
    hora_inicio="15:00",
    hora_fin="16:00",
)
guardar_agenda(agenda_de_juan)
print("Bloque de agenda de juan guardado.")

# Marina (id 1, amiga de juan) consulta la disponibilidad de juan
disponibilidad = obtener_disponibilidad(
    usuario_solicitante_id=1,
    amigo_id=7,
    fecha=date(2026, 9, 25),
)
print("\nDisponibilidad de juan el", FECHA_PRUEBA, "vista por Marina:")
for bloque in disponibilidad:
    print("Ocupado de", bloque["hora_inicio"], "a", bloque["hora_fin"])

# Caso negativo: Marina intenta ver la disponibilidad de alguien que NO es su amigo
print("\nProbando con alguien que NO es amigo de Marina (deberia fallar):")
try:
    obtener_disponibilidad(usuario_solicitante_id=1, amigo_id=8, fecha=date(2026, 9, 25))
    print("ERROR: no debería haber llegado hasta acá")
except ValueError as error:
    print("Bloqueado correctamente:", error)