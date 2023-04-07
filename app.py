"""Juego con Obstáculos

Este ejemplo muestra como crear un juego con obstáculos, en el cual el jugador
debe evitar chocar con ellos o recolectarlos para ganar puntos.

Autores:
    - Ángel Ricardo Gutierrez Meza (201847467)
    - Crhistian André Díaz Bonfigli Pastrana (201829189)
"""

import random
from typing import Union
import pygame
from models import Animated, Background, End, Fruit, Player, Saw, Spike
from models.animated import FPS

TILE_SIZE = 64

WIDTH, HEIGHT = 12 * TILE_SIZE, 10 * TILE_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TEXT_HEIGHT = 32

FRUIT_PROB = 3
SAW_PROB = 3
SPIKE_PROB = 2

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Obstáculos")

font = pygame.font.SysFont("MS Sans Serif", TEXT_HEIGHT)


def draw(background: Background, player: Player, objects: list[Animated]) -> None:
    """Dibuja todos los elementos en la pantalla"""
    screen.fill(BLACK)

    background.draw(screen)

    player.draw(screen)

    for obj in objects:
        obj.draw(screen)

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


def handle_movement(
    player: Player,
    fruits: list[Fruit],
    saws: list[Saw],
    spikes: list[Spike],
    end: End
) -> None:
    """Maneja el movimiento del jugador"""
    keys = pygame.key.get_pressed()
    player.move(keys, screen)

    for fruit in fruits:
        if player.overlap(fruit) and fruit.sprite != "collected":
            fruit.sprite = "collected"
            player.score += 1

    fruits_to_remove = [f for f in fruits if f.status == "collected"]

    for fruit in fruits_to_remove:
        fruits.remove(fruit)

    for killer in [*saws, *spikes]:
        killer.loop(screen)

        if player.overlap(killer) and player.status != "dead":
            player.status = "dead"

    if player.overlap(end) and end.status == "normal":
        end.sprite = "pressed"


def gen_objs(obj: type, x_ran: Union[range, list], y_ran: Union[range, list], prob: int) -> list:
    """Genera una lista de objetos"""
    return [obj((i, j)) for i in x_ran for j in y_ran if not random.randint(0, prob - 1)]


def main() -> None:
    """Función principal del juego"""
    running = True

    clock = pygame.time.Clock()

    background = Background(screen)

    player = Player((TILE_SIZE // 2, HEIGHT // 2))

    start = 2 * TILE_SIZE
    x_stop = WIDTH - 2 * TILE_SIZE
    y_stop = HEIGHT - 2 * TILE_SIZE + 1
    step = int(1.5 * TILE_SIZE)

    while running:
        fruits = gen_objs(Fruit, range(start, x_stop, step),
                          range(start, y_stop, step), FRUIT_PROB)
        saws = gen_objs(Saw, range(start, x_stop, 2 * step),
                        range(start, y_stop, 2 * step), SAW_PROB)
        spikes = gen_objs(Spike, range(start, x_stop, step),
                          [HEIGHT // 2], SPIKE_PROB)
        end = End((WIDTH - TILE_SIZE, HEIGHT // 2))

        while running:
            clock.tick(FPS)

            draw(background, player, [*fruits, *saws, *spikes, end])

            handle_movement(player, fruits, saws, spikes, end)

            if player.status == "dead" or end.status == "pressed":
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

        if running and player.status == "dead":
            running = wait_screen()

        player.restart()

    pygame.quit()


if __name__ == "__main__":
    main()
