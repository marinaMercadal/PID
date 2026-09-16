from functools import wraps
import secrets
from datetime import date, datetime, timedelta
import calendar as modulo_calendario
from flask import Flask, request, render_template, session, redirect, url_for
from dominio.usuario import Usuario
from dominio.juntada.juntada import Juntada
from dominio.agenda.agenda import Agenda
from base_datos.usuario_acciones import guardar, actualizar_perfil, dar_de_baja
from base_datos.usuario_acciones import buscarPorNombre, verificar_login, buscarPorID, obtenerTodos
from base_datos.credenciales import SECRET_KEY
from amistad_acciones import enviarSolicitud, aceptarSolicitud, rechazarSolicitud
from base_datos.solicitud_acciones import obtenerRecibidas, obtener_amigos_de_usuario
from base_datos.agenda_acciones import obtener_por_usuario as obtener_agenda_de_usuario
from base_datos.agenda_acciones import guardar as guardar_agenda
from base_datos.juntada_acciones import (
    guardar as guardar_juntada,
    obtener_organizadas_del_dia,
    obtener_invitaciones_del_calendario,
    obtener_invitados_organizador,
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
        usuario=buscarPorID(session["usuarioID"])
        if usuario is None or not usuario.activo:
            session.clear()
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
        return render_template("registro.html", error=str(error), nombre=nombre, email=email), 400

    return redirect(url_for("mostrar_login", registrado="1"))


@app.route("/registro", methods = ["GET"])
def mostrar_registro():
    return render_template("registro.html", error=None, nombre="", email="")

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

@app.route("/perfil",methods=["GET","POST"])
@login_requerido
def mostrar_perfil():
    usuario=buscarPorID(session["usuarioID"])
    if usuario is None:
        session.clear()
        return redirect(url_for("mostrar_login"))

    if "perfil_token" not in session:
        session["perfil_token"]=secrets.token_hex(32)
    nombre=usuario.nombre
    email=usuario.email
    error=None
    estado=200

    if request.method=="POST":
        if not secrets.compare_digest(request.form.get("token",""),session["perfil_token"]):
            return "El formulario venció. Recargá la página e intentá nuevamente.",400
        nombre=request.form.get("nombre","")
        try:
            actualizar_perfil(session["usuarioID"],nombre)
        except ValueError as problema:
            error=str(problema)
            estado=400
        else:
            session["perfil_guardado"]=True
            return redirect(url_for("mostrar_perfil"))

    guardado=session.pop("perfil_guardado",False)
    return render_template("perfil.html",nombre=nombre,email=email,error=error,guardado=guardado),estado

@app.route("/perfil/baja",methods=["POST"])
@login_requerido
def baja_cuenta():
    token=session.get("perfil_token")
    if not token or not secrets.compare_digest(request.form.get("token",""),token):
        return "El formulario venció. Recargá la página e intentá nuevamente.",400
    usuario=buscarPorID(session["usuarioID"])
    try:
        if request.form.get("confirmar")!="si":
            raise ValueError("Confirmá que querés dar de baja tu cuenta")
        dar_de_baja(session["usuarioID"],request.form.get("password",""))
    except ValueError as error:
        return render_template("perfil.html",nombre=usuario.nombre,email=usuario.email,error=str(error),guardado=False),400
    session.clear()
    return redirect(url_for("mostrar_login",baja="1"))

@app.route("/calendario",methods=["GET"])
@login_requerido
def mostrar_calendario():
    usuario_id=session["usuarioID"]

    fecha_parametro=request.args.get("fecha")
    try:
        fecha_seleccionada=date.fromisoformat(fecha_parametro) if fecha_parametro else date.today()
    except ValueError:
        fecha_seleccionada=date.today()

    inicio_mes=fecha_seleccionada.replace(day=1)
    fin_mes=fecha_seleccionada.replace(day=modulo_calendario.monthrange(fecha_seleccionada.year,fecha_seleccionada.month)[1])
    eventos=[]

    for agenda in obtener_agenda_de_usuario(usuario_id,inicio_mes,fin_mes):
        eventos.append({
            "fecha":agenda.fecha,"titulo":agenda.titulo,"hora_inicio":agenda.hora_inicio,"hora_fin":agenda.hora_fin,
            "detalle":"Personal","puede_responder":False,
        })

    invitados_por_juntada={}
    for juntada_id,nombre_invitado in obtener_invitados_organizador(usuario_id,inicio_mes,fin_mes):
        invitados_por_juntada.setdefault(juntada_id,[]).append(nombre_invitado)

    for juntada,confirmados,total in obtener_organizadas_del_dia(usuario_id,inicio_mes,fin_mes):
        invitados=", ".join(invitados_por_juntada.get(juntada.id,[]))
        eventos.append({
            "fecha":juntada.fecha,"titulo":juntada.titulo,"hora_inicio":juntada.hora_inicio,"hora_fin":juntada.hora_fin,
            "detalle":f"Organizás · {confirmados}/{total} confirmaron · Invitados: {invitados}","puede_responder":False,
        })

    invitaciones_pendientes=[]

    for invitacion,juntada in obtener_invitaciones_del_calendario(usuario_id,inicio_mes,fin_mes):
        if invitacion.estado in ("Pendiente","Tal vez"):
            invitaciones_pendientes.append({
                "titulo":juntada.titulo,"fecha":juntada.fecha,
                "hora_inicio":juntada.hora_inicio,"hora_fin":juntada.hora_fin,
                "juntada_id":juntada.id,
            })

        if inicio_mes<=juntada.fecha<=fin_mes:
            detalle={"Si":"Confirmaste","Tal vez":"Dijiste tal vez"}.get(invitacion.estado,"Invitación pendiente")
            eventos.append({
                "fecha":juntada.fecha,"titulo":juntada.titulo,"hora_inicio":juntada.hora_inicio,"hora_fin":juntada.hora_fin,
                "detalle":detalle,"puede_responder":invitacion.estado in ("Pendiente","Tal vez"),
                "juntada_id":juntada.id,
            })

    eventos.sort(key=lambda evento: evento["hora_inicio"])
    dias_mes=[inicio_mes+timedelta(days=i) for i in range(fin_mes.day)]
    eventos_por_dia={dia:[evento for evento in eventos if evento["fecha"]==dia] for dia in dias_mes}
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
        eventos=eventos_por_dia[fecha_seleccionada],
        eventos_por_dia=eventos_por_dia,
        dias_mes=dias_mes,
        invitaciones_pendientes=invitaciones_pendientes,
        semanas=semanas,
        hoy=date.today(),
        mes_anterior=mes_anterior.replace(day=1),
        mes_siguiente=mes_siguiente.replace(day=1),
        nombre_mes=NOMBRES_MES[fecha_seleccionada.month],
        dias_semana=DIAS_SEMANA,
    )

