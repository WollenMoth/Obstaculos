"""Módulo que contiene la clase Spike"""

import random
import pygame
from common import Direction
from .animated import Animated

SPRITE_SIZE = (54, 54)
VELOCITY = (5, 8)


class Spike(Animated):
    """Representa un Spike"""

    def __init__(self, center) -> None:
        """Inicializa el Spike"""
        super().__init__(center, "spike", SPRITE_SIZE, False, fps=6)
        self.direction = random.choice([Direction.up, Direction.down])
        self.velocity = random.randint(*VELOCITY)

    def loop(self, surface: pygame.Surface) -> None:
        """Ejecuta el loop del Spike"""
        self.rect.y += self.velocity if self.direction == Direction.down else -self.velocity

        surface_rect = surface.get_rect()
        collided = surface_rect.top >= self.rect.top or surface_rect.bottom <= self.rect.bottom

        if collided:
            self.direction = Direction.up if self.direction == Direction.down else Direction.down
