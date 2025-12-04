Proyecto Sistemas Linux Embebidos – Videojuegos 2D

Repositorio del proyecto de la asignatura Sistemas Embebidos en Linux, donde se desarrollan y optimizan dos videojuegos 2D usando Python + Pygame (y una versión opcional con OpenGL):

Juego_1 → plataforma 2D con animaciones de personaje y enemigos.

Juego_2 → shooter tipo Space War con meteoritos, barra de escudo y marcador.

(Opcional) Juego_Menu → menú para lanzar los juegos desde una misma interfaz.
# Proyecto Sistemas Linux Embebebidos — Videojuegos 2D

Repositorio del proyecto de la asignatura *Sistemas Embebidos en Linux*. Contiene ejemplos y versiones optimizadas de dos juegos 2D desarrollados en Python + Pygame:

- `Juego_1/` — plataforma 2D (versión Pygame y opcionalmente OpenGL).
- `Juego_2/` — shooter tipo Space War (meteoritos, barra de escudo y marcador).
- `Juego_Menu/` — (opcional) interfaz para lanzar los juegos desde un menú común.

El repositorio está preparado para ejecutarse en entornos Linux, WSL2 (con WSLg o servidor X) y sistemas embebidos con entorno gráfico.

---

## Índice rápido
- **Descripción** — ¿qué contiene el proyecto?
- **Estructura** — árbol de carpetas relevante
- **Requisitos** — hardware y software
- **Instalación** — pasos para preparar el entorno
- **Ejecución** — cómo lanzar cada juego
- **Optimización & notas técnicas** — decisiones relevantes
- **Contribuir** — cómo ayudar o probar cambios

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

## Requisitos

- **Python:** 3.10+ (se ha probado con 3.12)
- **Librerías:** `pygame`, `psutil` (opcional: `PyOpenGL`, `PyOpenGL_accelerate` si usas la versión OpenGL)
- **SO / gráfico:** X11/Wayland en Linux; en WSL2 usar WSLg o un servidor X
- **Hardware:** CPU x86_64 moderna; GPU dedicada no obligatoria para la versión Pygame

Dependencias rápidas:

```bash
pip install pygame psutil
# opcional (para Juego_1 OpenGL)
pip install PyOpenGL PyOpenGL_accelerate
```

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

- **Audio en WSL:** en algunos entornos (WSL sin audio) `pygame.mixer.init()` puede fallar. El código captura esta excepción y continúa sin sonido:

```py
try:
    pygame.mixer.init()
except pygame.error:
    print("Advertencia: audio no disponible, se continúa sin sonido.")
```

---

## Recomendaciones para la entrega

- Mostrar este README y los `README.md` de cada juego.
- Ejecutar el juego en Linux/WSL y mostrar controles + monitor CPU/GPU.
- Explicar brevemente la portabilidad por rutas relativas y las decisiones de optimización.

---

## Contribuir / pruebas

- Ejecuta `python main.py` en la carpeta del juego para probar.
- Para medir rendimiento revisa `utils.py` y `settings.py`.
- Si quieres, puedo añadir un `requirements.txt`, un script `run.sh` o traducir este README al inglés.

---

## Créditos

Proyecto desarrollado en la asignatura *Sistemas Embebidos en Linux*.
Autores: integrantes del grupo del curso.
Tecnologías principales: Python, Pygame, psutil (opcionalmente PyOpenGL).
