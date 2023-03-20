"""Módulo que contiene la clase Player"""

import pygame
from common import Coordinate
from sprites import load_sprites

PLAYER_VELOCITY = 5
PLAYER_SIZE = (64, 64)
SPRITES_SIZE = (32, 32)


class Player(pygame.sprite.Sprite):
    """Representa al jugador"""

    def __init__(self, start: Coordinate) -> None:
        """Inicializa el jugador"""
        super().__init__()

        self.velocity = PLAYER_VELOCITY
        self.rect = pygame.Rect(start, PLAYER_SIZE)
        self.rect.center = start
        self.sprites = load_sprites("frog", SPRITES_SIZE, True)
        self._sprite = "idle_right"
        self.animation_count = 0
        self.update_mask()

    def move(self, keys: pygame.key.ScancodeWrapper, surface: pygame.Surface) -> None:
        """Mueve al jugador"""
        x, y = self.rect.topleft

        if keys[pygame.K_LEFT]:
            x -= self.velocity
            self.sprite = "run_left"
        elif keys[pygame.K_RIGHT]:
            x += self.velocity
            self.sprite = "run_right"
        elif keys[pygame.K_UP]:
            y -= self.velocity
            self.sprite = "jump" + self.sprite_direction
        elif keys[pygame.K_DOWN]:
            y += self.velocity
            self.sprite = "fall" + self.sprite_direction
        else:
            self.sprite = "idle" + self.sprite_direction

        surface_rect = surface.get_rect()
        surface_mask = pygame.mask.from_surface(surface)
        offset = (surface_rect.x - x, surface_rect.y - y)
        overlap_area = self.mask.overlap_area(surface_mask, offset)
        full_area = self.mask.count()

        if overlap_area == full_area:
            self.rect.topleft = (x, y)

    def draw(self, screen: pygame.Surface) -> None:
        """Dibuja al jugador"""
        screen.blit(self.current_sprite, self.rect)
        self.increase_count()

    def increase_count(self) -> None:
        """Aumenta el contador de animación"""
        self.animation_count += 1
        self.animation_count %= len(self.sprites[self.sprite])
        self.update_mask()

    def update_mask(self) -> None:
        """Actualiza la máscara"""
        self.mask = pygame.mask.from_surface(self.current_sprite)

    @property
    def sprite(self) -> str:
        """Obtiene el sprite actual"""
        return self._sprite

    @sprite.setter
    def sprite(self, sprite: str) -> None:
        """Cambia el sprite actual"""
        if self._sprite != sprite:
            self.animation_count = 0
            self._sprite = sprite
            self.mask = pygame.mask.from_surface(self.current_sprite)

    @property
    def current_sprite(self) -> pygame.Surface:
        """Obtiene el sprite actual"""
        return self.sprites[self.sprite][self.animation_count]

    @property
    def sprite_direction(self) -> str:
        """Obtiene la dirección del sprite"""
        return "_right" if "right" in self.sprite else "_left"
