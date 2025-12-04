# Juego_1 – Plataforma 2D (Proyecto Sistemas Linux Embebidos)

Videojuego 2D tipo **plataforma/survival** desarrollado en Python como parte de la asignatura **Sistemas Embebidos en Linux**.  
El jugador controla un personaje que puede **caminar** y **saltar** mientras evita enemigos que se mueven por la pantalla.  
Incluye una versión clásica con Pygame y una versión optimizada que usa **OpenGL** para renderizar sprites en la GPU.

---

## 1. Objetivo del juego

- Controlar al personaje principal y **sobrevivir** el mayor tiempo posible.
- Evitar que la hitbox del jugador colisione con la de los enemigos.
- Si hay colisión con algún enemigo, la partida termina.

No hay disparos ni ataque: la mecánica es de **evadir y moverse** aprovechando el salto y el desplazamiento lateral.

---

## 2. Controles

En la versión actual:

- **`←`** → mover personaje a la **izquierda**
- **`→`** → mover personaje a la **derecha**
- **`↑`** → **saltar**
- **`ENTER`** → salir de la pantalla de menú e iniciar partida (solo en la versión con menú)
- **`ESC`** → salir del juego

El juego se maneja únicamente con el teclado.

---

# Juego 1 — Plataforma 2D

Juego de plataforma desarrollado en Python como parte de la asignatura **Sistemas Embebidos en Linux**. El jugador controla un personaje que puede caminar y saltar para evitar enemigos. Existe una versión clásica con `pygame` y una versión optimizada con OpenGL (`PyOpenGL`) para render en GPU.

**Estado:** jugable · versión Pygame + versión OpenGL (opcional)

---

## Características principales
- Movimiento lateral y salto del jugador.
- Enemigos con hitboxes y colisiones simples (game over al impactar).
- Versión OpenGL con renderizado por lotes (batch) y barra de vida en GPU.
- Monitor opcional de CPU/GPU para evaluar coste en sistemas embebidos (`utils.py`).

---

## Controles
- `←` — mover a la izquierda
- `→` — mover a la derecha
- `↑` — saltar
- `ENTER` — iniciar partida desde menú (si aplica)
- `ESC` — salir

---

## Requisitos
- Python 3.10+ (probado con 3.12)
- `pygame`
- `psutil` (opcional, para monitor de recursos)
- `PyOpenGL`, `PyOpenGL_accelerate` (opcional, para la versión OpenGL)

Instalación rápida de dependencias:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install pygame psutil
# si quieres la versión OpenGL:
pip install PyOpenGL PyOpenGL_accelerate
```

---

## Estructura del directorio `Juego_1/`
- `main.py` — versión clásica con Pygame (loop principal, lógica, colisiones).
- `main_opl.py` — versión optimizada con OpenGL (dibujado en GPU y batch drawing).
- `funciones.py` — utilidades de carga/dibujo / animaciones / funciones OpenGL.
- `settings.py` — configuración (colores, tamaños) y función `ruta()` para rutas relativas.
- `utils.py` — monitor CPU/GPU y utilidades de desarrollo.
- `texturas/` — sprites y fondos (background, walk, jump, enemy, clouds).
- `Sounds/` — recursos de audio (puede estar desactivado para WSL).
- `info/` — documentación interna y notas de optimización.
- archivos históricos de prueba: `ETAPA_1.py`, `ETAPA_2.py`, `ETAPA_3.py`, `TEST_HITBOXES.py`, `TESTMOVEMENT.py`.

---

## Ejecución

Activar el entorno virtual (si aplica):

```bash
source venv/bin/activate
cd Juego_1
```

- Ejecutar versión Pygame:

```bash
python main.py
```

- Ejecutar versión OpenGL (si está disponible y configurado):

```bash
python main_opl.py
```

Nota: la versión OpenGL requiere que el sistema tenga soporte para contexto OpenGL en la ventana de Pygame (WSLg o X11 con drivers adecuados).

---

## Notas técnicas y optimizaciones
- `settings.ruta()` se usa para construir rutas relativas a los recursos, evitando rutas absolutas dependientes del sistema.
- En la versión OpenGL, las texturas se cargan en la GPU y se usan técnicas de *batch drawing* para reducir llamadas a la API gráfica.
- El disparo de eventos y la creación de objetos se controlan para no saturar la CPU en sistemas de bajos recursos.
- `utils.monitor_usage()` imprime periódicamente `CPU: xx.x% | GPU: yy%` para comparar coste entre versiones.

---

## Compatibilidad y audio
- En entornos sin audio (por ejemplo WSL sin configuración de sonido) la inicialización del `mixer` puede fallar; el código captura la excepción y continúa sin sonido.

```py
try:
  pygame.mixer.init()
except pygame.error:
  print("Advertencia: audio no disponible, se continúa sin sonido.")
```

---



---

## Cómo contribuir
- Ejecuta el juego y prueba mecánicas (`python main.py`).
- Revisa `utils.py` para medir y comparar el rendimiento.


---

© Proyecto Sistemas Embebidos — `Juego_1`
