
# Proyecto Sistemas Linux Embebebidos — Videojuegos 2D

## Autores

  * Ismael Cortes Ramirez 
  * Juan Esteban Agreda Gutierrez
---
Repositorio del proyecto de la asignatura *Sistemas Embebidos en Linux*. Contiene ejemplos y versiones optimizadas de dos juegos 2D desarrollados en Python + Pygame:

- `Juego_1/` — plataforma 2D (versión Pygame y opcionalmente OpenGL).
- `Juego_2/` — shooter tipo Space War (meteoritos, barra de escudo y marcador).
- `Juego_Menu/` — (opcional) interfaz para lanzar los juegos desde un menú común.

El repositorio está preparado para ejecutarse en entornos Linux, WSL2 (con WSLg o servidor X) y sistemas embebidos con entorno gráfico.

---

## Índice rápido
- **Descripción** — ¿qué contiene el proyecto?
- **Estructura** — árbol de carpetas relevante
- **Requerimientos** — hardware, software y desempeño
- **Instalación** — pasos para preparar el entorno
- **Ejecución** — cómo lanzar cada juego
- **Optimización & notas técnicas** — decisiones relevantes
- **Problemas conocidos** — limitaciones actuales, bugs o advertencias de hardware
- **Plan de Verificación** — metodología de pruebas y resultados de benchmarking
- **Contribuir** — cómo ayudar o probar cambios
- **Explicación Técnica: Juego 1** — renderizado OpenGL y *batch processing*
- **Explicación Técnica: Juego 2** — gestión de sprites, POO y robustez
- **Explicación Técnica: Menú** — aislamiento de procesos y ciclo de vida
- **Licencia**

---

## Estructura del repositorio
```
Proyecto_Sistemas_Linux_Embebidos/
├── Juego_1/         # Plataforma 2D (Pygame + opcional OpenGL)
├── Juego_2/         # Shooter Space War (Pygame)
├── Juego_Menu/      # (opcional) menú para lanzar los juegos
├── venv/            # entorno virtual (opcional)
└── README.md        # este documento
```

Dentro de cada `Juego_X/` encontrarás archivos clave: `main.py`, `funciones.py`, `settings.py`, `utils.py`, y carpetas `Textturas/` y `Sounds/` con recursos.

---

## Requerimientos

### Requerimientos de software
* **Python:** 3.10 o superior (probado en 3.12 y 3.13).
* **Librerías necesarias:**
    * `pygame`
    * `psutil`
    * (Opcional) `PyOpenGL` y `PyOpenGL_accelerate` para la versión OpenGL del Juego 1.
* **Sistema operativo:**
    * Linux con entorno gráfico X11 o Wayland.
    * WSL2 con WSLg (o servidor X externo).
    * Compatible con sistemas embebidos con soporte para Pygame (como BeaglePlay / BeagleBone con Weston, X11 o SDL2).

**Dependencias rápidas:**
```bash
pip install pygame psutil
# Opcional OpenGL:
pip install PyOpenGL PyOpenGL_accelerate
```

### Requerimientos de hardware
* CPU: x86_64, ARMv8 o ARMv7 moderna.

* GPU: Dedicada no necesaria (aunque ayuda).

* Memoria mínima recomendada:

  * PC: 2 GB RAM.

  * SBC (BeagleBone/BeaglePlay): 1 GB RAM.

* Pantalla: Resolución ≥ 640×360 (los juegos se adaptan, pero se recomienda ≥ 720p).

### Requerimientos de funcionamiento (EXIGENCIAS DE DESEMPEÑO)
Para cumplir los objetivos del curso Sistemas Embebidos en Linux, el proyecto debe cumplir los siguientes requisitos de rendimiento:

* 1\. Mejora de rendimiento:

  * El juego optimizado debe alcanzar al menos +10 FPS adicionales respecto a la versión base/no optimizada.

* 2\. Técnicas de optimización aplicadas:

  * Reducción de carga de render (uso de convert_alpha(), escalado previo, reducción de blits innecesarios).

  * Uso eficiente de grupos de sprites (pygame.sprite.Group).

  * Control de spawn y límites de entidades.

  * Optimización de lectura de reloj (pygame.time.get_ticks()).

  * Eliminación de cálculos redundantes o dentro de bucles críticos.

* 3\. Estabilidad (FPS mínimos):

  * El menú de selección y los juegos deben poder ejecutarse de forma estable.

  * ≥ 30 FPS mínimos en BeaglePlay/BeagleBone con Weston.

  * ≥ 45 FPS mínimos en PC.

* 4\. Robustez:

  * El juego debe ser capaz de ejecutarse sin errores aun cuando no haya audio disponible (p. ej. en WSL o hardware sin soporte ALSA).

---

## Instalación (rápida)

```bash
git clone https://github.com/sillHD/Proyecto_Sistemas_Linux_Embebidos.git
cd Proyecto_Sistemas_Linux_Embebidos
python3 -m venv venv         # opcional pero recomendado
source venv/bin/activate
pip install --upgrade pip
pip install pygame psutil
```

En Windows (sin WSL):

```powershell
python -m venv venv
venv\Scripts\activate
pip install pygame psutil
```

---

## Cómo ejecutar

- Juego 1 (Pygame):

```bash
cd Juego_1
python main.py
```

- Juego 1 (OpenGL, si disponible):

```bash
python main_opl.py
```

- Juego 2 (Space War):

```bash
cd Juego_2
python main.py
```

- Menú (si está implementado):

```bash
cd Juego_Menu
python menu.py
```

Controles y detalles de cada juego están en sus respectivos `README.md` dentro de `Juego_1/` y `Juego_2/`.

---

## Optimización y notas técnicas

- **Rutas relativas:** todos los juegos usan `settings.ruta()` para construir rutas portables a recursos.
- **Control de sprites:** límite de creación de proyectiles (cooldown con `pygame.time.get_ticks()`) para evitar saturar la CPU.
- **Grupos de sprites:** uso de `pygame.sprite.Group` para actualizaciones y render eficiente.
- **Monitor de recursos:** `utils.py` muestra CPU (via `psutil`) y, si es accesible, una estimación de GPU (`/sys/class/drm/...`).

