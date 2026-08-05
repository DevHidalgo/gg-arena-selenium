"""Configuracion global de la suite de pruebas automatizadas de GG Arena.

Responsabilidades:
  * Levantar y apagar la aplicacion bajo prueba (SUT) automaticamente.
  * Restaurar los datos semilla antes de cada prueba (aislamiento).
  * Construir el WebDriver (Edge o Chrome, con o sin modo headless).
  * Capturar automaticamente una pantalla por cada escenario ejecutado
    y adjuntarla al reporte HTML.
"""
import base64
import os
import re
import socket
import subprocess
import sys
import time
from pathlib import Path

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

RAIZ = Path(__file__).resolve().parent.parent
CARPETA_REPORTES = RAIZ / "reports"
CARPETA_CAPTURAS = CARPETA_REPORTES / "capturas"
BD_PRUEBAS = RAIZ / "ggarena_pruebas.db"

CREDENCIALES_VALIDAS = {"usuario": "admin", "clave": "Arena2026*"}

_contador_capturas = {"n": 0}


# ------------------------------------------------------------- opciones CLI
def pytest_addoption(parser):
    parser.addoption("--navegador", action="store", default="edge",
                     help="Navegador a utilizar: edge | chrome")
    parser.addoption("--headless", action="store_true", default=False,
                     help="Ejecutar el navegador sin interfaz grafica")
    parser.addoption("--puerto", action="store", default="5055",
                     help="Puerto en el que se levanta la aplicacion bajo prueba")


def pytest_configure(config):
    CARPETA_CAPTURAS.mkdir(parents=True, exist_ok=True)
    config.addinivalue_line("markers", "hu(id): historia de usuario asociada")
    config.addinivalue_line("markers", "feliz: escenario de camino feliz")
    config.addinivalue_line("markers", "negativa: escenario de prueba negativa")
    config.addinivalue_line("markers", "limites: escenario de prueba de limites")
    try:
        from pytest_metadata.plugin import metadata_key

        config.stash[metadata_key].update({
            "Proyecto": "GG Arena - Gestion de Torneos eSports",
            "Tipo de pruebas": "Automatizadas E2E con Selenium WebDriver",
            "Patron": "Page Object Model (POM)",
            "Navegador": config.getoption("--navegador"),
        })
    except Exception:  # pragma: no cover - metadata es opcional
        pass


def pytest_html_report_title(report):
    report.title = "GG Arena | Reporte de Pruebas Automatizadas con Selenium"


# --------------------------------------------------- aplicacion bajo prueba
def _puerto_libre(puerto):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", int(puerto))) != 0


@pytest.fixture(scope="session")
def url_base(pytestconfig):
    return f"http://127.0.0.1:{pytestconfig.getoption('--puerto')}"


@pytest.fixture(scope="session", autouse=True)
def servidor_web(pytestconfig, url_base):
    """Levanta la aplicacion Flask durante toda la sesion de pruebas."""
    puerto = pytestconfig.getoption("--puerto")

    if not _puerto_libre(puerto):
        pytest.exit(f"El puerto {puerto} ya esta ocupado. Cierre la aplicacion y reintente.")

    if BD_PRUEBAS.exists():
        BD_PRUEBAS.unlink()

    entorno = os.environ.copy()
    entorno["GGARENA_DB"] = str(BD_PRUEBAS)
    entorno["GGARENA_TESTING"] = "1"
    entorno["PYTHONPATH"] = str(RAIZ)

    proceso = subprocess.Popen(
        [sys.executable, "-m", "app.app", "--port", str(puerto)],
        cwd=str(RAIZ),
        env=entorno,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    limite = time.time() + 30
    while time.time() < limite:
        try:
            if requests.get(f"{url_base}/api/health", timeout=1).status_code == 200:
                break
        except requests.RequestException:
            time.sleep(0.4)
    else:
        proceso.terminate()
        pytest.exit("No fue posible iniciar la aplicacion bajo prueba.")

    yield url_base

    proceso.terminate()
    try:
        proceso.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proceso.kill()


@pytest.fixture(autouse=True)
def datos_iniciales(url_base, servidor_web):
    """Restaura la base de datos semilla antes de cada escenario."""
    requests.post(f"{url_base}/api/reset", timeout=5)
    yield


# --------------------------------------------------------------- webdriver
def _construir_driver(navegador, headless):
    if navegador == "chrome":
        opciones = ChromeOptions()
        if headless:
            opciones.add_argument("--headless=new")
        opciones.add_argument("--window-size=1440,900")
        opciones.add_argument("--disable-gpu")
        opciones.add_experimental_option("excludeSwitches", ["enable-logging"])
        return webdriver.Chrome(options=opciones)

    opciones = EdgeOptions()
    if headless:
        opciones.add_argument("--headless=new")
    opciones.add_argument("--window-size=1440,900")
    opciones.add_argument("--disable-gpu")
    opciones.add_argument("--inprivate")
    opciones.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Edge(options=opciones)


@pytest.fixture
def driver(pytestconfig, request):
    navegador = pytestconfig.getoption("--navegador").lower()
    headless = pytestconfig.getoption("--headless")

    navegador_web = _construir_driver(navegador, headless)
    navegador_web.set_window_size(1440, 900)
    navegador_web.set_page_load_timeout(30)

    request.node._driver = navegador_web
    yield navegador_web
    navegador_web.quit()


# ------------------------------------------------------------ page objects
@pytest.fixture
def pagina_login(driver, url_base):
    from tests.pages.login_page import LoginPage

    return LoginPage(driver, url_base).abrir_login()


@pytest.fixture
def pagina_jugadores(driver, url_base):
    from tests.pages.jugadores_page import JugadoresPage

    return JugadoresPage(driver, url_base)


@pytest.fixture
def pagina_formulario(driver, url_base):
    from tests.pages.formulario_page import FormularioPage

    return FormularioPage(driver, url_base)


@pytest.fixture
def sesion_iniciada(pagina_login, pagina_jugadores):
    """Deja al usuario autenticado y posicionado en el listado de jugadores."""
    pagina_login.iniciar_sesion(**CREDENCIALES_VALIDAS)
    pagina_jugadores.esperar_url_contenga("/jugadores")
    return pagina_jugadores


# ------------------------------------------- capturas automaticas + reporte
def _nombre_archivo(nodeid, indice):
    limpio = re.sub(r"[^A-Za-z0-9_.-]+", "_", nodeid.split("::")[-1])
    return f"{indice:02d}_{limpio[:80]}.png"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    resultado = yield
    reporte = resultado.get_result()

    if reporte.when != "call":
        return

    navegador_web = getattr(item, "_driver", None)
    if navegador_web is None:
        return

    pytest_html = item.config.pluginmanager.getplugin("html")
    extras = getattr(reporte, "extras", [])

    try:
        _contador_capturas["n"] += 1
        nombre = _nombre_archivo(item.nodeid, _contador_capturas["n"])
        destino = CARPETA_CAPTURAS / nombre
        captura_b64 = navegador_web.get_screenshot_as_base64()
        destino.write_bytes(base64.b64decode(captura_b64))

        if pytest_html is not None:
            extras.append(pytest_html.extras.image(captura_b64, name=f"Captura: {nombre}"))
            extras.append(pytest_html.extras.url(navegador_web.current_url, name="URL final"))
        reporte.extras = extras
    except Exception as error:  # pragma: no cover
        print(f"[conftest] No se pudo capturar la pantalla: {error}")
