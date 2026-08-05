"""GG Arena - Sistema de gestion de torneos eSports.

Aplicacion web base (Flask + SQLite) utilizada como SUT (System Under Test)
para la suite de pruebas automatizadas con Selenium.
"""
import argparse
import os
from functools import wraps

from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from app import database
from app.database import JUEGOS, RANGOS
from app.validaciones import validar_jugador, validar_login

app = Flask(__name__)
app.secret_key = os.environ.get("GGARENA_SECRET", "gg-arena-clave-demo")


def login_requerido(vista):
    @wraps(vista)
    def envoltura(*args, **kwargs):
        if "usuario" not in session:
            flash("Debe iniciar sesion para acceder al panel.", "error")
            return redirect(url_for("login"))
        return vista(*args, **kwargs)

    return envoltura


@app.context_processor
def inyectar_contexto():
    return {"usuario_activo": session.get("nombre"), "juegos": JUEGOS, "rangos": RANGOS}


# ------------------------------------------------------------------ sesion
@app.route("/", methods=["GET"])
def inicio():
    return redirect(url_for("listado_jugadores") if "usuario" in session else url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    errores = []
    usuario = ""
    if request.method == "POST":
        usuario = request.form.get("usuario", "")
        clave = request.form.get("clave", "")
        errores = validar_login(usuario, clave)
        if not errores:
            encontrado = database.autenticar(usuario.strip(), clave)
            if encontrado:
                session["usuario"] = encontrado["usuario"]
                session["nombre"] = encontrado["nombre"]
                flash(f"Bienvenido, {encontrado['nombre']}.", "exito")
                return redirect(url_for("listado_jugadores"))
            errores.append("Usuario o contrasena incorrectos.")
    return render_template("login.html", errores=errores, usuario=usuario)


@app.route("/logout")
def logout():
    session.clear()
    flash("Sesion finalizada correctamente.", "exito")
    return redirect(url_for("login"))


# --------------------------------------------------------------- jugadores
@app.route("/jugadores")
@login_requerido
def listado_jugadores():
    busqueda = request.args.get("q", "").strip()
    jugadores = database.listar_jugadores(busqueda)
    return render_template("jugadores.html", jugadores=jugadores, busqueda=busqueda)


@app.route("/jugadores/nuevo", methods=["GET", "POST"])
@login_requerido
def nuevo_jugador():
    datos = {"gamertag": "", "nombre_real": "", "equipo": "", "juego": "", "rango": "", "puntos": ""}
    errores = []
    if request.method == "POST":
        datos, errores = validar_jugador(request.form)
        if not errores:
            database.crear_jugador(datos)
            flash(f"Jugador '{datos['gamertag']}' registrado correctamente.", "exito")
            return redirect(url_for("listado_jugadores"))
    return render_template("formulario.html", datos=datos, errores=errores, modo="crear")


@app.route("/jugadores/<int:jugador_id>/editar", methods=["GET", "POST"])
@login_requerido
def editar_jugador(jugador_id):
    jugador = database.obtener_jugador(jugador_id)
    if not jugador:
        flash("El jugador solicitado no existe.", "error")
        return redirect(url_for("listado_jugadores"))

    errores = []
    datos = jugador
    if request.method == "POST":
        datos, errores = validar_jugador(request.form, jugador_id=jugador_id)
        datos["id"] = jugador_id
        if not errores:
            database.actualizar_jugador(jugador_id, datos)
            flash(f"Jugador '{datos['gamertag']}' actualizado correctamente.", "exito")
            return redirect(url_for("listado_jugadores"))
    return render_template("formulario.html", datos=datos, errores=errores, modo="editar")


@app.route("/jugadores/<int:jugador_id>/eliminar", methods=["POST"])
@login_requerido
def borrar_jugador(jugador_id):
    jugador = database.obtener_jugador(jugador_id)
    if not jugador:
        flash("El jugador solicitado no existe.", "error")
    else:
        database.eliminar_jugador(jugador_id)
        flash(f"Jugador '{jugador['gamertag']}' eliminado correctamente.", "exito")
    return redirect(url_for("listado_jugadores"))


# ------------------------------------------------- utilidades para pruebas
@app.route("/api/health")
def health():
    return {"estado": "ok", "app": "GG Arena"}


@app.route("/api/reset", methods=["POST"])
def reset():
    """Restaura los datos semilla. Solo disponible en modo pruebas."""
    if os.environ.get("GGARENA_TESTING") != "1":
        return {"error": "No disponible"}, 403
    database.reset_db()
    session.clear()
    get_flashed_messages()
    return {"estado": "reiniciado"}


def crear_app():
    database.init_db()
    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GG Arena")
    parser.add_argument("--port", type=int, default=5055)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()
    crear_app().run(host=args.host, port=args.port, debug=False, use_reloader=False)
