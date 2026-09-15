from functools import wraps
from datetime import date, datetime, timedelta
import calendar as modulo_calendario
from flask import Flask, request, render_template, session, redirect, url_for
from dominio.usuario import Usuario
from dominio.juntada.juntada import Juntada
from base_datos.usuario_acciones import guardar
from base_datos.usuario_acciones import buscarPorNombre, verificar_login, buscarPorID, obtenerTodos
from base_datos.credenciales import SECRET_KEY
from amistad_acciones import enviarSolicitud, aceptarSolicitud, rechazarSolicitud
from base_datos.solicitud_acciones import obtenerRecibidas, obtener_amigos_de_usuario
from base_datos.agenda_acciones import obtener_por_usuario as obtener_agenda_de_usuario
from base_datos.juntada_acciones import (
    guardar as guardar_juntada,
    obtener_organizadas_por_usuario,
    obtener_invitaciones_de_usuario,
    obtener_por_id as obtener_juntada_por_id,
    obtener_invitados_de_juntada,
    responder_invitacion,
)

NOMBRES_MES = [
    "", "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
]
DIAS_SEMANA = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]

app= Flask(__name__)
app.config["SECRET_KEY"]=SECRET_KEY

def login_requerido(vista):
    @wraps(vista)
    def decorador(*args, **kwargs):
        if "usuarioID" not in session:
            return redirect(url_for("mostrar_login"))
        return vista(*args, **kwargs)
    return decorador

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
    return redirect(url_for("mostrar_calendario"))





@app.route("/logout",methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("mostrar_login"))

@app.route("/calendario",methods=["GET"])
@login_requerido
def mostrar_calendario():
    usuario_id=session["usuarioID"]

    fecha_parametro=request.args.get("fecha")
    try:
        fecha_seleccionada=date.fromisoformat(fecha_parametro) if fecha_parametro else date.today()
    except ValueError:
        fecha_seleccionada=date.today()

    eventos=[]

    for agenda in obtener_agenda_de_usuario(usuario_id):
        if agenda.fecha==fecha_seleccionada:
            eventos.append({
                "titulo":agenda.titulo,"hora_inicio":agenda.hora_inicio,"hora_fin":agenda.hora_fin,
                "detalle":"Personal","puede_responder":False,
            })

    for juntada in obtener_organizadas_por_usuario(usuario_id):
        if juntada.fecha==fecha_seleccionada:
            invitados=obtener_invitados_de_juntada(juntada.id)
            confirmados=sum(1 for invitado in invitados if invitado.estado=="Si")
            eventos.append({
                "titulo":juntada.titulo,"hora_inicio":juntada.hora_inicio,"hora_fin":juntada.hora_fin,
                "detalle":f"Organizás · {confirmados}/{len(invitados)} confirmaron","puede_responder":False,
            })

    invitaciones_pendientes=[]

    for invitacion in obtener_invitaciones_de_usuario(usuario_id):
        if invitacion.estado=="No":
            continue
        juntada=obtener_juntada_por_id(invitacion.juntada_id)
        if juntada is None:
            continue

        if invitacion.estado in ("Pendiente","Tal vez"):
            invitaciones_pendientes.append({
                "titulo":juntada.titulo,"fecha":juntada.fecha,
                "hora_inicio":juntada.hora_inicio,"hora_fin":juntada.hora_fin,
                "juntada_id":juntada.id,
            })

        if juntada.fecha==fecha_seleccionada:
            detalle={"Si":"Confirmaste","Tal vez":"Dijiste tal vez"}.get(invitacion.estado,"Invitación pendiente")
            eventos.append({
                "titulo":juntada.titulo,"hora_inicio":juntada.hora_inicio,"hora_fin":juntada.hora_fin,
                "detalle":detalle,"puede_responder":invitacion.estado in ("Pendiente","Tal vez"),
                "juntada_id":juntada.id,
            })

    eventos.sort(key=lambda evento: evento["hora_inicio"])
    invitaciones_pendientes.sort(key=lambda invitacion: (invitacion["fecha"], invitacion["hora_inicio"]))

    semanas=modulo_calendario.Calendar(firstweekday=0).monthdatescalendar(
        fecha_seleccionada.year, fecha_seleccionada.month
    )
    primer_dia_mes=fecha_seleccionada.replace(day=1)
    mes_anterior=primer_dia_mes-timedelta(days=1)
    ultimo_dia_mes=modulo_calendario.monthrange(fecha_seleccionada.year,fecha_seleccionada.month)[1]
    mes_siguiente=fecha_seleccionada.replace(day=ultimo_dia_mes)+timedelta(days=1)

    return render_template(
        "calendario.html",
        fecha_seleccionada=fecha_seleccionada,
        eventos=eventos,
        invitaciones_pendientes=invitaciones_pendientes,
        semanas=semanas,
        hoy=date.today(),
        mes_anterior=mes_anterior.replace(day=1),
        mes_siguiente=mes_siguiente.replace(day=1),
        nombre_mes=NOMBRES_MES[fecha_seleccionada.month],
        dias_semana=DIAS_SEMANA,
    )

