# funciones.py
import math
import pygame
from OpenGL.GL import *

# ============================================================
# TEXTURAS
# ============================================================

def load_texture_from_surface(surf):
    """Convierte una pygame.Surface en textura OpenGL.
       Devuelve (tex_id, width, height)."""
    image = pygame.image.tostring(surf, "RGBA", 1)
    width, height = surf.get_size()

    tex_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)

    glTexImage2D(
        GL_TEXTURE_2D, 0, GL_RGBA,
        width, height, 0,
        GL_RGBA, GL_UNSIGNED_BYTE, image
    )

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glBindTexture(GL_TEXTURE_2D, 0)
    return (tex_id, width, height)


def draw_texture_tuple(tex_tuple, x, y, w=None, h=None, offset=(0, 0)):
    """Dibuja una textura (tex_id, w, h) usando OpenGL."""
    tex_id, tw, th = tex_tuple

    if w is None: w = tw
    if h is None: h = th

    ox, oy = offset

    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)

    glTexCoord2f(0.0, 0.0); glVertex2f(ox + x,     oy + y)
    glTexCoord2f(1.0, 0.0); glVertex2f(ox + x + w, oy + y)
    glTexCoord2f(1.0, 1.0); glVertex2f(ox + x + w, oy + y + h)
    glTexCoord2f(0.0, 1.0); glVertex2f(ox + x,     oy + y + h)

    glEnd()
    glBindTexture(GL_TEXTURE_2D, 0)

# ============================================================
# ANIMACIONES
# ============================================================

def walking_animation_textures(texture_list, x, y, frame_counter, ventana_offset=(0, 0)):
    """Animación caminar usando GPU y texturas OpenGL."""
    if not texture_list:
        return

    idx = (frame_counter // 3) % len(texture_list)
    draw_texture_tuple(texture_list[idx], x, y, offset=ventana_offset)


def jumping_animation_textures(texture_list, x, y, angulo, ventana_offset=(0, 0)):
    """Animación saltar con mapeo de ángulo a frame."""
    if not texture_list:
        return

    step = math.pi / len(texture_list)
    idx = min(int(angulo / step), len(texture_list) - 1)

    draw_texture_tuple(texture_list[idx], x, y, offset=ventana_offset)

# ============================================================
# BARRA DE VIDA (HP BAR) - SOLO ESTA
# ============================================================

def draw_hp_bar_gl(x, y, width, height, value, max_value):
    """Barra de vida usando OpenGL."""
    pct = max(0.0, min(1.0, value / max_value))
    bar_width = width * pct

    # Fondo oscuro
    glColor3f(0.2, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + width, y)
    glVertex2f(x + width, y + height)
    glVertex2f(x, y + height)
    glEnd()

    # Barra roja
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + bar_width, y)
    glVertex2f(x + bar_width, y + height)
    glVertex2f(x, y + height)
    glEnd()

    # Reset color
    glColor3f(1, 1, 1)

