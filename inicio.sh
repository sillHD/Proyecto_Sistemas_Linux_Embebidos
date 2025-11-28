#!/bin/bash

# Ruta base
PROJECT_DIR="/home/devuser/Proyecto_Sistemas_Linux_Embebidos"

# Entrar al proyecto
cd "$PROJECT_DIR"

# Activar entorno virtual (ruta absoluta)
source "$PROJECT_DIR/venv/bin/activate"

# Necesario para pygame en X11
export DISPLAY=:0
export SDL_VIDEODRIVER=x11

# Ejecutar el juego
python "$PROJECT_DIR/Juego.py"

# Desactivar entorno
deactivate



