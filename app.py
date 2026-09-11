from flask import Flask, request, render_template, session, redirect, url_for
from dominio.usuario import Usuario
from base_datos.usuario_acciones import guardar
from base_datos.usuario_acciones import buscarPorNombre, verificar_login
from base_datos.credenciales import SECRET_KEY
from amistad_acciones import enviarSolicitud, aceptarSolicitud, rechazarSolicitud
from base_datos.solicitud_acciones import obtenerRecibidas

app= Flask(__name__)
app.config["SECRET_KEY"]=SECRET_KEY

@app.route("/registro", methods=["POST"])
def registro():
    nombre=request.form.get("nombre")
    email=request.form.get("email")
    password=request.form.get("password")

    try:
        usuario=Usuario(email,password,nombre)
        guardar(usuario)
    except ValueError as error:
        return str(error), 400

    return "Usuario registrado con éxito", 201


@app.route("/registro", methods = ["GET"])
def mostrar_registro():
    return render_template("registro.html")

@app.route("/login",methods=["GET"])
def mostrar_login():
    return render_template("login.html")

@app.route("/login",methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    usuario_encontrado=verificar_login(email,password)
    if usuario_encontrado is None:
        return render_template("login.html", error="Email o contraseña incorrectos"), 401
 
    session.clear()
    session["usuarioID"]=usuario_encontrado.id
    return redirect(url_for("mostrar_amistad"))





@app.route("/amistad",methods=["GET"])
def mostrar_amistad():
    if "usuarioID" not in session:
        return redirect(url_for("mostrar_login"))
    nombre=request.args.get("nombre","")
    personas=buscarPorNombre(nombre)
    recibidas=obtenerRecibidas(session["usuarioID"])

    return render_template(
        "amistad.html",
        personas=personas,
        nombre=nombre,
        recibidas=recibidas
    )

@app.route("/amistad/enviar/<int:receptorID>",methods=["POST"])
def enviar_solicitud(receptorID):
    if "usuarioID" not in session:
        return redirect(url_for("mostrar_login"))

    emisorID=session["usuarioID"]
    solicitud=enviarSolicitud(emisorID,receptorID)

    if solicitud is None:
        return "No se puede enviar esta solicitud.", 400

    return redirect(url_for("mostrar_amistad"))

@app.route("/amistad/aceptar/<int:solicitudID>",methods=["POST"])
def aceptar_solicitud(solicitudID):
    if "usuarioID" not in session:
        return redirect(url_for("mostrar_login"))

    aceptada=aceptarSolicitud(solicitudID,session["usuarioID"])

    if not aceptada:
        return "No se puede aceptar esta solicitud", 400

    return redirect(url_for("mostrar_amistad"))

@app.route("/amistad/rechazar/<int:solicitudID>",methods=["POST"])
def rechazar_solicitud(solicitudID):
    if "usuarioID" not in session:
        return redirect(url_for("mostrar_login"))

    rechazada=rechazarSolicitud(solicitudID,session["usuarioID"])

    if not rechazada:
        return "No se puede rechazar esta solicitud", 400

    return redirect(url_for("mostrar_amistad"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)