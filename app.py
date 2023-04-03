"""Juego con Obstáculos

Este ejemplo muestra como crear un juego con obstáculos, en el cual el jugador
debe evitar chocar con ellos o recolectarlos para ganar puntos.

Autores:
    - Ángel Ricardo Gutierrez Meza (201847467)
    - Crhistian André Díaz Bonfigli Pastrana (201829189)
"""

import random
import pygame
from models import Fruit, Player, Spike
from models.animated import FPS


WIDTH, HEIGHT = 800, 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TEXT_HEIGHT = 32

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Obstáculos")

font = pygame.font.SysFont("MS Sans Serif", TEXT_HEIGHT)


def draw(player: Player, fruits: list[Fruit], spikes: list[Spike]) -> None:
    """Dibuja todos los elementos en la pantalla"""
    screen.fill(BLACK)

    player.draw(screen)

    for fruit in fruits:
        fruit.draw(screen)

    for spike in spikes:
        spike.draw(screen)

    text = font.render(f"Puntaje: {player.score}", True, WHITE)

    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, TEXT_HEIGHT // 2)

    screen.blit(text, text_rect)

    pygame.display.flip()


def wait_screen() -> bool:
    """Muestra la pantalla de espera"""
    text = font.render("Presiona cualquier tecla para reiniciar", True, WHITE)

    text_rect = text.get_rect()
    text_rect.center = (WIDTH // 2, HEIGHT // 2)

    screen.blit(text, text_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                return True


def handle_movement(player: Player, fruits: list[Fruit], spikes: list[Spike]) -> None:
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

    for spike in spikes:
        spike.loop(screen)

        offset = (spike.rect.x - player.rect.x, spike.rect.y - player.rect.y)
        if player.mask.overlap(spike.mask, offset):
            player.status = "dead"


def main() -> None:
    """Función principal del juego"""
    running = True

    clock = pygame.time.Clock()

    player = Player((50, HEIGHT // 2))

    while running:
        fruits: list[Fruit] = []

        for i in range(150, WIDTH - 100, 100):
            for j in range(100, HEIGHT, 100):
                if not random.randint(0, 2):
                    fruits.append(Fruit((i, j)))

        spikes: list[Spike] = []

        for i in range(150, WIDTH - 100, 100):
            if random.randint(0, 1):
                center = (i, HEIGHT // 2)
                spikes.append(Spike(center))

        while running:
            clock.tick(FPS)

            draw(player, fruits, spikes)

            handle_movement(player, fruits, spikes)

            if player.status == "dead":
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

        if running:
            running = wait_screen()

            player.restart()

    pygame.quit()


if __name__ == "__main__":
    main()
