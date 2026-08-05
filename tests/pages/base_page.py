"""Clase base del patron Page Object Model.

Centraliza las esperas explicitas y las interacciones comunes para que las
paginas concretas solo declaren sus localizadores y acciones de negocio.
"""
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

TIEMPO_ESPERA = 10


class BasePage:
    def __init__(self, driver, url_base):
        self.driver = driver
        self.url_base = url_base
        self.espera = WebDriverWait(driver, TIEMPO_ESPERA)

    # ------------------------------------------------------- navegacion
    def abrir(self, ruta=""):
        self.driver.get(f"{self.url_base}{ruta}")
        return self

    @property
    def url_actual(self):
        return self.driver.current_url

    @property
    def titulo(self):
        return self.driver.title

    # ------------------------------------------------------ interaccion
    def buscar(self, localizador):
        return self.espera.until(EC.presence_of_element_located(localizador))

    def buscar_visible(self, localizador):
        return self.espera.until(EC.visibility_of_element_located(localizador))

    def buscar_todos(self, localizador):
        return self.driver.find_elements(*localizador)

    def clic(self, localizador):
        self.espera.until(EC.element_to_be_clickable(localizador)).click()

    # --------------------------------------------- sincronizacion de cargas
    def _ancla(self):
        """Referencia al documento actual para detectar la recarga de pagina."""
        return self.driver.find_element(By.TAG_NAME, "html")

    def esperar_recarga(self, ancla):
        """Espera a que el documento anterior quede obsoleto (staleness)."""
        self.espera.until(EC.staleness_of(ancla))
        self.espera.until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    def clic_con_recarga(self, localizador):
        """Hace clic en un elemento que provoca una navegacion completa."""
        ancla = self._ancla()
        self.clic(localizador)
        self.esperar_recarga(ancla)

    def clic_elemento_con_recarga(self, elemento):
        ancla = self._ancla()
        elemento.click()
        self.esperar_recarga(ancla)

    def escribir(self, localizador, texto):
        campo = self.buscar_visible(localizador)
        campo.clear()
        campo.send_keys(texto)

    def seleccionar(self, localizador, valor):
        Select(self.buscar_visible(localizador)).select_by_visible_text(valor)

    def texto_de(self, localizador):
        return self.buscar_visible(localizador).text.strip()

    def valor_de(self, localizador):
        return self.buscar(localizador).get_attribute("value")

    def existe(self, localizador, tiempo=3):
        try:
            WebDriverWait(self.driver, tiempo).until(
                EC.presence_of_element_located(localizador)
            )
            return True
        except TimeoutException:
            return False

    def esperar_url_contenga(self, fragmento):
        self.espera.until(EC.url_contains(fragmento))
        return self
