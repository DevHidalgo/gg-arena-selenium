"""HU-03 | Consulta y busqueda de jugadores (READ del CRUD).

Como administrador de torneos quiero consultar y filtrar el roster
para localizar rapidamente a un participante especifico.
"""
import pytest


@pytest.mark.hu("HU-03")
@pytest.mark.feliz
def test_hu03_listado_muestra_el_roster_completo(sesion_iniciada):
    """Camino feliz: el listado carga todos los jugadores registrados."""
    listado = sesion_iniciada

    assert listado.hay_resultados
    assert listado.total_mostrado == 4
    assert set(listado.gamertags) == {"ShadowRD", "ByteQueen", "NitroDom", "PixelWitch"}


@pytest.mark.hu("HU-03")
@pytest.mark.feliz
@pytest.mark.parametrize(
    "termino, esperados, criterio",
    [
        ("ShadowRD", ["ShadowRD"], "busqueda por gamertag exacto"),
        ("Caribe Titans", ["ByteQueen", "PixelWitch"], "busqueda por equipo"),
        ("Ana", ["ByteQueen"], "busqueda por nombre real"),
    ],
)
def test_hu03_busqueda_devuelve_coincidencias(sesion_iniciada, termino, esperados, criterio):
    """Camino feliz: el buscador filtra por gamertag, nombre real o equipo."""
    listado = sesion_iniciada
    listado.buscar_jugador(termino)

    assert listado.total_mostrado == len(esperados), f"Fallo en {criterio}"
    assert set(listado.gamertags) == set(esperados)


@pytest.mark.hu("HU-03")
@pytest.mark.negativa
def test_hu03_busqueda_sin_coincidencias_muestra_mensaje(sesion_iniciada):
    """Prueba negativa: un termino inexistente no debe romper la vista."""
    listado = sesion_iniciada
    listado.buscar_jugador("JugadorQueNoExiste2026")

    assert not listado.hay_resultados
    assert listado.total_mostrado == 0
    assert "No se encontraron jugadores" in listado.mensaje_sin_resultados


@pytest.mark.hu("HU-03")
@pytest.mark.negativa
def test_hu03_busqueda_con_caracteres_especiales_no_falla(sesion_iniciada):
    """Prueba negativa: entrada con simbolos no debe generar error de servidor."""
    listado = sesion_iniciada
    listado.buscar_jugador("<script>alert(1)</script>")

    assert not listado.hay_resultados
    assert listado.total_mostrado == 0
    assert "GG Arena" in listado.titulo


@pytest.mark.hu("HU-03")
@pytest.mark.limites
@pytest.mark.parametrize(
    "termino, total_esperado, caso",
    [
        ("a", 4, "limite inferior: un solo caracter"),
        ("A" * 60, 0, "limite superior: termino de 60 caracteres"),
    ],
)
def test_hu03_limites_de_longitud_en_la_busqueda(sesion_iniciada, termino, total_esperado, caso):
    """Prueba de limites: longitud minima y maxima del termino de busqueda."""
    listado = sesion_iniciada
    listado.buscar_jugador(termino)

    assert listado.total_mostrado == total_esperado, f"Fallo en {caso}"


@pytest.mark.hu("HU-03")
@pytest.mark.limites
def test_hu03_busqueda_vacia_restaura_el_listado_completo(sesion_iniciada):
    """Prueba de limites: termino vacio (cero caracteres) devuelve todo el roster."""
    listado = sesion_iniciada
    listado.buscar_jugador("NitroDom")
    assert listado.total_mostrado == 1

    listado.limpiar_busqueda()
    assert listado.total_mostrado == 4
