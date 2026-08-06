# Guion del video

Sin narración. Solo mostrar pantalla.

**Antes de grabar:** ejecutar `.\iniciar_app.ps1`

---

### 1. Portada
Abrir `docs\portada.html`.

### 2. La aplicación — http://127.0.0.1:5055
- Login con `admin` / `Arena2026*`
- Buscar `Caribe Titans`
- Crear un jugador nuevo
- Editar sus puntos
- Eliminarlo (mostrar el modal de confirmación)
- Crear otro con el gamertag `ShadowRD` → mostrar el mensaje de error

### 3. Jira
- El tablero con las 5 historias HU-01 a HU-05
- Abrir HU-02 y bajar por: criterios de aceptación, criterios de rechazo, casos de prueba

### 4. El código en VS Code
- `tests\pages\jugadores_page.py`
- `tests\pages\base_page.py`
- `tests\test_hu02_crear_jugador.py`
- `tests\conftest.py`

### 5. Ejecución de las pruebas
- Cerrar la ventana del servidor
- En la terminal: `pytest`
- Mostrar Edge ejecutándose solo
- Mostrar el resultado final: `40 passed`

### 6. Reporte
- Abrir `reports\reporte_pruebas.html`
- Expandir un escenario y mostrar la captura
- Abrir la carpeta `reports\capturas\`

### 7. Cierre
- github.com/DevHidalgo/gg-arena-selenium

---

Subir a YouTube en modo **Público**.
