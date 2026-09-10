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

    
    def esEntre(self,primerID,segundoID):
        mismoSentido=self.emisorID==primerID and self.receptorID==segundoID
        sentidoInverso=self.emisorID==segundoID and self.receptorID==primerID

        return mismoSentido or sentidoInverso


class GestorAmistades:
    def __init__(self):
        self.solicitudes=[]

    def puedeEnviar(self,emisorID,receptorID):
        sonDistintos= emisorID!=receptorID
        hayPendiente=self.haySolicitudPendiente(emisorID,receptorID)
        yaSonAmigos = self.sonAmigos(emisorID,receptorID)
        return sonDistintos and not hayPendiente and not yaSonAmigos
    
    def sonAmigos(self,primerID,segundoID):
        for solicitud in self.solicitudes:
            esEntreUsuarios=solicitud.esEntre(primerID,segundoID)
            estaAceptada=(solicitud.estado=="Aceptada")
            if esEntreUsuarios and estaAceptada:
                return True
        return False
    
    def enviarSolicitud(self,emisorID,receptorID):
        if self.puedeEnviar(emisorID,receptorID):
            solicitud=Solicitud(emisorID,receptorID)
            self.solicitudes.append(solicitud)
            return solicitud

    def haySolicitudPendiente(self,emisorID,receptorID):
        for solicitud in self.solicitudes:
            esEntreUsuarios=solicitud.esEntre(emisorID,receptorID)
            estaPendiente=(solicitud.estado=="Pendiente")
            if esEntreUsuarios and estaPendiente:
                return True
        return False

    


gestor = GestorAmistades()
solicitud = gestor.enviarSolicitud(1, 2)
solicitud.aceptar(2)

print(gestor.sonAmigos(1, 2))  
print(gestor.sonAmigos(2, 1))  
gestor.enviarSolicitud(2, 1)
print(len(gestor.solicitudes))  
