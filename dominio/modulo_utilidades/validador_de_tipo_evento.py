class ValidadorDetipoEvento:
    def validar(self, fecha, hora_inicio, hora_fin, titulo, responsable):
        if not responsable:
            raise ValueError("El campo responsable no puede estar vacío")

        if not titulo:
            raise ValueError("El campo titulo no puede estar vacío")

        if not fecha:
            raise ValueError("El campo fecha no puede estar vacío")

        if hora_inicio >= hora_fin:
            raise ValueError("La hora de inicio no puede ser posterior a la hora de finalizacion")
