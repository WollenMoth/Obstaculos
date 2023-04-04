"""Módulo que contiene la clase Background"""

import pygame


class Background:
    """Representa el fondo del juego"""

    def __init__(self, screen: pygame.Surface):
        """Inicializa el fondo"""
        self.image = pygame.image.load("images/background/background.png")

        self.tiles = []

        width, height = self.image.get_size()

        for i in range(0, screen.get_width(), width):
            for j in range(0, screen.get_height(), height):
                self.tiles.append((i, j))

    def draw(self, screen: pygame.Surface) -> None:
        """Dibuja el fondo"""
        for tile in self.tiles:
            screen.blit(self.image, tile)
