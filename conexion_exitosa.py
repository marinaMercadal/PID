from base_datos.configuracion import engine
conexion=engine.connect()

print("Conectadp!")
conexion.close()

