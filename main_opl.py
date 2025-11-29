# main.py (adaptado para usar funciones OpenGL desde funciones.py)
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
from settings import *
from funciones import *   # contiene load_texture_from_surface, draw_texture_tuple, walking_animation_textures, jumping_animation_textures, draw_hp_bar_gl

# =======================
# CONFIG VENTANA
# =======================
ANCHO_P, ALTO_P = 1280, 720
FPS = 60

pygame.init()
pygame.display.set_mode((ANCHO_P, ALTO_P), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Juego OpenGL")

# =======================
# OPENGL SETUP
# =======================
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
# Mantengo la proyección tal como tenías (0..ANCHO_P, 0..ALTO_P)
glOrtho(0, ANCHO_P, 0, ALTO_P, -1, 1)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

glEnable(GL_TEXTURE_2D)
glEnable(GL_BLEND)  # Habilitar transparencia
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)  # Configurar blending
glDisable(GL_DEPTH_TEST)

# -----------------------
# Wrappers / aliases para mantener tus llamadas
# -----------------------
# load_texture en tu código original devolvía (tex_id, w, h). Nuestra función se llama load_texture_from_surface.
load_texture = load_texture_from_surface

# draw_texture en tu código original recibía (tex_id, x, y, w, h)
def draw_texture(tex_id, x, y, w, h, offset=(0,0)):
    """Dibuja una textura dado su tex_id y tamaño (w,h)."""
    # Reutilizamos draw_texture_tuple que espera (tex_tuple, ...)
    draw_texture_tuple((tex_id, w, h), x, y, w, h, offset=offset)

# Animaciones (alias a las funciones GPU)
walking_animation = walking_animation_textures
jumping_animation = jumping_animation_textures

# Wrapper para mantener el nombre draw_shield_bar_gl que usas en main,
# pero internamente llamamos a draw_hp_bar_gl(x, y, width, height, value, max_value)
def draw_shield_bar_gl(x, y, pct):
    # pct ya está en 0..100, convertimos a value,max_value
    draw_hp_bar_gl(x, y, 200, 20, pct, 100)


# =======================
# CARGAR TEXTURAS
# =======================
# load_texture returns (tex_id, w, h)
fondo_tex = load_texture(ruta("texturas", "background.png"))
stayR_tex = load_texture(ruta("texturas", "stay_right.png"))
stayL_tex = load_texture(ruta("texturas", "stay_left.png"))

walk_right_tex = [load_texture(ruta("texturas", "walk", "right", f"run_r{i}.png")) for i in range(1, 9)]
walk_left_tex  = [load_texture(ruta("texturas", "walk", "left", f"run_l{i}.png")) for i in range(1, 9)]
jump_right_tex = [load_texture(ruta("texturas", "jump", "jump_right", f"jump_r{i}.png")) for i in range(1, 9)]
jump_left_tex  = [load_texture(ruta("texturas", "jump", "jump_left", f"jump_l{i}.png")) for i in range(1, 9)]
clouds_tex     = [load_texture(ruta("texturas", "clouds", f"c{i}.png")) for i in range(1, 4)]
enemy_left_tex = [load_texture(ruta("texturas", "enemy", "left", f"e_l{i}.png")) for i in range(1, 4)]
enemy_right_tex= [load_texture(ruta("texturas", "enemy", "right", f"e_r{i}.png")) for i in range(1, 4)]

# =======================
# FUNCIÓN DE COLISIÓN
# =======================
def check_collision(x1, y1, w1, h1, x2, y2, w2, h2):
    """Detecta colisión entre dos rectángulos"""
    return (x1 < x2 + w2 and
            x1 + w1 > x2 and
            y1 < y2 + h2 and
            y1 + h1 > y2)

# =======================
# VARIABLES JUGADOR
# =======================
base_y = 580
pn_x, pn_y = 640, base_y
vn_x = 0
velocidad = 5
angulo = 0
direccion = -1
frame_counter = 0
player_width = 60  # Ancho aproximado del jugador
player_height = 80  # Alto aproximado del jugador
player_health = 100
bin = 0
cooldown_timer = 0  # invencibilidad restante en frames (0 = vulnerable)

# =======================
# NUBES
# Estructura: [x, y, tex_tuple, speed, frame_counter_for_texture]
# =======================
cloud_positions = [
    [800, 60, random.choice(clouds_tex), random.randint(1, 3), 0],
    [300, 60, random.choice(clouds_tex), random.randint(1, 3), 0],
    [1100, 60, random.choice(clouds_tex), random.randint(1, 3), 0],
]