---

## Problemas conocidos

- **Audio:** en algunos entornos  `pygame.mixer.init()` puede fallar. El código captura esta excepción y continúa sin sonido:

```py
try:
    pygame.mixer.init()
except pygame.error:
    print("Advertencia: audio no disponible, se continúa sin sonido.")
```

## Plan de Verificación

Este plan describe las pruebas necesarias para validar que el proyecto cumple con los requisitos funcionales y de rendimiento, específicamente en el contexto de sistemas embebidos.

### 1. Pruebas de Rendimiento (Benchmarking)
**Objetivo:** Verificar la mejora de FPS y la estabilidad del *framerate*.

| ID | Prueba | Procedimiento | Criterio de Aceptación |
| :--- | :--- | :--- | :--- |
| **P-01** | **Línea Base (No Optimizado)** | Ejecutar `game_base.py` (versión sin optimizar) durante 60 segundos con carga media de enemigos. | Registrar FPS promedio inicial (ej. 25 FPS). |
| **P-02** | **Versión Optimizada** | Ejecutar `game_optimized.py` en las mismas condiciones que P-01. | **FPS Promedio ≥ (FPS Base + 10)**. |
| **P-03** | **Estabilidad Embebida** | Ejecutar en BeaglePlay/BeagleBone por 5 minutos continuos. | El juego no baja de **30 FPS** en ningún momento crítico. |
| **P-04** | **Estabilidad PC** | Ejecutar en PC (Linux/WSL) por 2 minutos. | El juego se mantiene sobre **45 FPS**. |

### 2. Pruebas de Recursos (Hardware)
**Objetivo:** Asegurar que el juego no exceda las capacidades de la SBC (Single Board Computer).

* **Herramienta de monitoreo:** `htop` o módulo interno `psutil`.
* **Procedimiento:**
    1.  Iniciar el juego.
    2.  Navegar por el menú y entrar al Juego 1.
    3.  Monitorear el consumo de memoria RAM y CPU.

**Criterios de éxito:**
- [ ] **RAM:** El consumo total del proceso no supera 500 MB (dejando margen para el SO en dispositivos de 1GB).
- [ ] **CPU:** El uso de CPU no se mantiene al 100% de forma sostenida (evitar *thermal throttling*).

### 3. Pruebas de Robustez y Compatibilidad
**Objetivo:** Verificar el comportamiento ante fallos de hardware o configuraciones limitadas.

#### A. Ausencia de Audio
* **Escenario:** Entorno sin servidor de audio (WSL por defecto o driver ALSA deshabilitado).
* **Comando de prueba:**
    ```bash
    export SDL_AUDIODRIVER=dummy
    python3 main.py
    ```
* **Resultado esperado:** El juego inicia, se puede jugar y cerrar sin lanzar excepciones (`Crash-free`). Se muestra advertencia en consola pero no detiene la ejecución.

#### B. Adaptabilidad de Resolución
* **Escenario:** Pantallas pequeñas o redimensionamiento de ventana.
* **Procedimiento:** Forzar resolución de 640x360 o redimensionar la ventana manualmente.
* **Resultado esperado:** Los elementos de la UI (Puntaje, Menú) permanecen visibles y no se superponen.

### 4. Lista de Chequeo Final (Release)
Antes de la entrega o despliegue en la tarjeta, confirmar:

- [ ] Todas las rutas de archivos (imágenes/sonidos) son relativas (no absolutas tipo `C:/Users/...`).
- [ ] El juego cierra correctamente al presionar `ESC` o cerrar la ventana (liberación de recursos `pygame.quit()`).
- [ ] Los permisos de ejecución están configurados (`chmod +x main.py`).

---

## Resultados de la Verificación

Tras la ejecución de las pruebas definidas en el plan de verificación, se confirma que el proyecto ha cumplido con la **mayoría de los objetivos críticos**, garantizando la jugabilidad y la fluidez. Sin embargo, se observaron desviaciones en el consumo de recursos.

### ✅ Objetivos Cumplidos
* **Mejora de FPS:** La versión optimizada supera el umbral de **+10 FPS** de ganancia respecto a la versión base.
* **Estabilidad de Cuadros:** Se mantienen los **30 FPS** mínimos en sistemas embebidos (BeaglePlay) y **45 FPS** en PC.
* **Robustez:** El sistema maneja correctamente la ausencia de dispositivos de audio y adaptaciones de resolución sin *crashes*.

### ⚠️ Objetivos No Cumplidos
* **Consumo de Recursos (CPU y RAM):**
    * No se logró mantener el consumo de memoria y uso de CPU bajo los mínimos ideales establecidos.
    * **Observación:** Las técnicas de optimización aplicadas (como el pre-escalado de sprites y el caché de superficies) priorizaron la velocidad de renderizado (FPS), lo que resultó en un aumento del uso de memoria RAM y una carga de CPU sostenida mayor a la esperada en la SBC.

---

## Explicación del Código: `main.py` (Juego 1)

Esta sección explica la estructura y las **optimizaciones clave** implementadas en el *loop* principal del Juego 1, que utiliza **OpenGL** directamente para el renderizado, logrando una alta eficiencia gráfica.

-----

### 1\. Inicialización y Configuración de OpenGL

Esta es la sección más crítica y la que define la optimización de bajo nivel, **delegando el renderizado a la GPU**.

