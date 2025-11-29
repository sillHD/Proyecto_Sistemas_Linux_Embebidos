# main.py (adaptado para usar funciones OpenGL desde funciones.py)
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import random
from settings import *
from funciones import *   # contiene load_texture_from_surface, draw_texture_tuple, walking_animation_textures, jumping_animation_textures, draw_hp_bar_gl, draw_batch

# Importar módulos de profiling (opcionales)
try:
    from profiler_module import FPSCounter, GameProfiler
    PROFILING_AVAILABLE = True
except ImportError:
    PROFILING_AVAILABLE = False
    print("Aviso: módulos de profiling no disponibles")

# =======================
# CONFIG VENTANA
# =======================
ANCHO_P, ALTO_P = 1280, 720
FPS = 60

pygame.init()
pygame.display.set_mode((ANCHO_P, ALTO_P), DOUBLEBUF | OPENGL)
pygame.display.set_caption("Juego OpenGL - Optimizado")

# =======================
# OPENGL SETUP
# =======================
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
# Mantengo la proyección tal como tenías (0..ANCHO_P, 0..ALTO_P)
# Usar origen en la esquina superior izquierda para que Y crezca hacia abajo.
# Esto hace que coordenadas como `base_y = 580` sitúen al jugador cerca
# del borde inferior de la ventana, como en coordenadas de Pygame.
glOrtho(0, ANCHO_P, ALTO_P, 0, -1, 1)
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
fondo_img = pygame.image.load(ruta("texturas", "background.png")).convert_alpha()
fondo_tex = load_texture_from_surface(fondo_img)
stayR_tex = load_texture_from_surface(
    pygame.image.load(ruta("texturas", "stay_right.png")).convert_alpha()
)

stayL_tex = load_texture_from_surface(
    pygame.image.load(ruta("texturas", "stay_left.png")).convert_alpha()
)


walk_right_tex = [
    load_texture_from_surface(
        pygame.image.load(ruta("texturas", "walk", "right", f"run_r{i}.png")).convert_alpha()
    )
    for i in range(1, 9)
]

walk_left_tex = [
    load_texture_from_surface(
        pygame.image.load(ruta("texturas", "walk", "left", f"run_l{i}.png")).convert_alpha()
    )
    for i in range(1, 9)
]

jump_right_tex = [
    load_texture_from_surface(
        pygame.image.load(ruta("texturas", "jump", "jump_right", f"jump_r{i}.png")).convert_alpha()
    )
    for i in range(1, 9)
]

jump_left_tex = [
    load_texture_from_surface(
        pygame.image.load(ruta("texturas", "jump", "jump_left", f"jump_l{i}.png")).convert_alpha()
    )
    for i in range(1, 9)
]

clouds_tex = [
    load_texture_from_surface(
        pygame.image.load(ruta("texturas", "clouds", f"c{i}.png")).convert_alpha()
    )
    for i in range(1, 4)
]
enemy_left_tex = [
    load_texture_from_surface(
        pygame.image.load(ruta("texturas", "enemy", "left", f"e_l{i}.png")).convert_alpha()
    )
    for i in range(1, 4)
]

enemy_right_tex = [
    load_texture_from_surface(
        pygame.image.load(ruta("texturas", "enemy", "right", f"e_r{i}.png")).convert_alpha()
    )
    for i in range(1, 4)
]


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

# Inicializar contadores de FPS y profiling (si disponibles)
fps_counter = None
profiler = None
if PROFILING_AVAILABLE:
    fps_counter = FPSCounter(window_size=60)
    profiler = GameProfiler(output_file="perfil.pstats")
    # Descomentar para activar profiling (ralentiza la ejecución):
    # profiler.start()

# Helper: cola de dibujado por textura

def enqueue_draw(draw_queue, tex_tuple, x, y, w=None, h=None, offset=(0,0)):
    tex_id, tw, th = tex_tuple
    if w is None: w = tw
    if h is None: h = th
    ox, oy = offset
    draw_queue.setdefault(tex_id, []).append((ox + x, oy + y, w, h))

