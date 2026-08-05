"""Page Object del listado de jugadores (Read y Delete del CRUD)."""
from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage


class JugadoresPage(BasePage):
    RUTA = "/jugadores"

    TITULO = (By.ID, "titulo-jugadores")
    BTN_NUEVO = (By.ID, "btn-nuevo-jugador")
    INPUT_BUSQUEDA = (By.ID, "input-busqueda")
    BTN_BUSCAR = (By.ID, "btn-buscar")
    BTN_LIMPIAR = (By.ID, "btn-limpiar")
    TOTAL = (By.ID, "total-jugadores")
    TABLA = (By.ID, "tabla-jugadores")
    FILAS = (By.CSS_SELECTOR, '[data-test="fila-jugador"]')
    SIN_RESULTADOS = (By.ID, "sin-resultados")
    MENSAJE_FLASH = (By.ID, "mensaje-flash")
    USUARIO_ACTIVO = (By.ID, "usuario-activo")
    BTN_LOGOUT = (By.ID, "btn-logout")

    MODAL = (By.ID, "modal-eliminar")
    MODAL_TEXTO = (By.ID, "modal-texto")
    BTN_CONFIRMAR_ELIMINAR = (By.ID, "btn-confirmar-eliminar")
    BTN_CANCELAR_ELIMINAR = (By.ID, "btn-cancelar-eliminar")

    def abrir_listado(self):
        return self.abrir(self.RUTA)

    # ------------------------------------------------------------ lectura
    @property
    def total_mostrado(self):
        return int(self.texto_de(self.TOTAL))

    @property
    def gamertags(self):
        return [f.get_attribute("data-gamertag") for f in self.buscar_todos(self.FILAS)]

    def contiene(self, gamertag):
        return gamertag in self.gamertags

    def fila_de(self, gamertag):
        return self.driver.find_element(
            By.CSS_SELECTOR, f'[data-test="fila-jugador"][data-gamertag="{gamertag}"]'
        )

    def datos_de(self, gamertag):
        fila = self.fila_de(gamertag)
        return {
            "gamertag": fila.find_element(By.CLASS_NAME, "col-gamertag").text.strip(),
            "nombre_real": fila.find_element(By.CLASS_NAME, "col-nombre").text.strip(),
            "equipo": fila.find_element(By.CLASS_NAME, "col-equipo").text.strip(),
            "juego": fila.find_element(By.CLASS_NAME, "col-juego").text.strip(),
            "puntos": int(fila.find_element(By.CLASS_NAME, "col-puntos").text.strip()),
        }

    @property
    def hay_resultados(self):
        return self.existe(self.TABLA, tiempo=2)

    @property
    def mensaje_sin_resultados(self):
        return self.texto_de(self.SIN_RESULTADOS)

    @property
    def mensaje_flash(self):
        return self.texto_de(self.MENSAJE_FLASH)

    @property
    def usuario_en_sesion(self):
        return self.texto_de(self.USUARIO_ACTIVO)

    # ---------------------------------------------------------- busqueda
    def buscar_jugador(self, termino):
        self.escribir(self.INPUT_BUSQUEDA, termino)
        self.clic_con_recarga(self.BTN_BUSCAR)
        return self

    def limpiar_busqueda(self):
        self.clic_con_recarga(self.BTN_LIMPIAR)
        return self

    # -------------------------------------------------------- navegacion
    def ir_a_nuevo(self):
        self.clic_con_recarga(self.BTN_NUEVO)
        return self

    def editar(self, gamertag):
        boton = self.fila_de(gamertag).find_element(By.CSS_SELECTOR, '[data-test="btn-editar"]')
        self.clic_elemento_con_recarga(boton)
        return self

    def cerrar_sesion(self):
        self.clic_con_recarga(self.BTN_LOGOUT)
        return self

    # -------------------------------------------------------- eliminacion
    def abrir_modal_eliminar(self, gamertag):
        self.fila_de(gamertag).find_element(By.CSS_SELECTOR, '[data-test="btn-eliminar"]').click()
        self.buscar_visible(self.MODAL)
        return self

    @property
    def modal_visible(self):
        return self.buscar(self.MODAL).is_displayed()

    @property
    def texto_modal(self):
        return self.texto_de(self.MODAL_TEXTO)

    def confirmar_eliminacion(self):
        self.clic_con_recarga(self.BTN_CONFIRMAR_ELIMINAR)
        return self

    def cancelar_eliminacion(self):
        self.clic(self.BTN_CANCELAR_ELIMINAR)
        return self

    def eliminar(self, gamertag):
        self.abrir_modal_eliminar(gamertag)
        return self.confirmar_eliminacion()
