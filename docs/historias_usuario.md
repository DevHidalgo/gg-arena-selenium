# Historias de Usuario — GG Arena

> **Documento de trabajo.** El registro oficial de estas historias vive en el tablero de
> **Jira** (ver enlace en el README). Este archivo existe únicamente para facilitar la
> carga de la información en el tablero y mantener la trazabilidad con el código.

Proyecto: **GG Arena — Sistema de Gestión de Torneos eSports**
Tipo de pruebas: automatizadas end-to-end con **Selenium WebDriver + pytest**

---

## HU-01 — Inicio de sesión

**Como** administrador de torneos
**quiero** iniciar sesión con mi usuario y contraseña
**para** acceder de forma segura al panel de gestión de jugadores.

### ✅ Criterios de aceptación
1. Dado un usuario registrado, cuando ingresa usuario y contraseña válidos y presiona *Ingresar*, entonces el sistema lo redirige a `/jugadores`.
2. El encabezado muestra el nombre del usuario autenticado y el botón *Cerrar sesión*.
3. Se muestra el mensaje de bienvenida con el nombre del usuario.
4. El listado de jugadores se carga completo después del acceso.

### ❌ Criterios de rechazo
1. Si la contraseña es incorrecta, se muestra "Usuario o contraseña incorrectos" y **no** se otorga acceso.
2. Si el usuario no existe, se muestra el mismo mensaje genérico (no se revela si el usuario existe).
3. Si el campo usuario o contraseña está vacío, se muestra el mensaje "El usuario es obligatorio" / "La contraseña es obligatoria".
4. Si un visitante sin sesión abre `/jugadores` directamente, es redirigido a `/login` con el aviso "Debe iniciar sesión para acceder al panel".

### 🧪 Casos de prueba automatizados — `tests/test_hu01_login.py`
| # | Caso | Tipo |
|---|------|------|
| CP-01 | `test_hu01_login_con_credenciales_validas` | Camino feliz |
| CP-02 | `test_hu01_login_con_credenciales_invalidas[clave incorrecta]` | Negativa |
| CP-03 | `test_hu01_login_con_credenciales_invalidas[usuario inexistente]` | Negativa |
| CP-04 | `test_hu01_acceso_directo_sin_sesion_es_bloqueado` | Negativa |
| CP-05 | `test_hu01_login_con_campos_en_el_limite_vacio` (3 variantes) | Límites |

---

## HU-02 — Registrar un nuevo jugador *(CREATE)*

**Como** administrador de torneos
**quiero** registrar nuevos jugadores en el roster
**para** mantener actualizado el listado de participantes del circuito.

### ✅ Criterios de aceptación
1. El formulario permite capturar gamertag, nombre real, equipo, juego, rango y puntos.
2. Al guardar datos válidos, el sistema muestra "Jugador '<gamertag>' registrado correctamente" y regresa al listado.
3. El nuevo jugador aparece en la tabla con todos sus datos y el contador aumenta en 1.
4. Se acepta un gamertag de **3 caracteres** (mínimo) y de **20 caracteres** (máximo).
5. Se aceptan **0** puntos (mínimo) y **10000** puntos (máximo).

### ❌ Criterios de rechazo
1. Si algún campo obligatorio está vacío, se listan los errores y **no** se crea el registro.
2. Si el gamertag ya existe, se muestra "El gamertag '<valor>' ya está registrado".
3. Si el gamertag contiene espacios o símbolos, se muestra "El gamertag solo admite letras, números y guion bajo".
4. Si el gamertag tiene **2** o **21** caracteres, se rechaza indicando el límite.
5. Si los puntos son **-1** o **10001**, se muestra "Los puntos deben estar entre 0 y 10000".

### 🧪 Casos de prueba automatizados — `tests/test_hu02_crear_jugador.py`
| # | Caso | Tipo |
|---|------|------|
| CP-06 | `test_hu02_registrar_jugador_valido` | Camino feliz |
| CP-07 | `test_hu02_no_registra_con_campos_obligatorios_vacios` | Negativa |
| CP-08 | `test_hu02_no_permite_gamertag_duplicado` | Negativa |
| CP-09 | `test_hu02_rechaza_gamertag_con_caracteres_no_permitidos` | Negativa |
| CP-10 | `test_hu02_acepta_valores_en_el_limite` (2 variantes) | Límites |
| CP-11 | `test_hu02_rechaza_valores_fuera_del_limite` (4 variantes) | Límites |

---

## HU-03 — Consultar y buscar jugadores *(READ)*

**Como** administrador de torneos
**quiero** consultar y filtrar el roster
**para** localizar rápidamente a un participante específico.

### ✅ Criterios de aceptación
1. Al entrar al panel se muestran todos los jugadores registrados ordenados por puntos (descendente).
2. El contador "Jugadores encontrados" refleja el total exacto de filas mostradas.
3. La búsqueda filtra por **gamertag**, **nombre real** o **equipo** de forma parcial y sin distinguir mayúsculas.
4. El botón *Limpiar* restaura el listado completo.

