"""Page Object de la pantalla de inicio de sesion."""
from selenium.webdriver.common.by import By

from tests.pages.base_page import BasePage


class LoginPage(BasePage):
    RUTA = "/login"

    INPUT_USUARIO = (By.ID, "usuario")
    INPUT_CLAVE = (By.ID, "clave")
    BTN_INGRESAR = (By.ID, "btn-ingresar")
    ERROR_LOGIN = (By.ID, "error-login")
    TITULO = (By.ID, "titulo-login")
    MENSAJE_FLASH = (By.ID, "mensaje-flash")

    def abrir_login(self):
        return self.abrir(self.RUTA)

    def iniciar_sesion(self, usuario, clave):
        self.escribir(self.INPUT_USUARIO, usuario)
        self.escribir(self.INPUT_CLAVE, clave)
        self.clic_con_recarga(self.BTN_INGRESAR)
        return self

    @property
    def mensaje_error(self):
        return self.texto_de(self.ERROR_LOGIN)

    @property
    def hay_error(self):
        return self.existe(self.ERROR_LOGIN)

    @property
    def mensaje_flash(self):
        return self.texto_de(self.MENSAJE_FLASH)

    @property
    def formulario_visible(self):
        return self.existe(self.BTN_INGRESAR)