# =======================
# LOOP PRINCIPAL
# =======================
while bin == 0:
    # actualizar cooldown (decrementar por frame)
    if cooldown_timer > 0:
        cooldown_timer -= 1

    clock.tick(FPS)
    glClear(GL_COLOR_BUFFER_BIT)

    # reset draw queue cada frame
    draw_queue = {}

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
    enqueue_draw(draw_queue, fondo_tex, 0, 0, ANCHO_P, ALTO_P)

    # ---- NUBES ----
    for cloud in cloud_positions:
        x, y, tex, speed, fc = cloud  # Desempaquetar velocidad y contador
        # dibujar solo si visible (optimización)
        if -tex[1] <= x <= ANCHO_P:
            enqueue_draw(draw_queue, tex, x, y, tex[1], tex[2])

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
        enqueue_draw(draw_queue, tex_tuple, pe_x1, pe_y1, tex_tuple[1], tex_tuple[2])
    if pe_x1 > ANCHO_P + 60:
        pe_x1 = -60

    pe_x2 -= ve2
    if -enemy_width <= pe_x2 <= ANCHO_P:
        tex_idx = (frame_counter // 10) % 3
        tex_tuple = enemy_left_tex[tex_idx]
        enqueue_draw(draw_queue, tex_tuple, pe_x2, pe_y2, tex_tuple[1], tex_tuple[2])
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
            # usar animación GPU (lista de tuples) -> encolar frame
            idx = (frame_counter // 3) % len(walk_left_tex)
            tex_tuple = walk_left_tex[idx]
            enqueue_draw(draw_queue, tex_tuple, pn_x, pn_y, tex_tuple[1], tex_tuple[2])
        else:
            # animación salto: elegir frame por ángulo
            step = math.pi / len(jump_left_tex)
            idx = min(int(angulo / step), len(jump_left_tex) - 1)
            tex_tuple = jump_left_tex[idx]
            enqueue_draw(draw_queue, tex_tuple, pn_x, pn_y, tex_tuple[1], tex_tuple[2])
    elif vn_x > 0:
        if angulo == 0:
            idx = (frame_counter // 3) % len(walk_right_tex)
            tex_tuple = walk_right_tex[idx]
            enqueue_draw(draw_queue, tex_tuple, pn_x, pn_y, tex_tuple[1], tex_tuple[2])
        else:
            step = math.pi / len(jump_right_tex)
            idx = min(int(angulo / step), len(jump_right_tex) - 1)
            tex_tuple = jump_right_tex[idx]
            enqueue_draw(draw_queue, tex_tuple, pn_x, pn_y, tex_tuple[1], tex_tuple[2])
    else:
        tex = stayL_tex if direccion == 1 else stayR_tex
        enqueue_draw(draw_queue, tex, pn_x, pn_y, tex[1], tex[2])

    # ---- FLUSH: dibujar por textura (reduce glBindTexture)
    for tex_id, quads in draw_queue.items():
        draw_batch(tex_id, quads)

    # ---- BARRA DE VIDA (dibujar al final para que no se borre) ----
    pct = max(0, min(100, player_health))  # asegurar 0..100
    # dibujamos con la función OpenGL de HP (usa 200x20 por defecto en el wrapper)
    draw_shield_bar_gl(50, 50, pct)

    pygame.display.flip()
    frame_counter += 1
    
    # Actualizar contador de FPS
    if fps_counter is not None:
        fps_counter.tick()
        if frame_counter % 300 == 0:  # Mostrar FPS cada 5 segundos (60 FPS * 5)
            fps = fps_counter.get_fps()
            ms = fps_counter.get_ms_per_frame()
            print(f"FPS: {fps:.1f} | MS/Frame: {ms:.2f}")

pygame.quit()

# Guardar profiling si fue iniciado
if profiler is not None and profiler.running:
    profiler.stop()