| Bloque | Propósito | Puntos Clave |
| :--- | :--- | :--- |
| **`pygame.display.set_mode`** | Configura la ventana y el contexto. | Se usa el *flag* `OPENGL` para que Pygame cree un **contexto OpenGL** en lugar de usar su renderizador SDL estándar. `DOUBLEBUF` ayuda a evitar el *tearing*. |
| **`glMatrixMode(GL_PROJECTION)`** | Define cómo las coordenadas 2D se mapean a la pantalla. | La función `glOrtho(0, ANCHO_P, ALTO_P, 0, -1, 1)` es crucial. **Mapea las coordenadas de Pygame (origen superior izquierdo, Y crece hacia abajo) directamente al contexto OpenGL**. Esto simplifica el código de juego al no tener que invertir la coordenada Y. |
| **`glEnable(GL_BLEND)`** | Habilita la **transparencia**. | Esencial para que las texturas con canal alfa (`.png` con transparencias) se dibujen correctamente. |
| **`glDisable(GL_DEPTH_TEST)`** | Deshabilita la prueba de profundidad. | Al ser un juego 2D, el orden de dibujo es gestionado por el código, no por la coordenada Z. |

-----

### 2\. Carga y Gestión de Texturas

Las texturas se cargan una única vez fuera del *loop* principal, convirtiendo las superficies de Pygame directamente en objetos de textura de OpenGL.

  * **`load_texture_from_surface(surface)`:** Convierte una superficie de Pygame (previamente cargada con `.convert_alpha()`) en un **Texture ID (Identificador de Textura)** dentro del contexto de OpenGL. Devuelve un *tuple* `(tex_id, width, height)`.
  * **Listas de Texturas:** Las animaciones (`walk_right_tex`, `jump_left_tex`, etc.) se almacenan como **listas de *tuples* de OpenGL**, lo que permite acceder rápidamente al `tex_id` y las dimensiones para el *batch rendering*.

-----

### 3\. El Loop Principal y la Optimización `draw_queue`

El *loop* principal (`while bin == 0`) gestiona la lógica del juego y el renderizado, implementando una técnica de optimización clave: **Batch Rendering (Dibujado por Lotes)**.

#### A. Lógica Central

  * **`cooldown_timer`:** Implementa un período de **invencibilidad** de 1 segundo (60 *frames*) tras recibir daño, simplificando la lógica de colisión.
  * **Movimiento de Salto:** Se utiliza una función trigonométrica `pn_y = base_y - math.sin(angulo) * 200` para un movimiento parabólico suave.
  * **Culling Básico:** En el segmento de las Nubes, se incluye un **culling básico** (`if -tex[1] <= x <= ANCHO_P:`) para encolar el dibujo solo si el objeto está visible en la pantalla.

#### B. Implementación de Batch Rendering (Optimización Principal)

Esta técnica minimiza la llamada OpenGL más costosa: **`glBindTexture()`**.

1.  **`draw_queue = {}` (Estructura de Datos):** Al inicio de cada *frame*, se inicializa un diccionario que mapea el `Texture ID` a una lista de *quads* (rectángulos) que deben dibujarse usando esa textura.
2.  **`enqueue_draw(...)` (Encolar):** Todas las entidades llaman a esta función para añadir sus coordenadas a la lista correspondiente de su `tex_id`.
3.  **`FLUSH` / `draw_batch()` (Dibujar por Lotes):**
    ```python
    # ---- FLUSH: dibujar por textura (reduce glBindTexture)
    for tex_id, quads in draw_queue.items():
        draw_batch(tex_id, quads)
    ```
    El código llama a **`glBindTexture(tex_id)`** **una sola vez** por cada textura única, e inmediatamente después llama a **`draw_batch(tex_id, quads)`** (definida en `funciones.py`) para dibujar **todos** los rectángulos (`quads`) que usan esa textura en una sola operación GPU. Esto reduce drásticamente las llamadas al *driver* gráfico y acelera el renderizado.

-----

### 4\. Animaciones

Las animaciones utilizan el **contador de *frames*** (`frame_counter`) para seleccionar el *frame* de la lista de texturas pre-cargadas.

  * **Animación de Caminar:** `idx = (frame_counter // 3) % len(walk_left_tex)`. El operador `// 3` reduce la velocidad de la animación (cambia de *frame* cada 3 *frames* del juego), mientras que el módulo (`%`) asegura el *loop* cíclico.
  * **Animación de Salto:** La selección del *frame* (`idx`) está sincronizada con la variable **`angulo`** del salto (`int(angulo / step)`), asegurando que la animación coincida con la altura del jugador.

---

Aquí tienes la explicación técnica detallada para el **Juego 2 (Space War)**. A diferencia del primero (que usaba OpenGL), este se enfoca en optimizaciones nativas de **Pygame** y **Programación Orientada a Objetos (POO)**.

---

### 5\. Codigo

