# 🎮 GG Arena — Pruebas Automatizadas con Selenium

**Tarea 4 · Pruebas Automatizadas** — Automatización de pruebas end-to-end sobre una
aplicación web con operaciones **CRUD** y **login**, implementadas con **Selenium WebDriver**
en **Python** bajo el patrón **Page Object Model**.

> ⚠️ Este proyecto **no** utiliza Selenium IDE. Todo el código de pruebas está escrito a mano
> con la librería `selenium` de Python y el framework `pytest`.

---

## 📌 Enlaces de la entrega

| Entregable | Enlace |
|---|---|
| 🟢 Repositorio de código | *(este repositorio)* |
| 🟡 Tablero de historias de usuario (Jira) | https://devhidalgo-qa.atlassian.net/jira/software/projects/SCRUM/boards/1 |
| 🔵 Video demostrativo (YouTube) | `PENDIENTE_YOUTUBE` |
| 📄 Reporte HTML de ejecución | [`reports/reporte_pruebas.html`](reports/reporte_pruebas.html) |
| 📸 Capturas automáticas | [`reports/capturas/`](reports/capturas) |

---

## 🧩 Aplicación bajo prueba (SUT)

**GG Arena** es un sistema de gestión de torneos de eSports desarrollado para este proyecto
(Flask + SQLite). Incluye:

- **Autenticación** con sesión y protección de rutas.
- **CRUD completo** sobre el roster de jugadores: crear, listar/buscar, actualizar y eliminar.
- **Validaciones de negocio** que hacen posibles las pruebas negativas y de límites:
  - Gamertag: obligatorio, único, de **3 a 20** caracteres, solo `A-Z a-z 0-9 _`.
  - Nombre real: obligatorio, máximo 60 caracteres.
  - Equipo: obligatorio, máximo 40 caracteres.
  - Puntos de ranking: entero entre **0 y 10000**.
- Modal de confirmación propio para la eliminación (no se usa `window.confirm`).

### Credenciales de acceso

| Usuario | Contraseña | Rol |
|---|---|---|
| `admin` | `Arena2026*` | Administrador de Torneos |
| `arbitro` | `Referee2026*` | Árbitro Oficial |

---

## 🧪 Cobertura de pruebas

**40 escenarios automatizados** distribuidos en **5 historias de usuario**, cada una con
casos de **camino feliz**, **prueba negativa** y **prueba de límites**.

| Historia | Descripción | Camino feliz | Negativa | Límites | Total |
|---|---|:---:|:---:|:---:|:---:|
| HU-01 | Inicio de sesión | 1 | 3 | 3 | 7 |
| HU-02 | Registrar jugador *(Create)* | 1 | 3 | 6 | 10 |
| HU-03 | Consultar y buscar *(Read)* | 4 | 2 | 3 | 9 |
| HU-04 | Actualizar jugador *(Update)* | 2 | 3 | 4 | 9 |
| HU-05 | Eliminar jugador *(Delete)* | 1 | 2 | 2 | 5 |
| | **Total** | **9** | **13** | **18** | **40** |

El detalle de cada historia, con sus **criterios de aceptación y rechazo**, está en
[`docs/historias_usuario.md`](docs/historias_usuario.md) y registrado en el tablero de Jira.

---

## 🏗️ Arquitectura del proyecto

