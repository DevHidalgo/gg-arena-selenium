"""HU-05 | Eliminacion de un jugador del roster (DELETE del CRUD).

Como administrador de torneos quiero eliminar jugadores con una confirmacion previa
para depurar el roster sin borrar registros por accidente.
"""
import pytest


@pytest.mark.hu("HU-05")
@pytest.mark.feliz
def test_hu05_eliminar_jugador_confirmando(sesion_iniciada):
    """Camino feliz: al confirmar, el jugador desaparece del roster."""
    listado = sesion_iniciada
    total_inicial = listado.total_mostrado

    listado.abrir_modal_eliminar("NitroDom")
    assert listado.modal_visible
    assert "NitroDom" in listado.texto_modal

    listado.confirmar_eliminacion()
    listado.esperar_url_contenga("/jugadores")

    assert "eliminado correctamente" in listado.mensaje_flash
    assert not listado.contiene("NitroDom")
    assert listado.total_mostrado == total_inicial - 1


@pytest.mark.hu("HU-05")
@pytest.mark.negativa
def test_hu05_cancelar_no_elimina_al_jugador(sesion_iniciada):
    """Prueba negativa: cancelar la confirmacion conserva el registro."""
    listado = sesion_iniciada
    total_inicial = listado.total_mostrado

    listado.abrir_modal_eliminar("ByteQueen")
    assert listado.modal_visible

    listado.cancelar_eliminacion()
    assert not listado.modal_visible

    listado.abrir_listado()
    assert listado.contiene("ByteQueen")
    assert listado.total_mostrado == total_inicial


@pytest.mark.hu("HU-05")
@pytest.mark.negativa
def test_hu05_eliminar_un_id_inexistente_muestra_aviso(sesion_iniciada, driver, url_base):
    """Prueba negativa: eliminar un registro inexistente no rompe la aplicacion."""
    listado = sesion_iniciada
    total_inicial = listado.total_mostrado

    driver.execute_script(
        """
        var f = document.createElement('form');
        f.method = 'POST';
        f.action = arguments[0] + '/jugadores/9999/eliminar';
        document.body.appendChild(f);
        f.submit();
        """,
        url_base,
    )
    listado.esperar_url_contenga("/jugadores")

    assert "no existe" in listado.mensaje_flash.lower()
    assert listado.total_mostrado == total_inicial


@pytest.mark.hu("HU-05")
@pytest.mark.limites
def test_hu05_eliminar_todos_deja_el_roster_vacio(sesion_iniciada):
    """Prueba de limites: eliminar hasta el ultimo registro (frontera inferior)."""
    listado = sesion_iniciada

    for gamertag in list(listado.gamertags):
        listado.eliminar(gamertag)
        listado.esperar_url_contenga("/jugadores")

    assert listado.total_mostrado == 0
    assert not listado.hay_resultados
    assert "No se encontraron jugadores" in listado.mensaje_sin_resultados


@pytest.mark.hu("HU-05")
@pytest.mark.limites
def test_hu05_eliminar_el_ultimo_resultado_de_una_busqueda(sesion_iniciada):
    """Prueba de limites: eliminar el unico registro devuelto por un filtro."""
    listado = sesion_iniciada
    listado.buscar_jugador("ShadowRD")
    assert listado.total_mostrado == 1

    listado.eliminar("ShadowRD")
    listado.esperar_url_contenga("/jugadores")

    assert not listado.contiene("ShadowRD")
    assert listado.total_mostrado == 3