### ❌ Criterios de rechazo
1. Si el término no coincide con ningún registro, se muestra "No se encontraron jugadores que coincidan con la búsqueda" y el contador queda en 0.
2. Si el término contiene caracteres especiales o etiquetas HTML, la aplicación **no** debe fallar ni ejecutar código (el contenido se escapa).
3. Un término de longitud extrema (60 caracteres) devuelve 0 resultados sin errores de servidor.

### 🧪 Casos de prueba automatizados — `tests/test_hu03_consultar_jugadores.py`
| # | Caso | Tipo |
|---|------|------|
| CP-12 | `test_hu03_listado_muestra_el_roster_completo` | Camino feliz |
| CP-13 | `test_hu03_busqueda_devuelve_coincidencias` (3 variantes) | Camino feliz |
| CP-14 | `test_hu03_busqueda_sin_coincidencias_muestra_mensaje` | Negativa |
| CP-15 | `test_hu03_busqueda_con_caracteres_especiales_no_falla` | Negativa |
| CP-16 | `test_hu03_limites_de_longitud_en_la_busqueda` (2 variantes) | Límites |
| CP-17 | `test_hu03_busqueda_vacia_restaura_el_listado_completo` | Límites |

---

## HU-04 — Actualizar los datos de un jugador *(UPDATE)*

**Como** administrador de torneos
**quiero** editar la información de un jugador
**para** corregir sus datos y mantener actualizado su puntaje de ranking.

### ✅ Criterios de aceptación
1. El botón *Editar* abre el formulario precargado con los datos actuales del jugador.
2. Al guardar cambios válidos se muestra "Jugador '<gamertag>' actualizado correctamente".
3. Los cambios se reflejan de inmediato en la tabla del listado.
4. El jugador puede conservar su propio gamertag sin que la validación de unicidad lo bloquee.
5. Se aceptan los valores frontera del ranking: **0** y **10000** puntos.

### ❌ Criterios de rechazo
1. Si se intenta usar el gamertag de **otro** jugador, se muestra "ya está registrado" y no se guarda.
2. Si el campo puntos no es numérico, se muestra "Los puntos deben ser un número entero" y el valor original se conserva.
3. Si se vacía un campo obligatorio, se muestra el error correspondiente y no se guarda.
4. Si los puntos son **-1** o **10001**, se rechaza y el valor original permanece intacto.

### 🧪 Casos de prueba automatizados — `tests/test_hu04_actualizar_jugador.py`
| # | Caso | Tipo |
|---|------|------|
| CP-18 | `test_hu04_actualizar_datos_de_un_jugador` | Camino feliz |
| CP-19 | `test_hu04_permite_conservar_el_mismo_gamertag` | Camino feliz |
| CP-20 | `test_hu04_no_permite_reutilizar_el_gamertag_de_otro` | Negativa |
| CP-21 | `test_hu04_rechaza_puntos_no_numericos` | Negativa |
| CP-22 | `test_hu04_no_permite_vaciar_un_campo_obligatorio` | Negativa |
| CP-23 | `test_hu04_acepta_puntos_en_los_limites` (2 variantes) | Límites |
| CP-24 | `test_hu04_rechaza_puntos_fuera_de_los_limites` (2 variantes) | Límites |

---

## HU-05 — Eliminar un jugador del roster *(DELETE)*

**Como** administrador de torneos
**quiero** eliminar jugadores con una confirmación previa
**para** depurar el roster sin borrar registros por accidente.

### ✅ Criterios de aceptación
1. El botón *Eliminar* abre un modal de confirmación que menciona el gamertag afectado.
2. Al confirmar, se muestra "Jugador '<gamertag>' eliminado correctamente" y la fila desaparece.
3. El contador de jugadores disminuye en 1.
4. Es posible eliminar todos los registros hasta dejar el roster vacío, mostrando el mensaje de listado vacío.

### ❌ Criterios de rechazo
1. Si el usuario presiona *Cancelar*, el modal se cierra y el jugador **permanece** en el roster.
2. Si se intenta eliminar un identificador inexistente, la aplicación muestra "El jugador solicitado no existe" sin romperse ni alterar el total.

### 🧪 Casos de prueba automatizados — `tests/test_hu05_eliminar_jugador.py`
| # | Caso | Tipo |
|---|------|------|
| CP-25 | `test_hu05_eliminar_jugador_confirmando` | Camino feliz |
| CP-26 | `test_hu05_cancelar_no_elimina_al_jugador` | Negativa |
| CP-27 | `test_hu05_eliminar_un_id_inexistente_muestra_aviso` | Negativa |
| CP-28 | `test_hu05_eliminar_todos_deja_el_roster_vacio` | Límites |
| CP-29 | `test_hu05_eliminar_el_ultimo_resultado_de_una_busqueda` | Límites |

---

## Resumen de cobertura

| Historia | Camino feliz | Negativa | Límites | Total escenarios |
|----------|:---:|:---:|:---:|:---:|
| HU-01 Login | 1 | 3 | 3 | 7 |
| HU-02 Crear | 1 | 3 | 6 | 10 |
| HU-03 Consultar | 4 | 2 | 3 | 9 |
| HU-04 Actualizar | 2 | 3 | 4 | 9 |
| HU-05 Eliminar | 1 | 2 | 2 | 5 |
| **Total** | **9** | **13** | **18** | **40** |
