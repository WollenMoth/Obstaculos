"""Juego con Obstáculos

Este ejemplo muestra como crear un juego con obstáculos, en el cual el jugador
debe evitar chocar con ellos o recolectarlos para ganar puntos.

Autores:
    - Ángel Ricardo Gutierrez Meza (201847467)
    - Crhistian André Díaz Bonfigli Pastrana (201829189)
"""

import random
import pygame
from models import Background, End, Fruit, Player, Saw, Spike
from models.animated import FPS

TILE_SIZE = 64

WIDTH, HEIGHT = 12 * TILE_SIZE, 10 * TILE_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TEXT_HEIGHT = 32

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Obstáculos")

font = pygame.font.SysFont("MS Sans Serif", TEXT_HEIGHT)


def draw(
    background: Background,
    player: Player,
    fruits: list[Fruit],
    saws: list[Saw],
    spikes: list[Spike],
    end: End
) -> None:
    """Dibuja todos los elementos en la pantalla"""
    screen.fill(BLACK)

    background.draw(screen)

    player.draw(screen)

    for fruit in fruits:
        fruit.draw(screen)

    for saw in saws:
        saw.draw(screen)

    for spike in spikes:
        spike.draw(screen)

    end.draw(screen)

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
        offset = (fruit.rect.x - player.rect.x, fruit.rect.y - player.rect.y)
        if player.mask.overlap(fruit.mask, offset) and fruit.sprite != "collected":
            fruit.sprite = "collected"
            player.score += 1

    fruits_to_remove = [f for f in fruits if f.status == "collected"]

    for fruit in fruits_to_remove:
        fruits.remove(fruit)

    for saw in saws:
        saw.loop(screen)

        offset = (saw.rect.x - player.rect.x, saw.rect.y - player.rect.y)
        if player.mask.overlap(saw.mask, offset):
            player.status = "dead"

    for spike in spikes:
        spike.loop(screen)

        offset = (spike.rect.x - player.rect.x, spike.rect.y - player.rect.y)
        if player.mask.overlap(spike.mask, offset):
            player.status = "dead"

    offset = (end.rect.x - player.rect.x, end.rect.y - player.rect.y)
    if player.mask.overlap(end.mask, offset) and end.status == "normal":
        end.sprite = "pressed"


def main() -> None:
    """Función principal del juego"""
    running = True

    clock = pygame.time.Clock()

    background = Background(screen)

    player = Player((TILE_SIZE // 2, HEIGHT // 2))

    start = 2 * TILE_SIZE
    x_stop = WIDTH - 2 * TILE_SIZE
    y_stop = HEIGHT - 2 * TILE_SIZE
    step = int(1.5 * TILE_SIZE)

    while running:
        fruits: list[Fruit] = []

        saws: list[Saw] = []

        for i in range(start, x_stop, step):
            for j in range(start, y_stop + 1, step):
                if not random.randint(0, 2):
                    fruits.append(Fruit((i, j)))

        for i in range(start, x_stop, 2 * step):
            for j in range(start, y_stop + 1, 2 * step):
                if not random.randint(0, 2):
                    saws.append(Saw((i, j)))

        spikes: list[Spike] = []

        for i in range(start, x_stop, step):
            if random.randint(0, 1):
                center = (i, HEIGHT // 2)
                spikes.append(Spike(center))

        end = End((WIDTH - TILE_SIZE, HEIGHT // 2))

        while running:
            clock.tick(FPS)

            draw(background, player, fruits, saws, spikes, end)

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
