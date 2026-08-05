# 🎥 Guion del Video Demostrativo — GG Arena

**Duración objetivo:** 6 a 9 minutos
**Herramienta de grabación sugerida:** Xbox Game Bar (`Win + G`), OBS Studio o Clipchamp
**Destino:** YouTube, con visibilidad **Pública** (o "Oculto/No listado" *solo* si el profesor
lo autoriza; el documento de la tarea exige acceso abierto).

> ✅ Antes de grabar: cierra pestañas personales, silencia notificaciones y verifica que se vea
> bien el texto de la terminal (aumenta el tamaño de fuente con `Ctrl + Shift + +`).

---

## Minuto 0:00 – 0:45 · Presentación

**Qué mostrar:** tu cara o la portada del proyecto (README en GitHub).

> "Buenas, soy [TU NOMBRE], y esta es mi entrega de la Tarea 4: Pruebas Automatizadas con
> Selenium. El proyecto se llama **GG Arena**, un sistema de gestión de torneos de eSports
> que desarrollé como aplicación base, y sobre el cual automaticé **40 escenarios de prueba**
> distribuidos en **5 historias de usuario**, usando **Selenium WebDriver con Python** bajo el
> patrón **Page Object Model**. Aclaro que **no utilicé Selenium IDE**: todo el código de
> pruebas está escrito a mano."

---

## Minuto 0:45 – 2:00 · La aplicación bajo prueba

**Qué mostrar:** el navegador con la app corriendo en `http://127.0.0.1:5055`.

Levántala antes de grabar con:
```bash
python -m app.app --port 5055
```

Recorre en vivo y **narra mientras haces clic**:
1. Pantalla de **login** → entra con `admin` / `Arena2026*`.
2. **Listado de jugadores** → señala el contador y el buscador. Busca "Caribe Titans".
3. **Crear** un jugador → muestra que se agrega a la tabla.
4. **Editar** ese jugador → cambia los puntos.
5. **Eliminar** → muestra el modal de confirmación.
6. Provoca **un error a propósito**: intenta crear un jugador con gamertag repetido.

> "Como ven, la aplicación tiene login y un CRUD completo, con validaciones de negocio.
> Estas validaciones son justamente las que me permiten diseñar pruebas negativas y de límites."

---

## Minuto 2:00 – 3:30 · Las historias de usuario en Jira

**Qué mostrar:** el tablero de Jira con las 5 historias.

1. Muestra el **board** completo con HU-01 a HU-05.
2. Abre **HU-02** y lee en voz alta 2 criterios de aceptación y 2 de rechazo.
3. Señala que cada historia tiene sus casos de prueba asociados.

> "Cada historia documenta sus criterios de aceptación y de rechazo. Por ejemplo, en HU-02
> el criterio de aceptación indica que se debe aceptar un gamertag de 3 a 20 caracteres,
> y el criterio de rechazo indica que 2 o 21 caracteres deben ser rechazados con un mensaje
> claro. Eso es exactamente lo que valida mi prueba de límites."

---

## Minuto 3:30 – 5:00 · El código de las pruebas

**Qué mostrar:** VS Code con el proyecto abierto.

1. **`tests/pages/`** → explica el Page Object Model:
   > "Los localizadores están centralizados en las clases de página. Los tests nunca conocen
   > un `By.ID`; solo llaman acciones de negocio como `iniciar_sesion` o `eliminar`."

2. **`tests/pages/base_page.py`** → señala las esperas explícitas:
   > "Uso `WebDriverWait` con `expected_conditions`, no hay ni un solo `time.sleep`. Además
   > implementé `clic_con_recarga`, que espera a que el documento anterior quede obsoleto
   > antes de validar; eso eliminó las condiciones de carrera que tenía al inicio."

3. **`tests/test_hu02_crear_jugador.py`** → muestra un caso de cada tipo:
   - `test_hu02_registrar_jugador_valido` → **camino feliz**
   - `test_hu02_no_permite_gamertag_duplicado` → **prueba negativa**
   - `test_hu02_acepta_valores_en_el_limite` y `test_hu02_rechaza_valores_fuera_del_limite`
     → **pruebas de límites** (menciona la parametrización con `@pytest.mark.parametrize`)

4. **`tests/conftest.py`** → explica lo que más suma puntos:
   > "El `conftest` levanta y apaga el servidor solo, restaura la base de datos antes de cada
   > escenario para que las pruebas sean independientes, y tiene un hook que captura la
   > pantalla automáticamente al final de cada prueba y la incrusta en el reporte."

---

## Minuto 5:00 – 7:00 · Ejecución en vivo ⭐ *(la parte más importante)*

**Qué mostrar:** la terminal ejecutando la suite **con el navegador visible**.

```bash
pytest
```

- Deja que se vea cómo **Edge se abre solo** y opera la aplicación: escribe, hace clic, navega.
- Narra un par de escenarios mientras corren.
- Espera al resumen final y **muéstralo en pantalla**:
  `40 passed in ...`

> "Aquí se ve Selenium controlando el navegador real: escribe las credenciales, envía el
> formulario, valida los mensajes de error... Al final, los 40 escenarios pasan."

**Opcional (si quieres acortar):** ejecuta solo un subconjunto en vivo y menciona que la
corrida completa está en el reporte:
```bash
pytest tests/test_hu02_crear_jugador.py
```

---

## Minuto 7:00 – 8:30 · Reporte HTML y capturas

**Qué mostrar:** el archivo `reports/reporte_pruebas.html` abierto en el navegador.

1. Muestra el **resumen**: 40 passed, duración, metadatos (proyecto, navegador, patrón).
2. **Expande un escenario** y muestra la **captura incrustada**.
3. Abre la carpeta `reports/capturas/` y desplázate por los **40 PNG numerados**.

> "El reporte se genera automáticamente con pytest-html en modo autocontenido: es un solo
> archivo que se abre en cualquier navegador. Cada escenario incluye su captura de pantalla
> tomada automáticamente, además de guardarse por separado en la carpeta de capturas."

---

## Minuto 8:30 – 9:00 · Cierre

**Qué mostrar:** el repositorio en GitHub.

> "Todo el código, la documentación y las evidencias están en este repositorio público de
> GitHub, y las historias de usuario en el tablero de Jira. Gracias por su tiempo."

---

## ✅ Checklist antes de subir el video

- [ ] Se ve claramente el **navegador siendo controlado por Selenium**
- [ ] Se ve el resumen final `40 passed`
- [ ] Se ve el **reporte HTML** con capturas incrustadas
- [ ] Se ve el **tablero de Jira** con criterios de aceptación y rechazo
- [ ] Se ve el **repositorio de GitHub**
- [ ] El audio se escucha (prueba 10 segundos antes de grabar completo)
- [ ] Subido a **YouTube** en modo **Público**
- [ ] El enlace se abre en una ventana de incógnito (verifica el acceso)