```
gg-arena-selenium/
├── app/                          # Aplicación bajo prueba (SUT)
│   ├── app.py                    # Rutas Flask y control de sesión
│   ├── database.py               # Acceso a datos SQLite y datos semilla
│   ├── validaciones.py           # Reglas de negocio (base de pruebas negativas/límites)
│   ├── templates/                # Vistas: login, listado y formulario
│   └── static/estilos.css
├── tests/
│   ├── conftest.py               # Fixtures: servidor, WebDriver, capturas automáticas
│   ├── pages/                    # ← Page Object Model
│   │   ├── base_page.py          # Esperas explícitas y acciones comunes
│   │   ├── login_page.py
│   │   ├── jugadores_page.py
│   │   └── formulario_page.py
│   ├── test_hu01_login.py
│   ├── test_hu02_crear_jugador.py
│   ├── test_hu03_consultar_jugadores.py
│   ├── test_hu04_actualizar_jugador.py
│   └── test_hu05_eliminar_jugador.py
├── docs/
│   ├── historias_usuario.md      # Historias con criterios de aceptación y rechazo
│   └── guion_video.md            # Guion del video demostrativo
├── reports/
│   ├── reporte_pruebas.html      # Reporte HTML autocontenido
│   └── capturas/                 # 40 capturas automáticas (una por escenario)
├── pytest.ini
└── requirements.txt
```

### Decisiones técnicas destacadas

- **Page Object Model**: los localizadores viven en las clases de página, nunca en los tests.
- **Esperas explícitas** (`WebDriverWait` + `expected_conditions`); **cero** `time.sleep()`.
- **Sincronización por *staleness***: `clic_con_recarga()` espera a que el documento anterior
  quede obsoleto antes de validar, eliminando falsos negativos por condiciones de carrera.
- **Aislamiento total**: la base de datos se restaura a su estado semilla **antes de cada
  escenario** mediante el endpoint `/api/reset` (solo activo en modo pruebas).
- **Ciclo de vida automatizado**: la suite **levanta y apaga** el servidor Flask por sí misma;
  no hace falta arrancar la aplicación a mano.
- **Localizadores estables**: la interfaz expone atributos `id` y `data-test` dedicados.
- **Capturas automáticas**: un hook de pytest toma una captura al final de **cada** escenario
  y la incrusta en el reporte HTML.

---

## ▶️ Cómo ejecutar

### 1. Requisitos previos
- Python 3.10 o superior
- Microsoft Edge o Google Chrome instalado
  *(el driver se descarga solo con Selenium Manager, no se requiere configuración manual)*

### 2. Instalación

```bash
git clone https://github.com/DevHidalgo/gg-arena-selenium.git
cd gg-arena-selenium

python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Linux / macOS

pip install -r requirements.txt
```

### 3. Ejecutar toda la suite

```bash
pytest
```

Esto levanta la aplicación, ejecuta los 40 escenarios, guarda las capturas en
`reports/capturas/` y genera `reports/reporte_pruebas.html`.

### 4. Variantes de ejecución

```bash
pytest --headless                  # sin abrir ventana del navegador
pytest --navegador=chrome          # usar Google Chrome (por defecto: edge)
pytest -m feliz                    # solo caminos felices
pytest -m negativa                 # solo pruebas negativas
pytest -m limites                  # solo pruebas de límites
pytest tests/test_hu02_crear_jugador.py -v     # una sola historia
```

### 5. Levantar solo la aplicación (demo manual)

```bash
python -m app.app --port 5055
```
Luego abrir <http://127.0.0.1:5055>.

---

## 📊 Reporte y evidencias

El reporte se genera con **pytest-html** en modo `--self-contained-html`: es **un solo
archivo** que puede abrirse en cualquier navegador sin dependencias externas.

Incluye por cada escenario: resultado, duración, historia de usuario asociada, tipo de prueba,
**captura de pantalla incrustada** y la URL final del navegador.

Además, las capturas se guardan de forma independiente en `reports/capturas/` numeradas en
orden de ejecución (`01_...png` a `40_...png`).

**Última ejecución: 40 escenarios, 40 exitosos, 0 fallidos.**

---

## 🛠️ Tecnologías

| Herramienta | Uso |
|---|---|
| Python 3.12 | Lenguaje de implementación |
| Selenium WebDriver 4.46 | Automatización del navegador |
| pytest 8.3 | Framework de pruebas y parametrización |
| pytest-html 4.1 | Reporte HTML con evidencias |
| Flask 3.0 + SQLite | Aplicación bajo prueba |
| Microsoft Edge / Chrome | Navegadores soportados |
