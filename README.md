->PID - JuntApp

Backend: Python + Flask
Base de datos: MySQL (alojada en Aiven, gratis, compartida entre las 3)
-> ORM: SQLAlchemy
Frontend: HTML + CSS (responsive, sin framework de JS por ahora)

-> Instalar dependencias

pip install -r requirements.txt

-> Crear Creadenciales en:

base_datos/credenciales.py

-> En la raiz del proyecto agregar certificado de conexion Aiven

PID/ca.pem

-> correr app:

python3 app.py y abri http://localhost:5000

-> tets:

Usamos pytest para probar las validaciones de las clases de dominio. Para correrlos:

pytest -v