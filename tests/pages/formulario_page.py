"""Page Object del formulario de jugadores (Create y Update del CRUD)."""
from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage


class FormularioPage(BasePage):
    RUTA_NUEVO = "/jugadores/nuevo"

    TITULO = (By.ID, "titulo-formulario")
    INPUT_GAMERTAG = (By.ID, "gamertag")
    INPUT_NOMBRE = (By.ID, "nombre_real")
    INPUT_EQUIPO = (By.ID, "equipo")
    INPUT_PUNTOS = (By.ID, "puntos")
    SELECT_JUEGO = (By.ID, "juego")
    SELECT_RANGO = (By.ID, "rango")
    BTN_GUARDAR = (By.ID, "btn-guardar")
    BTN_CANCELAR = (By.ID, "btn-cancelar")
    CAJA_ERRORES = (By.ID, "errores-formulario")
    ITEMS_ERROR = (By.CSS_SELECTOR, '[data-test="error-item"]')

    def abrir_nuevo(self):
        return self.abrir(self.RUTA_NUEVO)

    def completar(self, gamertag=None, nombre_real=None, equipo=None,
                  puntos=None, juego=None, rango=None):
        if gamertag is not None:
            self.escribir(self.INPUT_GAMERTAG, gamertag)
        if nombre_real is not None:
            self.escribir(self.INPUT_NOMBRE, nombre_real)
        if equipo is not None:
            self.escribir(self.INPUT_EQUIPO, equipo)
        if puntos is not None:
            self.escribir(self.INPUT_PUNTOS, str(puntos))
        if juego is not None:
            self.seleccionar(self.SELECT_JUEGO, juego)
        if rango is not None:
            self.seleccionar(self.SELECT_RANGO, rango)
        return self

    def limpiar_campos(self):
        for localizador in (self.INPUT_GAMERTAG, self.INPUT_NOMBRE,
                            self.INPUT_EQUIPO, self.INPUT_PUNTOS):
            self.buscar_visible(localizador).clear()
        return self

    def guardar(self):
        self.clic_con_recarga(self.BTN_GUARDAR)
        return self

    def cancelar(self):
        self.clic_con_recarga(self.BTN_CANCELAR)
        return self

    # ------------------------------------------------------------ estado
    @property
    def hay_errores(self):
        return self.existe(self.CAJA_ERRORES, tiempo=3)

    @property
    def errores(self):
        return [e.text.strip() for e in self.buscar_todos(self.ITEMS_ERROR)]

    @property
    def texto_errores(self):
        return " | ".join(self.errores)

    @property
    def titulo_seccion(self):
        return self.texto_de(self.TITULO)

    @property
    def valores_actuales(self):
        return {
            "gamertag": self.valor_de(self.INPUT_GAMERTAG),
            "nombre_real": self.valor_de(self.INPUT_NOMBRE),
            "equipo": self.valor_de(self.INPUT_EQUIPO),
            "puntos": self.valor_de(self.INPUT_PUNTOS),
        }
