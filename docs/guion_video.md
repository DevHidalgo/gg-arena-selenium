# 🎥 Guion del Video Demostrativo — GG Arena

**Modalidad: SIN NARRACIÓN.** El video solo muestra pantalla; no hace falta hablar.
Por eso el orden y las pausas son lo importante: si nadie explica, el video tiene que
explicarse solo.

**Duración objetivo:** 5 a 7 minutos
**Grabación:** Xbox Game Bar (`Win + G` → botón de grabar) o Clipchamp
**Destino:** YouTube en modo **Público**

---

## ⚙️ Preparación (haz esto ANTES de grabar)

1. **Cierra** pestañas personales, Discord, WhatsApp y silencia notificaciones
   (`Win + A` → *Asistencia a la concentración / No molestar*)
2. Abre estas **5 pestañas en el navegador, en este orden**:
   1. `docs\portada.html` *(doble clic sobre el archivo)*
   2. `http://127.0.0.1:5055` — la aplicación
   3. El tablero de Jira
   4. `reports\reporte_pruebas.html`
   5. `https://github.com/DevHidalgo/gg-arena-selenium`
3. Abre **VS Code** con el proyecto y aumenta la fuente: `Ctrl + Shift + P` → *"Editor Font Zoom In"* (2 o 3 veces)
4. Abre una **terminal** y aumenta la fuente con `Ctrl + Shift + +` (4 o 5 veces — debe leerse en pantalla completa)
5. Levanta la aplicación en una terminal aparte:
   ```
   .\iniciar_app.ps1
   ```

> 🔑 **Regla de oro sin narración:** en cada pantalla importante, **quédate quieto 4-5 segundos**
> antes de pasar a la siguiente. Quien evalúa necesita tiempo para leer. Mueve el mouse despacio
> y **señala con el cursor** lo que quieres que se vea.

---

## 🎬 Escena 1 · Portada — 15 segundos

Muestra `docs/portada.html` a pantalla completa (`F11`).

Ya contiene todo lo que dirías hablando: nombre del proyecto, la tarea, 5 historias,
40 escenarios, el índice de la demostración y las tecnologías. **Déjala fija 15 segundos.**

---

## 🎬 Escena 2 · La aplicación bajo prueba — 90 segundos

Pestaña `http://127.0.0.1:5055`. Haz este recorrido **despacio**:

| Acción | Pausa |
|---|---|
| Pantalla de login → escribe `admin` / `Arena2026*` → Ingresar | 3 s |
| Listado de jugadores: señala con el cursor el contador y la tabla | 4 s |
| Escribe `Caribe Titans` en el buscador → Buscar | 4 s |
| Limpiar → clic en **+ Nuevo jugador** | 2 s |
| Llena el formulario y registra un jugador | 4 s |
| Clic en **Editar** de ese jugador → cambia los puntos → Guardar | 4 s |
| Clic en **Eliminar** → **deja el modal de confirmación visible** | 4 s |
| Confirma la eliminación | 3 s |
| **Provoca un error:** Nuevo jugador → gamertag `ShadowRD` (repetido) → Registrar | 5 s |

⚠️ Ese último paso es clave: muestra las validaciones que justifican las pruebas negativas.

---

## 🎬 Escena 3 · Historias de usuario en Jira — 60 segundos

| Acción | Pausa |
|---|---|
| Tablero completo con las 5 historias HU-01 a HU-05 | 5 s |
| Clic en **HU-02** para abrir el detalle | 2 s |
| **Baja despacio** por los Criterios de aceptación | 6 s |
| **Baja despacio** por los Criterios de rechazo | 6 s |
| Baja hasta los Casos de prueba automatizados | 5 s |
| Vuelve al tablero y abre **HU-05** brevemente | 5 s |

---

## 🎬 Escena 4 · El código de las pruebas — 90 segundos

En VS Code, abre estos archivos en orden y **desplázate despacio**:

1. **`tests/pages/jugadores_page.py`** — el Page Object Model: los localizadores viven aquí, no en los tests *(10 s)*
2. **`tests/pages/base_page.py`** — señala con el cursor `WebDriverWait`, `expected_conditions` y el método `clic_con_recarga` *(15 s)*
3. **`tests/test_hu02_crear_jugador.py`** — recorre los 3 tipos de prueba y **detente en cada uno**: *(30 s)*
   - `test_hu02_registrar_jugador_valido` → camino feliz
   - `test_hu02_no_permite_gamertag_duplicado` → prueba negativa
   - `test_hu02_rechaza_valores_fuera_del_limite` → prueba de límites
4. **`tests/conftest.py`** — señala el hook `pytest_runtest_makereport` que captura la pantalla automáticamente *(15 s)*

> 💡 Los nombres de los tests y los docstrings ya dicen en español qué hace cada uno.
> Sin narración, eso es justamente lo que se lee en pantalla.

---

## 🎬 Escena 5 · Ejecución en vivo — 2 minutos ⭐ *(la más importante)*

Es el requisito central: *"el video debe mostrar claramente la ejecución de las pruebas"*.

En la terminal grande, ejecuta **con el navegador visible** (no headless):

```
pytest
```

- Deja que se vea **Edge abriéndose solo** y operando la aplicación: escribe, hace clic, navega
- Graba al menos **60-90 segundos** de ejecución real
- Puedes cortar en edición y saltar al final, pero **muestra el resumen**:
  `40 passed in ...`
- **Detente 6 segundos** sobre el resumen final

**Si prefieres un video más corto**, ejecuta solo una historia y luego enseña el reporte
completo en la Escena 6:
```
pytest tests/test_hu02_crear_jugador.py
```

---

## 🎬 Escena 6 · Reporte HTML y capturas — 60 segundos

| Acción | Pausa |
|---|---|
| Abre `reports/reporte_pruebas.html` — muestra el resumen **40 passed** | 5 s |
| Muestra los metadatos (proyecto, navegador, patrón POM) | 4 s |
| **Expande un escenario** y muestra la captura incrustada | 6 s |
| Expande otro de tipo negativo (se ve el mensaje de error) | 5 s |
| Abre la carpeta `reports\capturas\` en vista **Iconos grandes** y desplázate por los 40 PNG | 8 s |

---

## 🎬 Escena 7 · Cierre — 20 segundos

| Acción | Pausa |
|---|---|
| El repositorio en GitHub: muestra el README | 6 s |
| Baja hasta la tabla de cobertura de pruebas | 5 s |
| Muestra la carpeta `tests/` del repositorio | 5 s |
| Vuelve a `docs/portada.html` para cerrar | 5 s |

---

## ✅ Checklist antes de subir

- [ ] Se ve el **navegador siendo controlado por Selenium** (lo más importante)
- [ ] Se ve el resumen final **`40 passed`**
- [ ] Se ve el **reporte HTML** con capturas incrustadas
- [ ] Se ve el **tablero de Jira** con criterios de aceptación y rechazo
- [ ] Se ve el **repositorio de GitHub**
- [ ] No aparecen datos personales ni pestañas ajenas al proyecto
- [ ] Subido a **YouTube** en modo **Público**
- [ ] Verificado el enlace en una **ventana de incógnito**

> 📝 **Sobre la narración:** el documento de la tarea solo exige que el video *"muestre
> claramente la ejecución de las pruebas automatizadas"*. No pide audio. Si más adelante
> quieres narrarlo, cada escena de arriba ya lleva el orden y el foco que necesitarías.
