# settings.py
import os

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Dimensiones
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 562

# Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def ruta(*subrutas):
    """Construye rutas relativas a la carpeta del proyecto"""
    return os.path.join(BASE_DIR, *subrutas)