@app.route("/agenda/nueva",methods=["GET"])
@login_requerido
def mostrar_nueva_agenda():
    fecha_sugerida=request.args.get("fecha", date.today().isoformat())
    return render_template("agenda_nueva.html", fecha_sugerida=fecha_sugerida, error=None)

@app.route("/agenda/nueva",methods=["POST"])
@login_requerido
def crear_agenda():
    usuario_id=session["usuarioID"]
    fecha_parametro=request.form.get("fecha","")

    try:
        fecha_formateada=datetime.strptime(fecha_parametro, "%Y-%m-%d").strftime("%d/%m/%Y")
        agenda=Agenda(
            usuario_id=usuario_id,
            fecha=fecha_formateada,
            titulo_reunion=request.form.get("titulo"),
            hora_inicio=request.form.get("hora_inicio"),
            hora_fin=request.form.get("hora_fin"),
        )
    except ValueError as error:
        return render_template("agenda_nueva.html", fecha_sugerida=fecha_parametro, error=str(error)), 400

    guardar_agenda(agenda)
    return redirect(url_for("mostrar_calendario", fecha=fecha_parametro))

@app.route("/juntada/nueva",methods=["GET"])
@login_requerido
def mostrar_nueva_juntada():
    amigos=[buscarPorID(amigo_id) for amigo_id in obtener_amigos_de_usuario(session["usuarioID"])]
    amigos=[amigo for amigo in amigos if amigo is not None]
    invitado_id=request.args.get("invitado",type=int)
    seleccionados=[amigo.id for amigo in amigos if amigo.id==invitado_id]
    fecha_sugerida=request.args.get("fecha", date.today().isoformat())
    return render_template("juntada_nueva.html", amigos=amigos, fecha_sugerida=fecha_sugerida, error=None, seleccionados=seleccionados)

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
            error="Solo podés invitar a tus amigos.",
            seleccionados=[id for id in invitados_ids if id in amigos_ids]
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
            "juntada_nueva.html", amigos=amigos, fecha_sugerida=fecha_parametro, error=str(error),
            seleccionados=invitados_ids
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
    usuarios=obtenerTodos()
    amigos_ids=set(obtener_amigos_de_usuario(session["usuarioID"]))
    amigos=[usuario for usuario in usuarios if usuario.id in amigos_ids]
    amigos.sort(key=lambda usuario: (usuario.nombre.casefold(),usuario.id))
    sugerencias=[
        usuario for usuario in usuarios
        if usuario.id != session["usuarioID"]
    ]

    return render_template(
        "amistad.html",
        personas=personas,
        nombre=nombre,
        recibidas=recibidas,
        sugerencias=sugerencias,
        amigos=amigos,
        amigos_ids=amigos_ids
    )

@app.route("/amistad/enviar/<int:receptorID>",methods=["POST"])
@login_requerido
def enviar_solicitud(receptorID):
    emisorID=session["usuarioID"]
    receptor=buscarPorID(receptorID)
    if receptor is None or not receptor.activo:
        return "Ese usuario no está disponible.",400
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
