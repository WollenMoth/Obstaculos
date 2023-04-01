"""Módulo que contiene la clase Animated"""

import pygame
from common import Coordinate
from sprites import load_sprites

FPS = 24


class Animated(pygame.sprite.Sprite):
    """Clase que representa un sprite animado"""

    def __init__(
        self,
        center: Coordinate,
        directory: str,
        size: Coordinate,
        flipped: bool = False,
        fps: int = 24
    ):
        """Inicializa la clase Animated"""
        super().__init__()
        self.rect = pygame.Rect(center, tuple(s * 2 for s in size))
        self.rect.center = self.rect.topleft
        self.animation_count = 0
        self.sprites = load_sprites(directory, size, flipped)
        self._sprite = self.sprites.keys().__iter__().__next__()
        self.update_mask()
        self.fps = fps

    def draw(self, screen: pygame.Surface) -> None:
        """Dibuja el sprite"""
        screen.blit(self.current_sprite, self.rect)
        self.increase_count()

    def increase_count(self) -> None:
        """Aumenta el contador de animación"""
        self.animation_count += self.fps / FPS
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
        return self.sprites[self.sprite][int(self.animation_count)]

    @property
    def sprite_direction(self) -> str:
        """Obtiene la dirección del sprite"""
        return "_right" if "right" in self.sprite else "_left"