```python
# main.py (adaptado para usar funciones OpenGL desde funciones.py)
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
from settings import *
from funciones import *   # contiene load_texture_from_surface, draw_texture_tuple, walking_animation_textures, jumping_animation_textures, draw_hp_bar_gl, draw_batch

# =======================
# CONFIG VENTANA
# =======================
ANCHO_P, ALTO_P = 1280, 720
FPS = 60

pygame.init()
pygame.display.set_mode((ANCHO_P, ALTO_P), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Juego OpenGL - Optimizado")

# =======================
# OPENGL SETUP
# =======================
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
# Mantengo la proyección tal como tenías (0..ANCHO_P, 0..ALTO_P)
# Usar origen en la esquina superior izquierda para que Y crezca hacia abajo.
# Esto hace que coordenadas como `base_y = 580` sitúen al jugador cerca
# del borde inferior de la ventana, como en coordenadas de Pygame.
glOrtho(0, ANCHO_P, ALTO_P, 0, -1, 1)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

glEnable(GL_TEXTURE_2D)
glEnable(GL_BLEND)  # Habilitar transparencia
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Configurar blending
glDisable(GL_DEPTH_TEST)

# -----------------------
# Wrappers / aliases para mantener tus llamadas
# -----------------------
# load_texture en tu código original devolvía (tex_id, w, h). Nuestra función se llama load_texture_from_surface.
load_texture = load_texture_from_surface

# draw_texture en tu código original recibía (tex_id, x, y, w, h)
def draw_texture(tex_id, x, y, w, h, offset=(0,0)):
    """Dibuja una textura dado su tex_id y tamaño (w,h)."""
    # Reutilizamos draw_texture_tuple que espera (tex_tuple, ...)
    draw_texture_tuple((tex_id, w, h), x, y, w, h, offset=offset)

# Animaciones (alias a las funciones GPU)
walking_animation = walking_animation_textures
jumping_animation = jumping_animation_textures

# Wrapper para mantener el nombre draw_shield_bar_gl que usas en main,
# pero internamente llamamos a draw_hp_bar_gl(x, y, width, height, value, max_value)
def draw_shield_bar_gl(x, y, pct):
    # pct ya está en 0..100, convertimos a value,max_value
    draw_hp_bar_gl(x, y, 200, 20, pct, 100)


# =======================
# CARGAR TEXTURAS
# =======================
# load_texture returns (tex_id, w, h)
fondo_img = pygame.image.load(ruta("texturas", "background.png")).convert_alpha()
fondo_tex = load_texture_from_surface(fondo_img)
stayR_tex = load_texture_from_surface(
    pygame.image.load(ruta("texturas", "stay_right.png")).convert_alpha()
)

stayL_tex = load_texture_from_surface(
    pygame.image.load(ruta("texturas", "stay_left.png")).convert_alpha()
)


walk_right_tex = [
    load_texture_from_surface(
        pygame.image.load(ruta("texturas", "walk", "right", f"run_r{i}.png")).convert_alpha()
    )
    for i in range(1, 9)
]

walk_left_tex = [
    load_texture_from_surface(
        pygame.image.load(ruta("texturas", "walk", "left", f"run_l{i}.png")).convert_alpha()
    )
    for i in range(1, 9)
]

jump_right_tex = [
    load_texture_from_surface(
        pygame.image.load(ruta("texturas", "jump", "jump_right", f"jump_r{i}.png")).convert_alpha()
    )
    for i in range(1, 9)
]

jump_left_tex = [
    load_texture_from_surface(
        pygame.image.load(ruta("texturas", "jump", "jump_left", f"jump_l{i}.png")).convert_alpha()
    )
    for i in range(1, 9)
]

clouds_tex = [
    load_texture_from_surface(
        pygame.image.load(ruta("texturas", "clouds", f"c{i}.png")).convert_alpha()
    )
    for i in range(1, 4)
]
enemy_left_tex = [
    load_texture_from_surface(
        pygame.image.load(ruta("texturas", "enemy", "left", f"e_l{i}.png")).convert_alpha()
    )
    for i in range(1, 4)
]

enemy_right_tex = [
    load_texture_from_surface(
        pygame.image.load(ruta("texturas", "enemy", "right", f"e_r{i}.png")).convert_alpha()
    )
    for i in range(1, 4)
]


# =======================
# FUNCIÓN DE COLISIÓN
# =======================
def check_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    """Detecta colisión entre dos rectángulos"""
    return (x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2)

# =======================
# VARIABLES JUGADOR
# =======================
base_y = 580
pn_x, pn_y = 640, base_y
vn_x = 0
velocidad = 5
angulo = 0
direccion = -1
frame_counter = 0
player_width = 60  # Ancho aproximado del jugador
player_height = 80  # Alto aproximado del jugador
player_health = 100
bin = 0
cooldown_timer = 0  # invencibilidad restante en frames (0 = vulnerable)

# =======================
# NUBES
# Estructura: [x, y, tex_tuple, speed, frame_counter_for_texture]
# =======================
cloud_positions = [
    [800, 60, random.choice(clouds_tex), random.randint(1, 3), 0],
    [300, 60, random.choice(clouds_tex), random.randint(1, 3), 0],
    [1100, 60, random.choice(clouds_tex), random.randint(1, 3), 0],
]

# =======================
# ENEMIGOS
# =======================
pe_x1, pe_y1 = -60, 600
pe_x2, pe_y2 = 1224, 600
ve1, ve2 = random.randint(3, 6), random.randint(3, 6)

clock = pygame.time.Clock()

# Helper: cola de dibujado por textura
def enqueue_draw(draw_queue, tex_tuple, x, y, w=None, h=None, offset=(0,0)):
    tex_id, tw, th = tex_tuple
    if w is None: w = tw
    if h is None: h = th
    ox, oy = offset
    draw_queue.setdefault(tex_id, []).append((ox + x, oy + y, w, h))

# =======================
# LOOP PRINCIPAL
# =======================
while bin == 0:
    # actualizar cooldown (decrementar por frame)
    if cooldown_timer > 0:
        cooldown_timer -= 1

    clock.tick(FPS)
    glClear(GL_COLOR_BUFFER_BIT)

    # reset draw queue cada frame
    draw_queue = {}

    # ---- EVENTOS ----
    for event in pygame.event.get():
        if event.type == QUIT:
            bin = 1
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                bin = 1
            if event.key == K_RIGHT:
                vn_x = velocidad
            if event.key == K_LEFT:
                vn_x = -velocidad
            if event.key == K_UP and angulo == 0:
                angulo = 0.001
        if event.type == KEYUP:
            if event.key in (K_RIGHT, K_LEFT):
                # corregimos direccion según última entrada
                direccion = -1 if event.key == K_RIGHT else 1
                vn_x = 0

    # ---- MOVIMIENTO JUGADOR ----
    pn_x += vn_x
    if angulo > 0:
        pn_y = base_y - math.sin(angulo) * 200
        angulo += 0.1
        if angulo >= math.pi:
            angulo = 0
            pn_y = base_y
    else:
        pn_y = base_y

    # Mantener dentro de pantalla
    pn_x = max(0, min(ANCHO_P - 60, pn_x))

    # ---- FONDO ----
    # fondo_tex es (tex_id,w,h)
    enqueue_draw(draw_queue, fondo_tex, 0, 0, ANCHO_P, ALTO_P)

    # ---- NUBES ----
    for cloud in cloud_positions:
        x, y, tex, speed, fc = cloud  # Desempaquetar velocidad y contador
        # dibujar solo si visible (optimización)
        if -tex[1] <= x <= ANCHO_P:
            enqueue_draw(draw_queue, tex, x, y, tex[1], tex[2])

        # Actualizar posición de la nube (moviéndose hacia la izquierda)
        cloud[0] -= speed

        # Cambiar textura de la nube cada cierto tiempo (solo una vez cada 30 frames)
        cloud[4] += 1
        if cloud[4] >= 30:
            cloud[2] = random.choice(clouds_tex)
            cloud[4] = 0

        # Reiniciar posición de la nube
        if cloud[0] < -200:
            cloud[0] = ANCHO_P + 100

    # ---- ENEMIGOS ----
    # obtenemos tamaño del enemigo desde la primera textura
    enemy_width = enemy_right_tex[0][1]
    enemy_height = enemy_right_tex[0][2]

    pe_x1 += ve1
    # dibujar solo si visible
    if -enemy_width <= pe_x1 <= ANCHO_P:
        # escogemos frame por frame_counter
        tex_idx = (frame_counter // 10) % 3
        tex_tuple = enemy_right_tex[tex_idx]
        enqueue_draw(draw_queue, tex_tuple, pe_x1, pe_y1, tex_tuple[1], tex_tuple[2])
    if pe_x1 > ANCHO_P + 60:
        pe_x1 = -60

    pe_x2 -= ve2
    if -enemy_width <= pe_x2 <= ANCHO_P:
        tex_idx = (frame_counter // 10) % 3
        tex_tuple = enemy_left_tex[tex_idx]
        enqueue_draw(draw_queue, tex_tuple, pe_x2, pe_y2, tex_tuple[1], tex_tuple[2])
    if pe_x2 < -60:
        pe_x2 = ANCHO_P + 60

    # ---- COLISIONES ----
    if (check_collision(pn_x, pn_y, player_width, player_height, pe_x1, pe_y1, enemy_width, enemy_height)
        or check_collision(pn_x, pn_y, player_width, player_height, pe_x2, pe_y2, enemy_width, enemy_height)):
        if cooldown_timer == 0:
            player_health -= 10  # Restar 10 de vida
            cooldown_timer = FPS  # 1 segundo de invencibilidad
        if player_health <= 0:
            break  # Terminar juego

    # ---- JUGADOR ----
    if vn_x < 0:
        if angulo == 0:
            # usar animación GPU (lista de tuples) -> encolar frame
            idx = (frame_counter // 3) % len(walk_left_tex)
            tex_tuple = walk_left_tex[idx]
            enqueue_draw(draw_queue, tex_tuple, pn_x, pn_y, tex_tuple[1], tex_tuple[2])
        else:
            # animación salto: elegir frame por ángulo
            step = math.pi / len(jump_left_tex)
            idx = min(int(angulo / step), len(jump_left_tex) - 1)
            tex_tuple = jump_left_tex[idx]
            enqueue_draw(draw_queue, tex_tuple, pn_x, pn_y, tex_tuple[1], tex_tuple[2])
    elif vn_x > 0:
        if angulo == 0:
            idx = (frame_counter // 3) % len(walk_right_tex)
            tex_tuple = walk_right_tex[idx]
            enqueue_draw(draw_queue, tex_tuple, pn_x, pn_y, tex_tuple[1], tex_tuple[2])
        else:
            step = math.pi / len(jump_right_tex)
            idx = min(int(angulo / step), len(jump_right_tex) - 1)
            tex_tuple = jump_right_tex[idx]
            enqueue_draw(draw_queue, tex_tuple, pn_x, pn_y, tex_tuple[1], tex_tuple[2])
    else:
        tex = stayL_tex if direccion == 1 else stayR_tex
        enqueue_draw(draw_queue, tex, pn_x, pn_y, tex[1], tex[2])

    # ---- FLUSH: dibujar por textura (reduce glBindTexture)
    for tex_id, quads in draw_queue.items():
        draw_batch(tex_id, quads)

    # ---- BARRA DE VIDA (dibujar al final para que no se borre) ----
    pct = max(0, min(100, player_health))  # asegurar 0..100
    # dibujamos con la función OpenGL de HP (usa 200x20 por defecto en el wrapper)
    draw_shield_bar_gl(50, 50, pct)

    pygame.display.flip()
    frame_counter += 1

pygame.quit()

```

