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


class GestorAmistades:
    def __init__(self):
        self.solicitudes=[]

    def puedeEnviar(self,emisorID,receptorID):
            return emisorID!=receptorID
    
    def enviarSolicitud(self,emisorID,receptorID):
        if self.puedeEnviar(emisorID,receptorID):
            solicitud=Solicitud(emisorID,receptorID)
            self.solicitudes.append(solicitud)
            return solicitud


gestor=GestorAmistades()
solicitud=gestor.enviarSolicitud(1,1)
print(len(gestor.solicitudes))
