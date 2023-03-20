"""Módulo que contiene la clase Player"""

import pygame
from common import Coordinate
from .animated import Animated

PLAYER_VELOCITY = 5
PLAYER_SIZE = (64, 64)
SPRITE_SIZE = (32, 32)

class Player(Animated):
    """Representa al jugador"""

    def __init__(self, center: Coordinate) -> None:
        """Inicializa el jugador"""
        super().__init__(pygame.Rect(center, PLAYER_SIZE), "frog", SPRITE_SIZE, True)

        self.velocity = PLAYER_VELOCITY

    def move(self, keys: pygame.key.ScancodeWrapper, surface: pygame.Surface) -> None:
        """Mueve al jugador"""
        topleft = self.rect.topleft

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
            self.sprite = "run_left"
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
            self.sprite = "run_right"
        elif keys[pygame.K_UP]:
            self.rect.y -= self.velocity
            self.sprite = "jump" + self.sprite_direction
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.velocity
            self.sprite = "fall" + self.sprite_direction
        else:
            self.sprite = "idle" + self.sprite_direction

        surface_rect = surface.get_rect()
        surface_mask = pygame.mask.from_surface(surface)
        offset = (surface_rect.x - self.rect.x, surface_rect.y - self.rect.y)
        overlap_area = self.mask.overlap_area(surface_mask, offset)
        full_area = self.mask.count()

        if overlap_area != full_area:
            self.rect.topleft = topleft
