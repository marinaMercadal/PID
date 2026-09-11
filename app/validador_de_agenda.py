
class ValidadorDeAgenda : 
    def validador(self,agenda):

        if agenda.hora_inicio >= agenda.hora_fin:
            raise ValueError("La hora de inicio no puede ser posterior a la hora de finalizacion")
        
        if not agenda.fecha:
            raise ValueError("El campo fecha no puede estar vacío")
        
        if not agenda.titulo_reunion:
            raise ValueError("El campo titulo de la reunion no puede estar vacío")
        
        if not agenda.usuario:
            raise ValueError ("El campo usuario no puede estar vacío")
                    