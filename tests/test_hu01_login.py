"""HU-01 | Inicio de sesion en el panel de GG Arena.

Como administrador de torneos quiero iniciar sesion con mis credenciales
para acceder de forma segura al panel de gestion de jugadores.
"""
import pytest

from tests.pages.jugadores_page import JugadoresPage


@pytest.mark.hu("HU-01")
@pytest.mark.feliz
def test_hu01_login_con_credenciales_validas(pagina_login, pagina_jugadores):
    """Camino feliz: credenciales correctas dan acceso al listado de jugadores."""
    pagina_login.iniciar_sesion("admin", "Arena2026*")
    pagina_jugadores.esperar_url_contenga("/jugadores")

    assert "/jugadores" in pagina_jugadores.url_actual
    assert pagina_jugadores.usuario_en_sesion == "Administrador de Torneos"
    assert "Bienvenido" in pagina_jugadores.mensaje_flash
    assert pagina_jugadores.hay_resultados, "El roster debe mostrarse tras el login"


@pytest.mark.hu("HU-01")
@pytest.mark.negativa
@pytest.mark.parametrize(
    "usuario, clave, descripcion",
    [
        ("admin", "ClaveIncorrecta1", "clave incorrecta"),
        ("usuario_inexistente", "Arena2026*", "usuario inexistente"),
    ],
)
def test_hu01_login_con_credenciales_invalidas(pagina_login, usuario, clave, descripcion):
    """Prueba negativa: credenciales invalidas no otorgan acceso."""
    pagina_login.iniciar_sesion(usuario, clave)

    assert pagina_login.hay_error, f"Debe mostrarse un error para: {descripcion}"
    assert "incorrectos" in pagina_login.mensaje_error.lower()
    assert "/login" in pagina_login.url_actual
    assert pagina_login.formulario_visible


@pytest.mark.hu("HU-01")
@pytest.mark.negativa
def test_hu01_acceso_directo_sin_sesion_es_bloqueado(driver, url_base):
    """Prueba negativa: la ruta protegida redirige al login si no hay sesion."""
    pagina = JugadoresPage(driver, url_base).abrir_listado()

    assert "/login" in pagina.url_actual, "Debe redirigir al login"
    assert "iniciar sesion" in pagina.mensaje_flash.lower()


@pytest.mark.hu("HU-01")
@pytest.mark.limites
@pytest.mark.parametrize(
    "usuario, clave, error_esperado",
    [
        ("", "", "obligatorio"),
        ("admin", "", "contrasena es obligatoria"),
        ("", "Arena2026*", "usuario es obligatorio"),
    ],
)
def test_hu01_login_con_campos_en_el_limite_vacio(pagina_login, usuario, clave, error_esperado):
    """Prueba de limites: longitud minima (cero caracteres) en los campos."""
    pagina_login.iniciar_sesion(usuario, clave)

    assert pagina_login.hay_error
    assert error_esperado.lower() in pagina_login.mensaje_error.lower()
    assert "/login" in pagina_login.url_actual