---

## 🚀 Explicación del Código: `main.py` (Juego 2)

Esta sección detalla la arquitectura del **Juego 2**, el cual está construido utilizando el motor de renderizado 2D nativo de Pygame. El enfoque principal aquí es la **robustez** (manejo de errores) y la **gestión eficiente de Sprites**.

***

### 1. Robustez y Compatibilidad (Hardware/Audio)

Uno de los requisitos clave del proyecto es que funcione en entornos limitados (WSL, servidores sin audio, SBCs). Para lograr esto, se implementó un sistema de "Fallbacks" (alternativas seguras).

| Bloque | Propósito | Explicación Técnica |
| :--- | :--- | :--- |
| **Bloques `try...except` en Audio** | **Evitar Crashes** | En lugar de detener el programa si no se detecta una tarjeta de sonido (común en WSL o Docker), el juego captura la excepción `pygame.error`, marca `AUDIO_AVAILABLE = False` y continúa ejecutándose en modo silencio. |
| **Carga segura de Fondo** | **Continuidad Visual** | Si la imagen de fondo falla al cargar, el juego no se cierra; en su lugar, genera dinámicamente una superficie negra (`background.fill(BLACK)`). |

```python
# Ejemplo de manejo robusto de audio
try:
    pygame.mixer.init()
    AUDIO_AVAILABLE = True
except pygame.error:
    print("Advertencia: audio no disponible, se continúa sin sonido.")
    AUDIO_AVAILABLE = False
````

-----

### 2\. Optimización de Recursos Gráficos

A diferencia de OpenGL donde usamos texturas en GPU, en Pygame nativo la optimización clave está en el formato de las superficies en la RAM.

  * **`.convert()`:** Todas las imágenes cargadas (fondo y meteoritos) llaman a este método.
      * *¿Por qué?* Convierte la imagen al mismo formato de píxeles que la pantalla (display). Si no se hace, Pygame debe convertir la imagen **en cada frame** al dibujarla, lo que desploma los FPS.
  * **`.set_colorkey(BLACK)`:** Se utiliza para la transparencia. Es más rápido de procesar para la CPU antigua de algunos sistemas embebidos que el canal Alpha completo por píxel (`convert_alpha()`), aunque ofrece bordes un poco más duros.

-----

### 3\. Gestión de Entidades (Sprite Groups)

El juego utiliza intensivamente la clase `pygame.sprite.Group` para manejar cientos de interacciones sin código espagueti.

  * **`all_sprites`:** Contiene todas las entidades (jugador, meteoritos, láseres). Permite llamar a `all_sprites.update()` y `all_sprites.draw(screen)` una sola vez por frame, delegando la lógica a cada objeto.
  * **`meteor_list` y `lasers`:** Son subgrupos específicos usados exclusivamente para cálculos de colisiones, evitando iterar sobre objetos innecesarios (como el jugador o partículas de fondo).

-----

### 4\. Lógica de Colisiones Eficiente

Pygame ofrece funciones optimizadas en C para detectar choques entre grupos, que son mucho más rápidas que usar bucles `for` anidados en Python.

#### A. Láser vs Meteoritos (`groupcollide`)

```python
hits = pygame.sprite.groupcollide(meteor_list, lasers, True, True)
```

  * **Mecánica:** Compara todos los meteoritos contra todos los láseres.
  * **`True, True`:** Los argumentos booleanos indican que, al chocar, **ambos** objetos (el meteorito y el láser) deben eliminarse automáticamente de la memoria y de la pantalla. Esto gestiona la limpieza de memoria automáticamente.

#### B. Jugador vs Meteoritos (`spritecollide`)

```python
hits = pygame.sprite.spritecollide(player, meteor_list, True)
```

  * **Mecánica:** Compara un solo objeto (jugador) contra un grupo.
  * **Sistema de Escudo:** Al detectar colisión, no termina el juego inmediatamente. Resta energía (`player.shield -= 25`) y elimina el meteorito. El "Game Over" solo ocurre cuando el escudo llega a 0.

-----

### 5\. Ciclo de "Reciclaje" (Spawn)

Para mantener el juego infinito sin llenar la memoria, cada vez que un meteorito es destruido (por láser o choque), se crea uno nuevo inmediatamente:

```python
meteor = Meteor(meteor_images)
all_sprites.add(meteor)
meteor_list.add(meteor)
```

Esto asegura que siempre haya una cantidad constante de enemigos en pantalla (9 en este caso), manteniendo la carga de CPU predecible y estable.


Aquí tienes la explicación técnica del **Menú Principal**. Este script actúa como un "Hub" o lanzador centralizado. Su arquitectura es interesante porque no importa módulos, sino que gestiona **procesos del sistema operativo**, lo cual es ideal para aislar errores entre juegos.

---

### 6\. Codigo

```python
# main.py - Space War optimizado tomando ideas de Juego_1
import pygame
import random
print(">>> MAIN EJECUTADO DESDE:", __file__)