# =======================
# ENEMIGOS
# =======================
pe_x1, pe_y1 = -60, 600
pe_x2, pe_y2 = 1224, 600
ve1, ve2 = random.randint(3, 6), random.randint(3, 6)

clock = pygame.time.Clock()

# =======================
# LOOP PRINCIPAL
# =======================
while bin == 0:
    # actualizar cooldown (decrementar por frame)
    if cooldown_timer > 0:
        cooldown_timer -= 1

    clock.tick(FPS)
    glClear(GL_COLOR_BUFFER_BIT)

    # ---- EVENTOS ----
    for event in pygame.event.get():
        if event.type == QUIT:
            bin = 1
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                bin = 1
            if event.key == K_RIGHT:
                vn_x = velocidad
            if event.key == K_LEFT:
                vn_x = -velocidad
            if event.key == K_UP and angulo == 0:
                angulo = 0.001
        if event.type == KEYUP:
            if event.key in (K_RIGHT, K_LEFT):
                # corregimos direccion según última entrada
                direccion = -1 if event.key == K_RIGHT else 1
                vn_x = 0

    # ---- MOVIMIENTO JUGADOR ----
    pn_x += vn_x
    if angulo > 0:
        pn_y = base_y - math.sin(angulo) * 200
        angulo += 0.1
        if angulo >= math.pi:
            angulo = 0
            pn_y = base_y
    else:
        pn_y = base_y

    # Mantener dentro de pantalla
    pn_x = max(0, min(ANCHO_P - 60, pn_x))

    # ---- FONDO ----
    # fondo_tex es (tex_id,w,h)
    draw_texture(fondo_tex[0], 0, 0, ANCHO_P, ALTO_P)

    # ---- NUBES ----
    for cloud in cloud_positions:
        x, y, tex, speed, fc = cloud  # Desempaquetar velocidad y contador
        # dibujar solo si visible (optimización)
        if -tex[1] <= x <= ANCHO_P:
            draw_texture(tex[0], x, y, tex[1], tex[2])

        # Actualizar posición de la nube (moviéndose hacia la izquierda)
        cloud[0] -= speed

        # Cambiar textura de la nube cada cierto tiempo (solo una vez cada 30 frames)
        cloud[4] += 1
        if cloud[4] >= 30:
            cloud[2] = random.choice(clouds_tex)
            cloud[4] = 0

        # Reiniciar posición de la nube
        if cloud[0] < -200:
            cloud[0] = ANCHO_P + 100

    # ---- ENEMIGOS ----
    # obtenemos tamaño del enemigo desde la primera textura
    enemy_width = enemy_right_tex[0][1]
    enemy_height = enemy_right_tex[0][2]

    pe_x1 += ve1
    # dibujar solo si visible
    if -enemy_width <= pe_x1 <= ANCHO_P:
        # escogemos frame por frame_counter
        tex_idx = (frame_counter // 10) % 3
        tex_tuple = enemy_right_tex[tex_idx]
        draw_texture(tex_tuple[0], pe_x1, pe_y1, tex_tuple[1], tex_tuple[2])
    if pe_x1 > ANCHO_P + 60:
        pe_x1 = -60

    pe_x2 -= ve2
    if -enemy_width <= pe_x2 <= ANCHO_P:
        tex_idx = (frame_counter // 10) % 3
        tex_tuple = enemy_left_tex[tex_idx]
        draw_texture(tex_tuple[0], pe_x2, pe_y2, tex_tuple[1], tex_tuple[2])
    if pe_x2 < -60:
        pe_x2 = ANCHO_P + 60

    # ---- COLISIONES ----
    if (check_collision(pn_x, pn_y, player_width, player_height, pe_x1, pe_y1, enemy_width, enemy_height)
        or check_collision(pn_x, pn_y, player_width, player_height, pe_x2, pe_y2, enemy_width, enemy_height)):
        if cooldown_timer == 0:
            player_health -= 10  # Restar 10 de vida
            cooldown_timer = FPS  # 1 segundo de invencibilidad
        if player_health <= 0:
            break  # Terminar juego

    # ---- JUGADOR ----
    if vn_x < 0:
        if angulo == 0:
            # usar animación GPU (lista de tuples)
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

    # ---- BARRA DE VIDA (dibujar al final para que no se borre) ----
    pct = max(0, min(100, player_health))  # asegurar 0..100
    # dibujamos con la función OpenGL de HP (usa 200x20 por defecto en el wrapper)
    draw_shield_bar_gl(50, 50, pct)

    pygame.display.flip()
    frame_counter += 1

pygame.quit()
