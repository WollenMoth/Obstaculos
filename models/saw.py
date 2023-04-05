"""Módulo que contiene la clase Saw"""

import random

import pygame

from common import Direction
from .animated import Animated

TILE_SIZE = 64
SPRITE_SIZE = (38, 38)
VELOCITY = (3, 5)


class Saw(Animated):
    """Representa un Saw"""

    def __init__(self, center) -> None:
        """Inicializa el Saw"""
        super().__init__(center, "saw", SPRITE_SIZE, True, fps=6)

        self.start = center
        self.direction = random.choice([Direction.up, Direction.down])
        self.velocity = random.randint(*VELOCITY)

    def loop(self, surface: pygame.Surface) -> None:
        """Ejecuta el loop del Saw"""
        self.rect.x += self.velocity if self.direction == Direction.up else -self.velocity
        self.rect.y += self.velocity if self.direction == Direction.down else -self.velocity

        surface_rect = surface.get_rect()
        collided = surface_rect.top >= self.rect.top or surface_rect.bottom <= self.rect.bottom

        reached_end = abs(self.rect.x - self.start[0]) >= TILE_SIZE

        if collided or reached_end:
            self.direction = Direction.up if self.direction == Direction.down else Direction.down
