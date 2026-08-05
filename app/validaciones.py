"""Reglas de negocio y validaciones del formulario de jugadores.

Estas reglas son las que ejercitan las pruebas negativas y de limites
de la suite Selenium.
"""
import re

from app.database import (
    GAMERTAG_MAX,
    GAMERTAG_MIN,
    JUEGOS,
    PUNTOS_MAX,
    PUNTOS_MIN,
    RANGOS,
    existe_gamertag,
)

PATRON_GAMERTAG = re.compile(r"^[A-Za-z0-9_]+$")
NOMBRE_MAX = 60
EQUIPO_MAX = 40


def validar_jugador(form, jugador_id=None):
    """Devuelve (datos_normalizados, lista_de_errores)."""
    errores = []

    gamertag = (form.get("gamertag") or "").strip()
    nombre_real = (form.get("nombre_real") or "").strip()
    equipo = (form.get("equipo") or "").strip()
    juego = (form.get("juego") or "").strip()
    rango = (form.get("rango") or "").strip()
    puntos_raw = (form.get("puntos") or "").strip()

    # --- gamertag
    if not gamertag:
        errores.append("El gamertag es obligatorio.")
    elif len(gamertag) < GAMERTAG_MIN:
        errores.append(f"El gamertag debe tener al menos {GAMERTAG_MIN} caracteres.")
    elif len(gamertag) > GAMERTAG_MAX:
        errores.append(f"El gamertag no puede exceder {GAMERTAG_MAX} caracteres.")
    elif not PATRON_GAMERTAG.match(gamertag):
        errores.append("El gamertag solo admite letras, numeros y guion bajo.")
    elif existe_gamertag(gamertag, excluir_id=jugador_id):
        errores.append(f"El gamertag '{gamertag}' ya esta registrado.")

    # --- nombre real
    if not nombre_real:
        errores.append("El nombre real es obligatorio.")
    elif len(nombre_real) > NOMBRE_MAX:
        errores.append(f"El nombre real no puede exceder {NOMBRE_MAX} caracteres.")

    # --- equipo
    if not equipo:
        errores.append("El equipo es obligatorio.")
    elif len(equipo) > EQUIPO_MAX:
        errores.append(f"El equipo no puede exceder {EQUIPO_MAX} caracteres.")

    # --- juego y rango
    if juego not in JUEGOS:
        errores.append("Debe seleccionar un juego valido.")
    if rango not in RANGOS:
        errores.append("Debe seleccionar un rango valido.")

    # --- puntos
    puntos = None
    if puntos_raw == "":
        errores.append("Los puntos son obligatorios.")
    else:
        try:
            puntos = int(puntos_raw)
        except ValueError:
            errores.append("Los puntos deben ser un numero entero.")
        else:
            if puntos < PUNTOS_MIN or puntos > PUNTOS_MAX:
                errores.append(
                    f"Los puntos deben estar entre {PUNTOS_MIN} y {PUNTOS_MAX}."
                )

    datos = {
        "gamertag": gamertag,
        "nombre_real": nombre_real,
        "equipo": equipo,
        "juego": juego,
        "rango": rango,
        "puntos": puntos if puntos is not None else puntos_raw,
    }
    return datos, errores


def validar_login(usuario, clave):
    errores = []
    if not usuario.strip():
        errores.append("El usuario es obligatorio.")
    if not clave:
        errores.append("La contrasena es obligatoria.")
    return errores
