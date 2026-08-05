"""HU-02 | Registro de un nuevo jugador (CREATE del CRUD).

Como administrador de torneos quiero registrar nuevos jugadores en el roster
para mantener actualizado el listado de participantes del circuito.
"""
import pytest


@pytest.mark.hu("HU-02")
@pytest.mark.feliz
def test_hu02_registrar_jugador_valido(sesion_iniciada, pagina_formulario):
    """Camino feliz: alta de un jugador con todos los datos validos."""
    listado = sesion_iniciada
    total_inicial = listado.total_mostrado

    listado.ir_a_nuevo()
    pagina_formulario.completar(
        gamertag="NovaStrike",
        nombre_real="Pedro Almonte",
        equipo="Cibao Wolves",
        puntos=6200,
        juego="Valorant",
        rango="Diamante",
    ).guardar()

    listado.esperar_url_contenga("/jugadores")
    assert "registrado correctamente" in listado.mensaje_flash
    assert listado.contiene("NovaStrike")
    assert listado.total_mostrado == total_inicial + 1

    registro = listado.datos_de("NovaStrike")
    assert registro["nombre_real"] == "Pedro Almonte"
    assert registro["equipo"] == "Cibao Wolves"
    assert registro["juego"] == "Valorant"
    assert registro["puntos"] == 6200


@pytest.mark.hu("HU-02")
@pytest.mark.negativa
def test_hu02_no_registra_con_campos_obligatorios_vacios(sesion_iniciada, pagina_formulario):
    """Prueba negativa: el formulario vacio muestra todos los errores y no guarda."""
    listado = sesion_iniciada
    total_inicial = listado.total_mostrado

    pagina_formulario.abrir_nuevo().limpiar_campos().guardar()

    assert pagina_formulario.hay_errores
    errores = pagina_formulario.texto_errores
    assert "gamertag es obligatorio" in errores
    assert "nombre real es obligatorio" in errores
    assert "equipo es obligatorio" in errores
    assert "juego valido" in errores
    assert "rango valido" in errores

    listado.abrir_listado()
    assert listado.total_mostrado == total_inicial, "No debe crearse ningun registro"


@pytest.mark.hu("HU-02")
@pytest.mark.negativa
def test_hu02_no_permite_gamertag_duplicado(sesion_iniciada, pagina_formulario):
    """Prueba negativa: el gamertag es unico dentro del roster."""
    listado = sesion_iniciada
    total_inicial = listado.total_mostrado

    pagina_formulario.abrir_nuevo().completar(
        gamertag="ShadowRD",
        nombre_real="Otro Jugador",
        equipo="Equipo Nuevo",
        puntos=100,
        juego="Dota 2",
        rango="Plata",
    ).guardar()

    assert pagina_formulario.hay_errores
    assert "ya esta registrado" in pagina_formulario.texto_errores

    listado.abrir_listado()
    assert listado.total_mostrado == total_inicial


@pytest.mark.hu("HU-02")
@pytest.mark.negativa
def test_hu02_rechaza_gamertag_con_caracteres_no_permitidos(sesion_iniciada, pagina_formulario):
    """Prueba negativa: el gamertag solo admite letras, numeros y guion bajo."""
    pagina_formulario.abrir_nuevo().completar(
        gamertag="Nova Strike!",
        nombre_real="Pedro Almonte",
        equipo="Cibao Wolves",
        puntos=500,
        juego="Valorant",
        rango="Oro",
    ).guardar()

    assert pagina_formulario.hay_errores
    assert "solo admite letras" in pagina_formulario.texto_errores


@pytest.mark.hu("HU-02")
@pytest.mark.limites
@pytest.mark.parametrize(
    "gamertag, puntos, caso",
    [
        ("ABC", 0, "limite inferior: 3 caracteres y 0 puntos"),
        ("A" * 20, 10000, "limite superior: 20 caracteres y 10000 puntos"),
    ],
)
def test_hu02_acepta_valores_en_el_limite(sesion_iniciada, pagina_formulario,
                                          gamertag, puntos, caso):
    """Prueba de limites: los valores frontera validos deben aceptarse."""
    listado = sesion_iniciada

    pagina_formulario.abrir_nuevo().completar(
        gamertag=gamertag,
        nombre_real="Jugador Frontera",
        equipo="QA Testers",
        puntos=puntos,
        juego="Rocket League",
        rango="Bronce",
    ).guardar()

    listado.esperar_url_contenga("/jugadores")
    assert listado.contiene(gamertag), f"Debe aceptar el {caso}"
    assert listado.datos_de(gamertag)["puntos"] == puntos


@pytest.mark.hu("HU-02")
@pytest.mark.limites
@pytest.mark.parametrize(
    "gamertag, puntos, error_esperado",
    [
        ("AB", 500, "al menos 3 caracteres"),
        ("A" * 21, 500, "no puede exceder 20 caracteres"),
        ("LimitePts", 10001, "entre 0 y 10000"),
        ("LimiteNeg", -1, "entre 0 y 10000"),
    ],
)
def test_hu02_rechaza_valores_fuera_del_limite(sesion_iniciada, pagina_formulario,
                                               gamertag, puntos, error_esperado):
    """Prueba de limites: un caracter fuera de la frontera debe rechazarse."""
    listado = sesion_iniciada

    pagina_formulario.abrir_nuevo().completar(
        gamertag=gamertag,
        nombre_real="Jugador Frontera",
        equipo="QA Testers",
        puntos=puntos,
        juego="Rocket League",
        rango="Bronce",
    ).guardar()

    assert pagina_formulario.hay_errores
    assert error_esperado in pagina_formulario.texto_errores

    listado.abrir_listado()
    assert not listado.contiene(gamertag)
