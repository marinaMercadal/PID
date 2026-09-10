PID - JuntApp

Backend: Python + Flask
Base de datos: MySQL (alojada en Aiven, gratis, compartida entre las 3)
ORM: SQLAlchemy
Frontend: HTML + CSS (responsive, sin framework de JS por ahora)

Instalar dependencias

pip install -r requirements.txt

Crear Creadenciales en:

base_datos/credenciales.py

En la raiz del proyecto agregar certificado de conexion Aiven

PID/ca.pem

