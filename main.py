import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
from settings import ruta
from funciones import walking_animation, jumping_animation


# =======================
# CONFIG VENTANA
# =======================
ANCHO_P, ALTO_P = 1280, 720

pygame.init()
pygame.display.set_mode((ANCHO_P, ALTO_P), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Juego OpenGL")


# =======================
# OPENGL SETUP
# =======================
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, ANCHO_P, 0, ALTO_P, -1, 1)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

glEnable(GL_TEXTURE_2D)
glDisable(GL_DEPTH_TEST)


# =======================
# FUNCIÓN PARA CARGAR TEXTURAS
# =======================
def load_texture(path):
    surf = pygame.image.load(path).convert_alpha()
    data = pygame.image.tostring(surf, "RGBA", True)
    w, h = surf.get_size()

    tex = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, w, h, 0,
                 GL_RGBA, GL_UNSIGNED_BYTE, data)

    return tex, w, h


# =======================
# DIBUJAR TEXTURA
# =======================
def draw_texture(tex_id, x, y, w, h):
    glBindTexture(GL_TEXTURE_2D, tex_id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(x, y)
    glTexCoord2f(1, 0); glVertex2f(x + w, y)
    glTexCoord2f(1, 1); glVertex2f(x + w, y + h)
    glTexCoord2f(0, 1); glVertex2f(x, y + h)
    glEnd()


# =======================
# CARGAR TEXTURAS (USANDO TUS RUTAS)
# =======================

# --- Fondo ---
fondo_tex = load_texture(ruta("texturas", "background.png"))

# --- Stay ---
stayR_tex = load_texture(ruta("texturas", "stay_right.png"))
stayL_tex = load_texture(ruta("texturas", "stay_left.png"))

# --- Walk ---
walk_right_tex = [
    load_texture(ruta("texturas", "walk", "right", f"run_r{i}.png"))
    for i in range(1, 9)
]

walk_left_tex = [
    load_texture(ruta("texturas", "walk", "left", f"run_l{i}.png"))
    for i in range(1, 9)
]

# --- Jump ---
jump_right_tex = [
    load_texture(ruta("texturas", "jump", "jump_right", f"jump_r{i}.png"))
    for i in range(1, 9)
]

jump_left_tex = [
    load_texture(ruta("texturas", "jump", "jump_left", f"jump_l{i}.png"))
    for i in range(1, 9)
]

# --- Clouds ---
clouds_tex = [
    load_texture(ruta("texturas", "clouds", f"c{i}.png"))
    for i in range(1, 4)
]

# --- Enemigos ---
enemy_left_tex = [
    load_texture(ruta("texturas", "enemy", "left", f"e_l{i}.png"))
    for i in range(1, 4)
]

enemy_right_tex = [
    load_texture(ruta("texturas", "enemy", "right", f"e_r{i}.png"))
    for i in range(1, 4)
]


# =======================
# VARIABLES DEL JUEGO
# =======================
pn_x, pn_y = 640, 580
vn_x = 0
velocidad = 5

angulo = 0
direccion = -1

frame_counter = 0

# Nubes
cloud_positions = [
    [800, 520, random.choice(clouds_tex)],
    [300, 460, random.choice(clouds_tex)],
    [1100, 500, random.choice(clouds_tex)],
]

# Enemigos
pe_x1, pe_y1 = -60, 580
pe_x2, pe_y2 = 1224, 580
ve1, ve2 = random.randint(3, 6), random.randint(3, 6)


clock = pygame.time.Clock()
jugando = True


# =======================
# LOOP PRINCIPAL
# =======================
while jugando:

    clock.tick(60)
    glClear(GL_COLOR_BUFFER_BIT)

    # -----------------
    # MANEJO DE EVENTOS
    # -----------------
    for event in pygame.event.get():
        if event.type == QUIT:
            jugando = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                jugando = False
            if event.key == K_RIGHT:
                vn_x = velocidad
            if event.key == K_LEFT:
                vn_x = -velocidad
            if event.key == K_UP:
                if angulo == 0:
                    angulo = 0.001

        if event.type == KEYUP:
            if event.key in (K_RIGHT, K_LEFT):
                direccion = -1 if vn_x > 0 else 1
                vn_x = 0

    # -----------------
    # MOVIMIENTO JUGADOR
    # -----------------
    pn_x += vn_x
    pn_y = 580 - math.sin(angulo) * 200

    if angulo > 0:
        angulo += 0.10
        if angulo >= math.pi:
            angulo = 0

    # -----------------
    # FONDO
    # -----------------
    draw_texture(fondo_tex[0], 0, 0, ANCHO_P, ALTO_P)

    # -----------------
    # NUBES
    # -----------------
    for i in range(len(cloud_positions)):
        x, y, tex = cloud_positions[i]
        draw_texture(tex[0], x, y, tex[1], tex[2])

        cloud_positions[i][0] -= 1
        if cloud_positions[i][0] < -200:
            cloud_positions[i][0] = ANCHO_P + 100

    # -----------------
    # ENEMIGOS
    # -----------------
    # Enemigo 1
    pe_x1 += ve1
    draw_texture(enemy_right_tex[frame_counter % 3][0], pe_x1, pe_y1,
                 enemy_right_tex[0][1], enemy_right_tex[0][2])

    if pe_x1 > ANCHO_P + 60:
        pe_x1 = -60

    # Enemigo 2
    pe_x2 -= ve2
    draw_texture(enemy_left_tex[frame_counter % 3][0], pe_x2, pe_y2,
                 enemy_left_tex[0][1], enemy_left_tex[0][2])

    if pe_x2 < -60:
        pe_x2 = ANCHO_P + 60

    # -----------------
    # DIBUJAR JUGADOR
    # -----------------
    if vn_x < 0:
        if angulo == 0:
            walking_animation(walk_left_tex, pn_x, pn_y, frame_counter)
        else:
            jumping_animation(jump_left_tex, pn_x, pn_y, angulo)

    elif vn_x > 0:
        if angulo == 0:
            walking_animation(walk_right_tex, pn_x, pn_y, frame_counter)
        else:
            jumping_animation(jump_right_tex, pn_x, pn_y, angulo)

    else:
        tex = stayL_tex if direccion == 1 else stayR_tex
        draw_texture(tex[0], pn_x, pn_y, tex[1], tex[2])

    pygame.display.flip()
    frame_counter += 1

pygame.quit()
