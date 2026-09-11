from flask import Flask, request , render_template
from dominio.usuario import Usuario
from base_datos.usuario_acciones import guardar
from base_datos.usuario_acciones import buscarPorNombre

app= Flask(__name__)

@app.route("/registro", methods=["POST"])
def registro():
    nombre=request.form.get("nombre")
    email=request.form.get("email")
    password=request.form.get("password")

    try:
        usuario=Usuario(email,password,nombre)

    except ValueError as error:
        return str(error), 400

    guardar(usuario)
    return "Usuario registrado con éxito", 201

@app.route("/registro", methods = ["GET"])
def mostrar_registro():
    return render_template("registro.html")

@app.route("/amistad",methods=["GET"])
def mostrar_amistad():
    nombre=request.args.get("nombre","")
    personas=buscarPorNombre(nombre)

    return render_template(
        "amistad.html",
        personas=personas,
        nombre=nombre
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)