from settings import *
from funciones import *
from utils import monitor_usage   # monitor de CPU/GPU

# ============================================================
# INICIALIZACIÓN
# ============================================================
pygame.init()

# Intentar iniciar el audio, pero no morir si no hay dispositivo (WSL, etc.)
try:
    pygame.mixer.init()
    AUDIO_AVAILABLE = True
except pygame.error:
    print("Advertencia: audio no disponible, se continúa sin sonido.")
    AUDIO_AVAILABLE = False

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Space War")
clock = pygame.time.Clock()
FPS = 60

# ============================================================
# CARGAR RECURSOS
# ============================================================
# Imágenes de meteoritos
meteor_images = []
meteor_list_files = [
    "Meteorito1.png", "Meteorito3.png", "Meteorito4.png",
    "Meteorito5.png", "Meteorito6.png", "Meteorito7.png",
    "Meteorito2.png", "Ovni.png"
]

for img in meteor_list_files:
    try:
        meteor_img = pygame.image.load(ruta('Textturas', img)).convert()
        meteor_img.set_colorkey(BLACK)
        meteor_images.append(meteor_img)
    except pygame.error as e:
        print(f"Error cargando {img}: {e}")

# Fondo
try:
    background = pygame.image.load(ruta('Textturas', 'Fondo2.png')).convert()
except pygame.error as e:
    print(f"Error cargando fondo: {e}")
    # En caso de fallo, fondo negro
    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill(BLACK)

# Sonidos
laser_sound = None
explosion_sound = None

if AUDIO_AVAILABLE:
    try:
        laser_sound = pygame.mixer.Sound(ruta('Sounds', 'Lasersound.ogg'))
        explosion_sound = pygame.mixer.Sound(ruta('Sounds', 'Explosion.wav'))
    except pygame.error as e:
        print(f"Error cargando sonidos: {e}")

# Música de fondo opcional
if AUDIO_AVAILABLE:
    try:
        pygame.mixer.music.load(ruta('Sounds', 'Playersong.ogg'))
        pygame.mixer.music.set_volume(0.4)
        pygame.mixer.music.play(-1)  # loop infinito
    except pygame.error:
        pass

# ============================================================
# FUNCIÓN PARA REINICIAR PARTIDA
# ============================================================
def new_game():
    """Crea todos los sprites y devuelve (all_sprites, meteor_list, lasers, player, score)."""
    all_sprites = pygame.sprite.Group()
    meteor_list = pygame.sprite.Group()
    lasers = pygame.sprite.Group()

    player = Player(laser_sound)
    player.all_sprites = all_sprites
    player.lasers = lasers
    all_sprites.add(player)

    # Crear meteoritos iniciales
    for _ in range(9):
        meteor = Meteor(meteor_images)
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    score = 0
    return all_sprites, meteor_list, lasers, player, score


# ============================================================
# VARIABLES DEL JUEGO
# ============================================================
score = 0
game_over = True
running = True
first_run = True   # para mostrar pantalla de inicio solo la primera vez

