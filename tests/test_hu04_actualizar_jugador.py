"""HU-04 | Actualizacion de los datos de un jugador (UPDATE del CRUD).

Como administrador de torneos quiero editar la informacion de un jugador
para corregir datos y mantener actualizado su puntaje de ranking.
"""
import pytest


@pytest.mark.hu("HU-04")
@pytest.mark.feliz
def test_hu04_actualizar_datos_de_un_jugador(sesion_iniciada, pagina_formulario):
    """Camino feliz: los cambios se persisten y se reflejan en el listado."""
    listado = sesion_iniciada
    listado.editar("NitroDom")

    assert "Editar jugador" in pagina_formulario.titulo_seccion
    assert pagina_formulario.valores_actuales["gamertag"] == "NitroDom"

    pagina_formulario.completar(
        equipo="Duarte Legends",
        puntos=7900,
        rango="Inmortal",
    ).guardar()

    listado.esperar_url_contenga("/jugadores")
    assert "actualizado correctamente" in listado.mensaje_flash

    registro = listado.datos_de("NitroDom")
    assert registro["equipo"] == "Duarte Legends"
    assert registro["puntos"] == 7900


@pytest.mark.hu("HU-04")
@pytest.mark.feliz
def test_hu04_permite_conservar_el_mismo_gamertag(sesion_iniciada, pagina_formulario):
    """Camino feliz: la validacion de unicidad excluye al propio registro."""
    listado = sesion_iniciada
    listado.editar("ByteQueen")

    pagina_formulario.completar(gamertag="ByteQueen", nombre_real="Ana Fermin Diaz").guardar()

    listado.esperar_url_contenga("/jugadores")
    assert "actualizado correctamente" in listado.mensaje_flash
    assert listado.datos_de("ByteQueen")["nombre_real"] == "Ana Fermin Diaz"


@pytest.mark.hu("HU-04")
@pytest.mark.negativa
def test_hu04_no_permite_reutilizar_el_gamertag_de_otro(sesion_iniciada, pagina_formulario):
    """Prueba negativa: no se puede tomar el gamertag de otro jugador."""
    listado = sesion_iniciada
    listado.editar("PixelWitch")

    pagina_formulario.completar(gamertag="ShadowRD").guardar()

    assert pagina_formulario.hay_errores
    assert "ya esta registrado" in pagina_formulario.texto_errores

    listado.abrir_listado()
    assert listado.contiene("PixelWitch"), "El registro original no debe modificarse"


@pytest.mark.hu("HU-04")
@pytest.mark.negativa
def test_hu04_rechaza_puntos_no_numericos(sesion_iniciada, pagina_formulario):
    """Prueba negativa: el campo de puntos solo admite numeros enteros."""
    listado = sesion_iniciada
    listado.editar("ShadowRD")

    pagina_formulario.completar(puntos="mil quinientos").guardar()

    assert pagina_formulario.hay_errores
    assert "numero entero" in pagina_formulario.texto_errores

    listado.abrir_listado()
    assert listado.datos_de("ShadowRD")["puntos"] == 8450


@pytest.mark.hu("HU-04")
@pytest.mark.negativa
def test_hu04_no_permite_vaciar_un_campo_obligatorio(sesion_iniciada, pagina_formulario):
    """Prueba negativa: al editar tampoco se admiten campos obligatorios vacios."""
    listado = sesion_iniciada
    listado.editar("ShadowRD")

    pagina_formulario.completar(equipo="").guardar()

    assert pagina_formulario.hay_errores
    assert "equipo es obligatorio" in pagina_formulario.texto_errores


@pytest.mark.hu("HU-04")
@pytest.mark.limites
@pytest.mark.parametrize(
    "puntos, caso",
    [
        (0, "limite inferior del ranking"),
        (10000, "limite superior del ranking"),
    ],
)
def test_hu04_acepta_puntos_en_los_limites(sesion_iniciada, pagina_formulario, puntos, caso):
    """Prueba de limites: los extremos validos del ranking deben guardarse."""
    listado = sesion_iniciada
    listado.editar("PixelWitch")

    pagina_formulario.completar(puntos=puntos).guardar()

    listado.esperar_url_contenga("/jugadores")
    assert listado.datos_de("PixelWitch")["puntos"] == puntos, f"Fallo en {caso}"


@pytest.mark.hu("HU-04")
@pytest.mark.limites
@pytest.mark.parametrize("puntos", [-1, 10001])
def test_hu04_rechaza_puntos_fuera_de_los_limites(sesion_iniciada, pagina_formulario, puntos):
    """Prueba de limites: un punto fuera de la frontera debe rechazarse."""
    listado = sesion_iniciada
    listado.editar("PixelWitch")

    pagina_formulario.completar(puntos=puntos).guardar()

    assert pagina_formulario.hay_errores
    assert "entre 0 y 10000" in pagina_formulario.texto_errores

    listado.abrir_listado()
    assert listado.datos_de("PixelWitch")["puntos"] == 4180