@app.route("/juntada/nueva",methods=["GET"])
@login_requerido
def mostrar_nueva_juntada():
    amigos=[buscarPorID(amigo_id) for amigo_id in obtener_amigos_de_usuario(session["usuarioID"])]
    fecha_sugerida=request.args.get("fecha", date.today().isoformat())
    return render_template("juntada_nueva.html", amigos=amigos, fecha_sugerida=fecha_sugerida, error=None)

@app.route("/juntada/nueva",methods=["POST"])
@login_requerido
def crear_juntada():
    usuario_id=session["usuarioID"]
    fecha_parametro=request.form.get("fecha","")
    invitados_ids=[int(id) for id in request.form.getlist("invitados")]
    amigos_ids=obtener_amigos_de_usuario(usuario_id)

    if not set(invitados_ids).issubset(set(amigos_ids)):
        amigos=[buscarPorID(amigo_id) for amigo_id in amigos_ids]
        return render_template(
            "juntada_nueva.html", amigos=amigos, fecha_sugerida=fecha_parametro,
            error="Solo podés invitar a tus amigos."
        ), 400

    try:
        fecha_formateada=datetime.strptime(fecha_parametro, "%Y-%m-%d").strftime("%d/%m/%Y")
        juntada=Juntada(
            organizador=usuario_id,
            fecha=fecha_formateada,
            titulo_juntada=request.form.get("titulo"),
            hora_inicio=request.form.get("hora_inicio"),
            hora_fin=request.form.get("hora_fin"),
            amigos_invitados=invitados_ids,
        )
    except ValueError as error:
        amigos=[buscarPorID(amigo_id) for amigo_id in amigos_ids]
        return render_template(
            "juntada_nueva.html", amigos=amigos, fecha_sugerida=fecha_parametro, error=str(error)
        ), 400

    guardar_juntada(juntada)
    return redirect(url_for("mostrar_calendario", fecha=fecha_parametro))

@app.route("/juntada/<int:juntada_id>/responder",methods=["POST"])
@login_requerido
def responder_juntada(juntada_id):
    responder_invitacion(juntada_id, session["usuarioID"], request.form.get("respuesta"))
    fecha_parametro=request.form.get("fecha")
    return redirect(url_for("mostrar_calendario", fecha=fecha_parametro) if fecha_parametro else url_for("mostrar_calendario"))

@app.route("/amistad",methods=["GET"])
@login_requerido
def mostrar_amistad():
    nombre=request.args.get("nombre","")
    personas=buscarPorNombre(nombre)
    recibidas=[
        {"solicitud": solicitud, "emisor": buscarPorID(solicitud.emisorID)}
        for solicitud in obtenerRecibidas(session["usuarioID"])
    ]
    sugerencias=[
        usuario for usuario in obtenerTodos()
        if usuario.id != session["usuarioID"]
    ]

    return render_template(
        "amistad.html",
        personas=personas,
        nombre=nombre,
        recibidas=recibidas,
        sugerencias=sugerencias
    )

@app.route("/amistad/enviar/<int:receptorID>",methods=["POST"])
@login_requerido
def enviar_solicitud(receptorID):
    emisorID=session["usuarioID"]
    solicitud=enviarSolicitud(emisorID,receptorID)

    if solicitud is None:
        return "No se puede enviar esta solicitud.", 400

    return redirect(url_for("mostrar_amistad"))

@app.route("/amistad/aceptar/<int:solicitudID>",methods=["POST"])
@login_requerido
def aceptar_solicitud(solicitudID):
    aceptada=aceptarSolicitud(solicitudID,session["usuarioID"])

    if not aceptada:
        return "No se puede aceptar esta solicitud", 400

    return redirect(url_for("mostrar_amistad"))

@app.route("/amistad/rechazar/<int:solicitudID>",methods=["POST"])
@login_requerido
def rechazar_solicitud(solicitudID):
    rechazada=rechazarSolicitud(solicitudID,session["usuarioID"])

    if not rechazada:
        return "No se puede rechazar esta solicitud", 400

    return redirect(url_for("mostrar_amistad"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)