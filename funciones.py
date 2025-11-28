# funciones_opengl.py
from OpenGL.GL import *
import math

def draw_texture(tex_id, x, y, w, h):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y)
    glTexCoord2f(1, 0); glVertex2f(x + w, y)
    glTexCoord2f(1, 1); glVertex2f(x + w, y + h)
    glTexCoord2f(0, 1); glVertex2f(x, y + h)
    glEnd()

def walking_animation(frames, x, y, frame_counter):
    frame = (frame_counter // 3) % len(frames)
    tex_id, w, h = frames[frame]
    draw_texture(tex_id, x, y, w, h)

def jumping_animation(frames, x, y, angulo):
    index = min(int(angulo / (math.pi / 8)), len(frames)-1)
    tex_id, w, h = frames[index]
    draw_texture(tex_id, x, y, w, h)
