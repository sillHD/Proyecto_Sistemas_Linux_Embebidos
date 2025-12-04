# Juego 2 – Space War (Proyecto Sistemas Linux Embebidos)

Shooter 2D tipo **“Space War”** desarrollado en Python con Pygame como parte del proyecto de la asignatura **Sistemas Embebidos en Linux**.

La nave del jugador se mueve en la parte inferior de la pantalla y debe destruir meteoritos que caen desde la parte superior, mientras protege su barra de escudo.

---

## Controles

- **A** → mover nave a la **izquierda**
- **D** → mover nave a la **derecha**
- **W** o **ESPACIO** → **disparar** láser
- **ESC** → salir del juego
- Cerrar ventana → terminar ejecución

---

## Estructura de archivos

Dentro de `Juego_2/`:

- `main.py`  
  Bucle principal del juego. Gestiona:
  - creación de sprites,
  - lógica de colisiones,
  - score,
  - barra de escudo,
  - lectura de teclado,
  - llamada al monitor de CPU/GPU (vía `utils.py`).

- `funciones.py`  
  Contiene la lógica del juego:
  - `Player`: clase de la nave del jugador (movimiento, disparo con cooldown).
  - `Meteor`: clase de meteoritos (posición, velocidad y respawn).
  - `Laser`: clase del láser disparado por el jugador.
  - Funciones de dibujo:
    - `draw_text`
    - `draw_shield_bar`

- `settings.py`  
  Parámetros generales:
  - tamaños de pantalla,
  - colores,
  - función `ruta()` para construir **rutas relativas portables** a las texturas y sonidos.

- `utils.py`  
  Utilidades de monitoreo:
  - `gpu_usage()`
  - `monitor_usage()`  
  Imprimen en consola el uso de CPU y de GPU cada cierto intervalo (pensado para evidenciar el costo del juego sobre el sistema embebido).

- Carpeta `Textturas/`  
  Contiene:
  - nave del jugador (`Cohete.png`),
  - meteoritos (`MeteoritoX.png`),
  - ovni (`Ovni.png`),
  - fondo (`Fondo2.png`),
  - sprite del láser (`Laser.png`).

- Carpeta `Sounds/`  
  Contiene:
  - `Lasersound.ogg` (disparo),
  - `Explosion.wav` (colisión),
  - `Playersong.ogg` (música de fondo, si se usa).

---

---

## Características
- Movimiento horizontal de la nave y disparo de láseres.
- Meteoritos con respawn aleatorio y colisiones físicas simples.
- Barra de escudo (shield) y mecánica de vida/reinicio.
- Monitor opcional de uso de CPU/GPU para evaluación en sistemas embebidos (`utils.py`).
- Soporte de audio cuando el sistema lo permite; el juego funciona sin sonido si no hay dispositivo.

---



---

## Requisitos
- Python 3.10+ (se ha probado con 3.12)
- `pygame`
- `psutil` (opcional, para monitor de recursos)

Instala con pip:

```bash
python3 -m venv venv         # opcional
source venv/bin/activate
pip install pygame psutil
```

---

## Ejecutar
Desde la raíz del repositorio:

```bash
cd Proyecto_Sistemas_Linux_Embebidos/Juego_2
python main.py
```

---

## Estructura del proyecto (`Juego_2/`)
- `main.py` — bucle principal: creación y actualización de sprites, manejo de colisiones, puntaje y loop de juego.
- `funciones.py` — clases y lógica de juego: `Player`, `Meteor`, `Laser` y funciones de dibujo (`draw_text`, `draw_shield_bar`).
- `settings.py` — parámetros globales (tamaños, colores) y la función `ruta()` para construir rutas relativas portables.
- `utils.py` — utilidades de monitorización (CPU/GPU) y funciones auxiliares de desarrollo.
- `Textturas/` — imágenes y sprites (nave, meteoritos, fondo, láser, etc.).
- `Sounds/` — efectos de sonido y música (si están disponibles).

---

## Notas técnicas y optimizaciones
- Rutas relativas: uso de `settings.ruta()` para evitar rutas absolutas y facilitar ejecución en Linux, WSL y Windows.
- Cooldown de disparo: `Player.shoot()` usa `pygame.time.get_ticks()` para limitar la tasa de disparo y reducir carga de sprites.
- Uso de `pygame.sprite.Group` para actualizar/dibujar objetos eficientemente.
- `utils.monitor_usage()` imprime información de uso de CPU y (si es accesible) una estimación de uso de GPU.

---

## Problemas conocidos (audio en WSL)
En entornos como WSL puede fallar la inicialización del mixer de audio de Pygame:

```py
try:
    pygame.mixer.init()
except pygame.error:
    print("Advertencia: audio no disponible, se continúa sin sonido.")
```

En ese caso el juego funciona sin sonido; en Linux nativo los efectos se reproducen normalmente.

---

## Cómo contribuir / pruebas
- Ejecuta `python main.py` para jugar y probar mecánicas.
- Para depurar o medir rendimiento, revisamos `utils.py` y `settings.py`.


---

© Proyecto Sistemas Embebidos — carpeta `Juego_2`
