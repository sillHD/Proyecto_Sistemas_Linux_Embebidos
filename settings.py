# settings.py
from OpenGL.GL import *
from OpenGL.GLU import *

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
MARRON = (180, 100, 60)

# Paths
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
def ruta(*subrutas):
    return os.path.join(BASE_DIR, *subrutas)