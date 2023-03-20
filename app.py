"""Juego con Obstáculos

Este ejemplo muestra como crear un juego con obstáculos, en el cual el jugador
debe evitar chocar con ellos o recolectarlos para ganar puntos.

Autores:
    - Ángel Ricardo Gutierrez Meza (201847467)
    - Crhistian André Díaz Bonfigli Pastrana (201829189)
"""

import random
import pygame
from models import Fruit, Player


WIDTH, HEIGHT = 800, 600

FPS = 24

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Obstáculos")


def draw(player: Player, fruits) -> None:
    """Dibuja todos los elementos en la pantalla"""
    screen.fill(BLACK)

    player.draw(screen)

    for fruit in fruits:
        fruit.draw(screen)

    pygame.display.flip()


def handle_movement(player: Player, fruits: list[Fruit]) -> None:
    """Maneja el movimiento del jugador"""
    keys = pygame.key.get_pressed()
    player.move(keys, screen)

    for fruit in fruits:
        offset = (fruit.rect.x - player.rect.x, fruit.rect.y - player.rect.y)
        if player.mask.overlap(fruit.mask, offset) and fruit.sprite != "collected":
            fruit.sprite = "collected"
            player.score += 1

    fruits_to_remove = [f for f in fruits if f.status == "collected"]

    for fruit in fruits_to_remove:
        fruits.remove(fruit)


def main() -> None:
    """Función principal del juego"""
    running = True

    clock = pygame.time.Clock()

    player = Player((50, HEIGHT // 2))

    fruits: list[Fruit] = []

    for i in range(150, WIDTH - 100, 100):
        for j in range(100, HEIGHT, 100):
            if not random.randint(0, 2):
                fruits.append(Fruit((i, j)))

    while running:
        clock.tick(FPS)

        draw(player, fruits)

        handle_movement(player, fruits)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()


if __name__ == "__main__":
    main()
