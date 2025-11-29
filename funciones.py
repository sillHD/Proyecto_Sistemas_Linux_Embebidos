# funciones_opengl.py
from OpenGL.GL import *
import math
import pygame
from settings import *


ANCHO_P, ALTO_P = 1280, 720

def draw_shield_bar(surface, x, y, percent): #Dibuja la barra de escudo que tiene la nave
    BAR_LENGHT = 100
    BAR_HEIGHT = 10
    fill = (percent / 100) * BAR_LENGHT
    border = pygame.Rect(x, y, BAR_LENGHT, BAR_HEIGHT)
    fill = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, VERDE, fill)
    pygame.draw.rect(surface, BLANCO, border, 3)

def draw_shield_bar_gl(x, y, percent):
    """Dibuja la barra de vida usando OpenGL.
    x,y están en coordenadas tipo pygame (y desde arriba)."""
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percent / 100.0) * BAR_LENGTH

    # Convertir y de coordenadas top-left (pygame) a bottom-left (OpenGL)
    ogl_y = ALTO_P - y - BAR_HEIGHT

    # Desactivar texturas y dibujar rectángulos
    glDisable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Relleno (verde)
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(x, ogl_y)
    glVertex2f(x + fill, ogl_y)
    glVertex2f(x + fill, ogl_y + BAR_HEIGHT)
    glVertex2f(x, ogl_y + BAR_HEIGHT)
    glEnd()

    # Borde (blanco)
    glColor3f(1.0, 1.0, 1.0)
    glLineWidth(2.0)
    glBegin(GL_LINE_LOOP)
    glVertex2f(x, ogl_y)
    glVertex2f(x + BAR_LENGTH, ogl_y)
    glVertex2f(x + BAR_LENGTH, ogl_y + BAR_HEIGHT)
    glVertex2f(x, ogl_y + BAR_HEIGHT)
    glEnd()

    # Restaurar estado
    glColor3f(1.0, 1.0, 1.0)
    glEnable(GL_TEXTURE_2D)

def load_texture(path): # Función para cargar texturas
    surf = pygame.image.load(path).convert_alpha()  # Usar convert_alpha para manejar la transparencia
    data = pygame.image.tostring(surf, "RGBA", True)
    w, h = surf.get_size()
    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, data)
    return tex, w, h  # Retornar la tupla con tex, w, h

def draw_texture(tex_id, x, y, w, h):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, ALTO_P - (y + h))  # Invertir Y
    glTexCoord2f(1, 0); glVertex2f(x + w, ALTO_P - (y + h))  # Invertir Y
    glTexCoord2f(1, 1); glVertex2f(x + w, ALTO_P - y)  # Invertir Y
    glTexCoord2f(0, 1); glVertex2f(x, ALTO_P - y)  # Invertir Y
    glEnd()

def walking_animation(frames, x, y, frame_counter):
    frame = (frame_counter // 3) % len(frames)
    tex_id, w, h = frames[frame]
    draw_texture(tex_id, x, y, w, h)

def jumping_animation(frames, x, y, angulo):
    index = min(int(angulo / (math.pi / 8)), len(frames)-1)
    tex_id, w, h = frames[index]
    draw_texture(tex_id, x, y, w, h)
