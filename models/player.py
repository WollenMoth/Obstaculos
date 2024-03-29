"""Módulo que contiene la clase Player"""

import pygame
from common import Coordinate
from .animated import Animated

PLAYER_VELOCITY = 8
SPRITE_SIZE = (32, 32)


class Player(Animated):
    """Representa al jugador"""

    def __init__(self, center: Coordinate) -> None:
        """Inicializa el jugador"""
        super().__init__(center, "frog", SPRITE_SIZE, True)

        self.start = center
        self.velocity = PLAYER_VELOCITY
        self.score = 0
        self.status = "alive"

    def move(self, keys: pygame.key.ScancodeWrapper, surface: pygame.Surface) -> None:
        """Mueve al jugador"""
        topleft = self.rect.topleft

        directions = {
            "left": keys[pygame.K_LEFT] or keys[pygame.K_a],
            "right": keys[pygame.K_RIGHT] or keys[pygame.K_d],
            "up": keys[pygame.K_UP] or keys[pygame.K_w],
            "down": keys[pygame.K_DOWN] or keys[pygame.K_s]
        }

        if directions["left"]:
            self.rect.x -= self.velocity
            self.sprite = "run_left"
        elif directions["right"]:
            self.rect.x += self.velocity
            self.sprite = "run_right"

        if directions["up"]:
            self.rect.y -= self.velocity
            self.sprite = "jump" + self.sprite_direction
        elif directions["down"]:
            self.rect.y += self.velocity
            self.sprite = "fall" + self.sprite_direction

        if not any(directions.values()):
            self.sprite = "idle" + self.sprite_direction

        surface_rect = surface.get_rect()
        surface_mask = pygame.mask.from_surface(surface)
        offset = (surface_rect.x - self.rect.x, surface_rect.y - self.rect.y)
        overlap_area = self.mask.overlap_area(surface_mask, offset)
        full_area = self.mask.count()

        if overlap_area != full_area:
            self.rect.topleft = topleft

    def restart(self) -> None:
        """Reinicia al jugador"""
        self.rect.center = self.start

        if self.status == "dead":
            self.status = "alive"
            self.score = 0

    def overlap(self, other: Animated) -> bool:
        """Comprueba si el jugador colisiona con otro sprite"""
        offset = (other.rect.x - self.rect.x, other.rect.y - self.rect.y)
        return bool(self.mask.overlap(other.mask, offset))
