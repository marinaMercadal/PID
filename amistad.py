class Solicitud:
    def __init__(self,emisorID,receptorID):
        self.emisorID=emisorID
        self.receptorID=receptorID
        self.estado="Pendiente"

    def puedeResponder(self,usuarioID):
        return usuarioID==self.receptorID and self.estado=="Pendiente"

    def aceptar(self,usuarioID):
        if self.puedeResponder(usuarioID):
            self.estado="Aceptada"

    def rechazar(self,usuarioID):
        if self.puedeResponder(usuarioID):
            self.estado="Rechazada"

solicitud=Solicitud(1,2)
solicitud.aceptar(1)
print(solicitud.estado)
solicitud.rechazar(2)
print(solicitud.estado)