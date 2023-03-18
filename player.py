"""Módulo que contiene la clase Player"""

from typing import Union
import pygame
from common import Coordinate, Direction
from sprites import load_sprites

PLAYER_VELOCITY = 5


class Player(pygame.sprite.Sprite):
    """Representa al jugador"""

    def __init__(self, start: Coordinate, size: Coordinate) -> None:
        """Inicializa el jugador"""
        super().__init__()

        self.velocity = PLAYER_VELOCITY
        self.rect = pygame.Rect(start, size)
        self.mask = None
        self.direction: Union[Direction, None] = None
        self.animation_count = 0
        self.sprites = load_sprites("", size, True)
        self.sprite = "idle_right"

    def move(self, keys: pygame.key.ScancodeWrapper) -> None:
        """Mueve al jugador"""
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
            self.set_direction(Direction.left)
            self.sprite = "run_left"
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
            self.set_direction(Direction.right)
            self.sprite = "run_right"
        elif keys[pygame.K_UP]:
            self.rect.y -= self.velocity
            self.set_direction(Direction.up)
            self.sprite = "jump" + \
                ("_right" if "right" in self.sprite else "_left")
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.velocity
            self.set_direction(Direction.down)
            self.sprite = "fall" + \
                ("_right" if "right" in self.sprite else "_left")
        else:
            self.set_direction(None)
            self.sprite = "idle" + \
                ("_right" if "right" in self.sprite else "_left")

    def set_direction(self, direction: Union[Direction, None]) -> None:
        """Cambia la dirección del jugador"""
        if self.direction != direction:
            self.direction = direction
            self.animation_count = 0

    def draw(self, screen: pygame.Surface) -> None:
        """Dibuja al jugador"""
        screen.blit(self.sprites[self.sprite][self.animation_count], self.rect)
        self.animation_count += 1
        self.animation_count %= len(self.sprites[self.sprite])
