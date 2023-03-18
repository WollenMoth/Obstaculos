"""Juego con Obstáculos

Este ejemplo muestra como crear un juego con obstáculos, en el cual el jugador
debe evitar chocar con ellos o recolectarlos para ganar puntos.

Autores:
    - Ángel Ricardo Gutierrez Meza (201847467)
    - Crhistian André Díaz Bonfigli Pastrana (201829189)
"""

import pygame
from player import Player


WIDTH, HEIGHT = 800, 600

FPS = 24

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Obstáculos")


def draw(player: Player) -> None:
    """Dibuja todos los elementos en la pantalla"""
    screen.fill(BLACK)

    player.draw(screen)

    pygame.display.flip()


def handle_movement(player: Player) -> None:
    """Maneja el movimiento del jugador"""
    keys = pygame.key.get_pressed()
    player.move(keys, screen)


def main() -> None:
    """Función principal del juego"""
    running = True

    clock = pygame.time.Clock()

    player = Player((50, HEIGHT // 2))

    while running:
        clock.tick(FPS)

        draw(player)

        handle_movement(player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()


if __name__ == "__main__":
    main()
