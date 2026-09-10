import unittest
from amistad import GestorAmistades


class TestAmistades(unittest.TestCase):
    def test_enviar_solicitud(self):
        gestor=GestorAmistades()

        solicitud=gestor.enviarSolicitud(1,2)

        self.assertEqual(solicitud.estado,"Pendiente")
        self.assertEqual(len(gestor.solicitudes),1)

    def test_aceptar_solicitud(self):
        gestor=GestorAmistades()
        solicitud=gestor.enviarSolicitud(1,2)

        solicitud.aceptar(2)

        self.assertEqual(solicitud.estado,"Aceptada")
        self.assertTrue(gestor.sonAmigos(1,2))
        self.assertEqual(len(gestor.solicitudesRecibidas(2)),0)

    def test_rechazar_solicitud(self):
        gestor=GestorAmistades()
        solicitud=gestor.enviarSolicitud(1,2)

        solicitud.rechazar(2)

        self.assertEqual(solicitud.estado,"Rechazada")
        self.assertFalse(gestor.sonAmigos(1,2))
        self.assertEqual(len(gestor.solicitudesRecibidas(2)),0)

    def test_emisor_no_puede_aceptar(self):
        gestor=GestorAmistades()
        solicitud=gestor.enviarSolicitud(1,2)

        solicitud.aceptar(1)

        self.assertEqual(solicitud.estado,"Pendiente")
        self.assertFalse(gestor.sonAmigos(1,2))
        self.assertEqual(len(gestor.solicitudesRecibidas(2)),1)

    def test_emisor_no_puede_rechazar(self):
        gestor=GestorAmistades()
        solicitud=gestor.enviarSolicitud(1,2)

        solicitud.rechazar(1)

        self.assertEqual(solicitud.estado,"Pendiente")
        self.assertEqual(len(gestor.solicitudesRecibidas(2)),1)

    def test_no_permite_enviarse_a_uno_mismo(self):
        gestor=GestorAmistades()

        resultado=gestor.enviarSolicitud(1,1)

        self.assertIsNone(resultado)
        self.assertEqual(len(gestor.solicitudes),0)

    def test_no_permite_solicitud_duplicada(self):
        gestor=GestorAmistades()
        primera=gestor.enviarSolicitud(1,2)

        segunda=gestor.enviarSolicitud(1,2)

        self.assertIsNone(segunda)
        self.assertEqual(len(gestor.solicitudes),1)
        self.assertEqual(gestor.solicitudesRecibidas(2),[primera])

    def test_no_permite_solicitud_cruzada(self):
        gestor=GestorAmistades()
        primera=gestor.enviarSolicitud(1,2)

        segunda=gestor.enviarSolicitud(2,1)

        self.assertIsNone(segunda)
        self.assertEqual(len(gestor.solicitudes),1)
        self.assertEqual(gestor.solicitudesRecibidas(2),[primera])
        self.assertEqual(gestor.solicitudesRecibidas(1),[])

    def test_no_permite_solicitudes_entre_amigos(self):
        gestor=GestorAmistades()
        solicitud=gestor.enviarSolicitud(1,2)
        solicitud.aceptar(2)

        mismoSentido=gestor.enviarSolicitud(1,2)
        sentidoInverso=gestor.enviarSolicitud(2,1)

        self.assertIsNone(mismoSentido)
        self.assertIsNone(sentidoInverso)
        self.assertEqual(len(gestor.solicitudes),1)
        self.assertTrue(gestor.sonAmigos(1,2))
        self.assertTrue(gestor.sonAmigos(2,1))

    def test_no_permite_rechazar_una_solicitud_aceptada(self):
        gestor=GestorAmistades()
        solicitud=gestor.enviarSolicitud(1,2)
        solicitud.aceptar(2)

        solicitud.rechazar(2)

        self.assertEqual(solicitud.estado,"Aceptada")
        self.assertTrue(gestor.sonAmigos(1,2))
        self.assertEqual(len(gestor.solicitudesRecibidas(2)),0)

    def test_no_permite_aceptar_una_solicitud_rechazada(self):
        gestor=GestorAmistades()
        solicitud=gestor.enviarSolicitud(1,2)
        solicitud.rechazar(2)

        solicitud.aceptar(2)

        self.assertEqual(solicitud.estado,"Rechazada")
        self.assertFalse(gestor.sonAmigos(1,2))
        self.assertEqual(len(gestor.solicitudesRecibidas(2)),0)

    def test_recibidas_solo_incluye_solicitudes_del_usuario(self):
        gestor=GestorAmistades()
        paraUsuario2=gestor.enviarSolicitud(1,2)
        paraUsuario3=gestor.enviarSolicitud(1,3)

        self.assertEqual(
            gestor.solicitudesRecibidas(2),[paraUsuario2]
        )
        self.assertEqual(
            gestor.solicitudesRecibidas(3),[paraUsuario3]
        )
        self.assertEqual(gestor.solicitudesRecibidas(1),[])

if __name__=="__main__":
    unittest.main()