#corran esto en la terminal chcias para ver q anda!

from base_datos.configuracion import engine
conexion=engine.connect()

print("Conectadp!")
conexion.close()