# ============================================================
# LOOP PRINCIPAL
# ============================================================
while running:

    if game_over:
        # Pantalla de inicio solo la primera vez
        if first_run:
            if not show_start_screen(screen, clock, background):
                break
            first_run = False

        all_sprites, meteor_list, lasers, player, score = new_game()
        game_over = False

    clock.tick(FPS)
    monitor_usage()   # imprime uso CPU/GPU cada 0.5 s

    # ---- EVENTOS ----
    for event in pygame.event.get():
        # Cerrar ventana con la X
        if event.type == pygame.QUIT:
            running = False

        # Tecla presionada
        elif event.type == pygame.KEYDOWN:
            # Disparar con ESPACIO o W
            if event.key in (pygame.K_SPACE, pygame.K_w):
                player.shoot()
            # Salir solo con ESC
            elif event.key == pygame.K_ESCAPE:
                running = False

        # ---- ACTUALIZAR ----
    all_sprites.update()

    # ---- CONTROLES POR TECLADO (continuos) ----
    keys = pygame.key.get_pressed()

    # DEBUG: ver si Pygame detecta las teclas
    if keys[pygame.K_a]:
        print("A PRESIONADA")
    if keys[pygame.K_SPACE]:
        print("SPACE PRESIONADA")
    if keys[pygame.K_w]:
        print("W PRESIONADA")

    # Disparar con ESPACIO o W
    if keys[pygame.K_SPACE] or keys[pygame.K_w]:
        player.shoot()

    # Salir con ESC
    if keys[pygame.K_ESCAPE]:
        running = False



    # ---- COLISIONES (Meteorito-Laser) ----
    hits = pygame.sprite.groupcollide(meteor_list, lasers, True, True)
    for _ in hits:
        score += 5
        if explosion_sound and AUDIO_AVAILABLE:
            try:
                explosion_sound.play()
            except Exception:
                pass
        meteor = Meteor(meteor_images)
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    # ---- COLISIONES (Meteorito-Jugador) ----
    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    for _ in hits:
        player.shield -= 25
        meteor = Meteor(meteor_images)
        all_sprites.add(meteor)
        meteor_list.add(meteor)
        if player.shield <= 0:
            game_over = True

    # ---- DIBUJAR ----
    screen.blit(background, [0, 0])
    all_sprites.draw(screen)

    # Marcador
    draw_text(screen, str(score), 40, SCREEN_WIDTH // 2, 5)

    # Barra de escudo
    draw_shield_bar(screen, 5, 5, player.shield)

    pygame.display.flip()

pygame.quit()
```
---

## Explicación del Código: `main_menu.py` (Launcher)

Este script actúa como el punto de entrada del proyecto. Su función principal es desacoplar la ejecución de los juegos, asegurando que si un juego falla o se cierra, el usuario regrese al menú en lugar de salir al escritorio.

***

### 1. Gestión de Procesos (`subprocess`)
A diferencia de importar los juegos como librerías (ej. `import Juego_1`), este menú los ejecuta como **procesos independientes**.

````python
subprocess.run([sys.executable, path], check=False)
````

  * **`sys.executable`:** Garantiza que el juego se lance utilizando **el mismo intérprete de Python** (y el mismo entorno virtual) que está ejecutando el menú.
  * **Aislamiento:** Si *Juego 1* tiene un error fatal (`crash`), el proceso hijo muere, pero el proceso padre (el menú) sigue vivo y puede recuperar el control.
  * **`check=False`:** Evita que el menú lance una excepción si el juego termina con un código de error.

-----

### 2\. Ciclo de Vida de la Ventana (Window Lifecycle)

Esta es la parte más inteligente del script, diseñada para ahorrar recursos en sistemas embebidos (como tu BeaglePlay).

**El flujo es:**

1.  **Cerrar Menú:** Antes de lanzar un juego, se llama a `pygame.display.quit()`. Esto destruye la ventana del menú y libera el contexto gráfico.
      * *Beneficio:* El juego hijo tiene acceso total a la GPU y RAM sin competir con el menú.
2.  **Bloqueo:** `subprocess.run` detiene la ejecución del menú hasta que el juego hijo se cierra.
3.  **Re-inicializar:** Una vez el juego termina (bloque `finally`), el menú detecta que volvió a tener el control y **reconstruye la ventana** (`pygame.init()`, `set_mode()`).

<!-- end list -->

```python
try:
    pygame.display.quit()  # 1. Liberar recursos
    subprocess.run(...)    # 2. Ejecutar y esperar
finally:
    pygame.init()          # 3. Reconstruir menú al volver
    screen = pygame.display.set_mode(...)
```

-----

### 3\. Sistema de Rutas Relativas (Portabilidad)

Para asegurar que el juego funcione en cualquier carpeta (PC o Linux embebido) sin editar código, se calculan las rutas dinámicamente:

```python
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
JUEGO1_PATH = os.path.join(BASE_DIR, 'Juego_1', 'main_opl.py')
```

  * Usa `__file__` para saber dónde está el script del menú y sube un nivel (`..`) para encontrar la raíz del proyecto. Esto hace que el proyecto sea "portable" (puedes mover la carpeta completa y seguirá funcionando).

-----

### 4\. Interfaz y Navegación

Se implementa una **Máquina de Estados simple** para la navegación por teclado, esencial para sistemas sin ratón (como arcades o consolas caseras).

  * **Variable `selected`:** Un entero (0 o 1) controla qué botón está activo.
  * **Feedback Visual:** La función `draw_button` cambia el color y añade un borde dorado (`border`) si `selected == True`.
  * **Comprobación de Archivos:** El diccionario `AVAILABLE` deshabilita visualmente los botones si los archivos de los juegos no se encuentran, previniendo errores de ejecución.

<!-- end list -->

---

### 5\. Codigo


````python
"""
Simple launcher/menu Pygame para elegir entre Juego_1 y Juego_2.
Ejecuta los scripts como procesos separados usando el mismo intérprete Python.

Uso: desde la raíz del workspace ejecutar:
    python .\Juego_Menu\main_menu.py

- Usa ARRIBA/ABAJO para seleccionar; ENTER para lanzar el juego.
- Cierra el juego para volver al menú.
- Pulsa ESC para cerrar el menú y salir.
"""

import os
import sys
import subprocess
import pygame
from pygame.locals import *

# Paths relativos (asume que se ejecuta desde workspace root o desde cualquier sitio; se resuelven vía __file__)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
JUEGO1_PATH = os.path.join(BASE_DIR, 'Juego_1', 'main_opl.py')
JUEGO2_PATH = os.path.join(BASE_DIR, 'Juego_2', 'main.py')

# Comprueba existencia
AVAILABLE = {
    'Juego 1': os.path.exists(JUEGO1_PATH),
    'Juego 2': os.path.exists(JUEGO2_PATH),
}

# Pygame UI
pygame.init()
WIDTH, HEIGHT = 640, 360
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Selector de Juegos')
font = pygame.font.SysFont(None, 32)
small = pygame.font.SysFont(None, 20)
clock = pygame.time.Clock()

# Botones: (label, rect)
button_w, button_h = 220, 64
gap = 30
x_center = WIDTH // 2 - button_w // 2
btn1_rect = pygame.Rect(x_center, 80, button_w, button_h)
btn2_rect = pygame.Rect(x_center, 80 + button_h + gap, button_w, button_h)

INFO_TEXT = 'Usa ARRIBA/ABAJO para seleccionar; ENTER para lanzar el juego.'


def draw_button(rect, label, enabled=True, selected=False):
    """Dibuja botón. `selected` resalta la opción activa (navegación por teclado)."""
    base = (40, 160, 40) if enabled else (120, 120, 120)
    if selected:
        # color más brillante para la selección
        color = tuple(min(255, c + 60) for c in base)
        border = (255, 215, 0)  # dorado
    else:
        color = base
        border = None

    pygame.draw.rect(screen, color, rect, border_radius=8)
    if border:
        pygame.draw.rect(screen, border, rect, width=3, border_radius=8)

    text = font.render(label, True, (255, 255, 255))
    tx = rect.x + (rect.w - text.get_width()) // 2
    ty = rect.y + (rect.h - text.get_height()) // 2
    screen.blit(text, (tx, ty))


def launch_game(path):
    """Lanza el juego indicado y espera hasta que termine.
    Cierra la ventana del menú antes de lanzar y la reabre al terminar.
    """
    if not os.path.exists(path):
        print(f"Archivo no encontrado: {path}")
        return
    print(f"Lanzando: {path}")

    # Usar el mismo intérprete
    global screen, font, small, clock
    try:
        # Cerrar la ventana del menú antes de lanzar el juego para que
        # la ventana del juego sea la única visible.
        try:
            pygame.display.quit()
        except Exception:
            pass

        # Bloquea hasta que el proceso termine; cuando termine, reabrimos el menú
        subprocess.run([sys.executable, path], check=False)
    except Exception as e:
        print('Error al lanzar el juego:', e)
    finally:
        # Re-inicializar la ventana del menú (si pygame sigue disponible)
        try:
            # Asegurarse de que pygame esté inicializado
            if not pygame.get_init():
                pygame.init()
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption('Selector de Juegos')
            # Recrear fuentes y reloj en caso de que se hayan cerrado
            font = pygame.font.SysFont(None, 32)
            small = pygame.font.SysFont(None, 20)
            clock = pygame.time.Clock()
        except Exception:
            # Si la re-inicialización falla, informamos pero no rompemos el menú caller
            print('Advertencia: no se pudo reabrir la ventana del menú automaticamente.')


running = True
# selección por teclado: 0 -> Juego 1, 1 -> Juego 2
selected = 0
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            # ESC cierra el programa
            if event.key == K_ESCAPE:
                # cerrar pygame y salir inmediatamente
                try:
                    pygame.quit()
                except Exception:
                    pass
                sys.exit(0)
            # Navegación: ARRIBA/ABAJO; activar con ENTER
            if event.key == K_UP:
                selected = max(0, selected - 1)
            elif event.key == K_DOWN:
                selected = min(1, selected + 1)
            elif event.key in (K_RETURN, K_KP_ENTER):
                # Lanzar el juego seleccionado (si está disponible)
                if selected == 0 and AVAILABLE['Juego 1']:
                    launch_game(JUEGO1_PATH)
                elif selected == 1 and AVAILABLE['Juego 2']:
                    launch_game(JUEGO2_PATH)

    screen.fill((18, 24, 34))

    # Título
    title = font.render('Menu de Inicio - Selecciona un Juego (usa flechas + ENTER)', True, (230, 230, 230))
    screen.blit(title, ((WIDTH - title.get_width()) // 2, 16))

    # Botones (resaltar según selección)
    draw_button(btn1_rect, 'Juego 1', enabled=AVAILABLE['Juego 1'], selected=(selected == 0))
    draw_button(btn2_rect, 'Juego 2', enabled=AVAILABLE['Juego 2'], selected=(selected == 1))

    # Estado disponibilidad
    available_text = 'Disponibilidad: ' + ', '.join(f"{k}: {'OK' if v else 'Falta'}" for k, v in AVAILABLE.items())
    st = small.render(available_text, True, (200, 200, 200))
    screen.blit(st, (12, HEIGHT - 28))

    # Info
    info = small.render(INFO_TEXT, True, (200, 200, 200))
    screen.blit(info, (12, HEIGHT - 48))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print('Menu cerrado.')

````

---

## Licencia

Este proyecto es de carácter académico. Universidad Nacional de Colombia - Sede Manizales, 2025.

---

## Créditos

Proyecto desarrollado en la asignatura *Sistemas Linux Embebidos*.
Autores: Ismael Cortes Ramirez, Juan Esteban Agreda Gutierrez.
Tecnologías principales: Python, Pygame, psutil (opcionalmente PyOpenGL).
