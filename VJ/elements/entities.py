"""
Hola este es modulo Bug,
este modulo manejara la creacion y acciones de los Bugs
"""
import pygame
import random
from pygame.locals import (RLEACCEL)
from elements.parametros import ENEM_VELOC_RANGE
# bug
BUGpng = pygame.image.load('assets/bug.png')
BUGpng_scaled = pygame.transform.scale(BUGpng, (64, 64))

# coin
COINpng = pygame.image.load('assets/heart.png')
COINpng_scaled = pygame.transform.scale(COINpng, (64, 64))

class Enemy(pygame.sprite.Sprite):

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT, veloc_range):
        # nos permite invocar métodos o atributos de Sprite
        super(Enemy, self).__init__()
        
        self.surf = BUGpng_scaled
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH + 100,
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(*veloc_range)


    def update(self):
        self.rect.move_ip(-self.speed, 0)

        if self.rect.right < 0:
            self.kill()


class Heart(pygame.sprite.Sprite):

    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):
        super(Heart, self).__init__()
        
        self.screen_height = SCREEN_HEIGHT
        self.screen_width = SCREEN_WIDTH
        self.surf = COINpng_scaled
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH - 200,
                random.randint(0, SCREEN_HEIGHT),
            )
        )