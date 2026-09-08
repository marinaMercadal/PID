class Solicitud:
    def __init__(self,emisorID,receptorID):
        self.emisorID=emisorID
        self.receptorID=receptorID
        self.estado="Pendiente"

    def aceptar(self):
        if self.estado=="Pendiente":
            self.estado="Aceptada"

    def rechazar(self):
        if self.estado=="Pendiente":
            self.estado="Rechazada"

solicitud=Solicitud(1,2)
print(solicitud.estado)
solicitud.aceptar()
solicitud.rechazar()
print(solicitud.estado)