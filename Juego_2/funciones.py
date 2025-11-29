# funciones.py
import pygame
import random
from settings import *

# ============================================================
# CLASES SPRITE
# ============================================================

class Player(pygame.sprite.Sprite):
    """Clase del jugador/cohete"""
    def __init__(self, laser_sound_obj=None):
        super().__init__()
        self.image = pygame.image.load(ruta('Textturas', 'Cohete.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0
        self.shield = 100
        self.laser_sound = laser_sound_obj
        self.all_sprites = None
        self.lasers = None

    def update(self):
        """Actualiza la posición del jugador"""
        self.speed_x = 0
        keyst = pygame.key.get_pressed()
        if keyst[pygame.K_a]:
            self.speed_x = -6
        if keyst[pygame.K_d]:
            self.speed_x = 6
        self.rect.x += self.speed_x

        # Limitar a los bordes de la pantalla
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        """Dispara un láser"""
        if self.all_sprites and self.lasers:
            laser = Laser(self.rect.centerx, self.rect.top)
            self.all_sprites.add(laser)
            self.lasers.add(laser)
            if self.laser_sound:
                try:
                    self.laser_sound.play()
                except:
                    pass


class Meteor(pygame.sprite.Sprite):
    """Clase de meteorito"""
    def __init__(self, meteor_images_list):
        super().__init__()
        self.meteor_images = meteor_images_list
        self.image = random.choice(self.meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-70, -40)
        self.speed_y = random.randrange(3, 6)
        self.speed_x = random.randrange(-4, 5)

    def update(self):
        """Actualiza la posición del meteorito"""
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        
        # Reinicia si sale de la pantalla
        if self.rect.top > SCREEN_HEIGHT + 10 or self.rect.left < -45 or self.rect.right > SCREEN_WIDTH + 45:
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-140, -100)
            self.speed_y = random.randrange(2, 6)


class Laser(pygame.sprite.Sprite):
    """Clase de láser disparado por el jugador"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(ruta('Textturas', 'Laser.png')).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speed_y = -10

    def update(self):
        """Actualiza la posición del láser"""
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()


# ============================================================
# FUNCIONES DE DIBUJO
# ============================================================

def draw_text(surface, text, size, x, y):
    """Dibuja texto en la pantalla"""
    font = pygame.font.SysFont('broadway', size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def draw_shield_bar(surface, x, y, percent):
    """Dibuja la barra de escudo"""
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (percent / 100) * BAR_LENGTH
    border = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, GREEN, fill_rect)
    pygame.draw.rect(surface, WHITE, border, 3)


def show_start_screen(screen, clock, background_img):
    """Muestra la pantalla de inicio"""
    screen.blit(background_img, [0, 0])
    draw_text(screen, "SPACE WAR", 65, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 12)
    draw_text(screen, "Diego Cortes Silva", 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2.3)
    draw_text(screen, "Jhoan Sebastian Mosquera", 40, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.8)
    draw_text(screen, "Presione cualquier tecla", 25, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.2)
    pygame.display.flip()
    
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYUP:
                waiting = False
    return True
