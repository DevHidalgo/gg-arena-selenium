"""Capa de acceso a datos de GG Arena (SQLite, sin ORM externo)."""
import os
import sqlite3
from pathlib import Path

DB_PATH = os.environ.get(
    "GGARENA_DB",
    str(Path(__file__).resolve().parent.parent / "ggarena.db"),
)

JUEGOS = ["Valorant", "League of Legends", "Counter-Strike 2", "Dota 2", "Rocket League"]
RANGOS = ["Bronce", "Plata", "Oro", "Platino", "Diamante", "Inmortal"]

PUNTOS_MIN = 0
PUNTOS_MAX = 10000
GAMERTAG_MIN = 3
GAMERTAG_MAX = 20


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(seed=True):
    """Crea el esquema y carga los datos iniciales."""
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    cur = conn.cursor()
    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id       INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario  TEXT NOT NULL UNIQUE,
            clave    TEXT NOT NULL,
            nombre   TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS jugadores (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            gamertag     TEXT NOT NULL UNIQUE,
            nombre_real  TEXT NOT NULL,
            equipo       TEXT NOT NULL,
            juego        TEXT NOT NULL,
            rango        TEXT NOT NULL,
            puntos       INTEGER NOT NULL DEFAULT 0
        );
        """
    )
    conn.commit()

    if seed:
        cur.execute("SELECT COUNT(*) AS total FROM usuarios")
        if cur.fetchone()["total"] == 0:
            cur.executemany(
                "INSERT INTO usuarios (usuario, clave, nombre) VALUES (?, ?, ?)",
                [
                    ("admin", "Arena2026*", "Administrador de Torneos"),
                    ("arbitro", "Referee2026*", "Arbitro Oficial"),
                ],
            )

        cur.execute("SELECT COUNT(*) AS total FROM jugadores")
        if cur.fetchone()["total"] == 0:
            cur.executemany(
                """INSERT INTO jugadores (gamertag, nombre_real, equipo, juego, rango, puntos)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                [
                    ("ShadowRD", "Luis Peralta", "Quisqueya Kings", "Valorant", "Inmortal", 8450),
                    ("ByteQueen", "Ana Fermin", "Caribe Titans", "League of Legends", "Diamante", 7320),
                    ("NitroDom", "Carlos Nunez", "Santo Domingo eSports", "Counter-Strike 2", "Platino", 5610),
                    ("PixelWitch", "Maria Rosario", "Caribe Titans", "Dota 2", "Oro", 4180),
                ],
            )
        conn.commit()
    conn.close()


def reset_db():
    """Reinicia la base de datos (utilizado por la suite de pruebas)."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db(seed=True)


# ---------------------------------------------------------------- usuarios
def autenticar(usuario, clave):
    conn = get_connection()
    fila = conn.execute(
        "SELECT * FROM usuarios WHERE usuario = ? AND clave = ?", (usuario, clave)
    ).fetchone()
    conn.close()
    return dict(fila) if fila else None


# --------------------------------------------------------------- jugadores
def listar_jugadores(busqueda=""):
    conn = get_connection()
    if busqueda:
        patron = f"%{busqueda}%"
        filas = conn.execute(
            """SELECT * FROM jugadores
               WHERE gamertag LIKE ? OR nombre_real LIKE ? OR equipo LIKE ?
               ORDER BY puntos DESC""",
            (patron, patron, patron),
        ).fetchall()
    else:
        filas = conn.execute("SELECT * FROM jugadores ORDER BY puntos DESC").fetchall()
    conn.close()
    return [dict(f) for f in filas]


def obtener_jugador(jugador_id):
    conn = get_connection()
    fila = conn.execute("SELECT * FROM jugadores WHERE id = ?", (jugador_id,)).fetchone()
    conn.close()
    return dict(fila) if fila else None


def existe_gamertag(gamertag, excluir_id=None):
    conn = get_connection()
    if excluir_id:
        fila = conn.execute(
            "SELECT id FROM jugadores WHERE LOWER(gamertag) = LOWER(?) AND id <> ?",
            (gamertag, excluir_id),
        ).fetchone()
    else:
        fila = conn.execute(
            "SELECT id FROM jugadores WHERE LOWER(gamertag) = LOWER(?)", (gamertag,)
        ).fetchone()
    conn.close()
    return fila is not None


def crear_jugador(datos):
    conn = get_connection()
    cur = conn.execute(
        """INSERT INTO jugadores (gamertag, nombre_real, equipo, juego, rango, puntos)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (
            datos["gamertag"],
            datos["nombre_real"],
            datos["equipo"],
            datos["juego"],
            datos["rango"],
            datos["puntos"],
        ),
    )
    conn.commit()
    nuevo_id = cur.lastrowid
    conn.close()
    return nuevo_id


def actualizar_jugador(jugador_id, datos):
    conn = get_connection()
    conn.execute(
        """UPDATE jugadores
           SET gamertag = ?, nombre_real = ?, equipo = ?, juego = ?, rango = ?, puntos = ?
           WHERE id = ?""",
        (
            datos["gamertag"],
            datos["nombre_real"],
            datos["equipo"],
            datos["juego"],
            datos["rango"],
            datos["puntos"],
            jugador_id,
        ),
    )
    conn.commit()
    conn.close()


def eliminar_jugador(jugador_id):
    conn = get_connection()
    conn.execute("DELETE FROM jugadores WHERE id = ?", (jugador_id,))
    conn.commit()
    conn.close()
