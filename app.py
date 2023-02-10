import pygame
from utils import move_rect, keep_inside_surface

WIDTH, HEIGHT = 800, 600

FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PLAYER_SIZE = 20
PLAYER_COLOR = WHITE
PLAYER_VELOCITY = 5

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Obstáculos")


class Player(pygame.sprite.Sprite):
    SIZE = PLAYER_SIZE
    COLOR = PLAYER_COLOR
    VELOCITY = PLAYER_VELOCITY

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((self.SIZE, self.SIZE))
        self.image.fill(self.COLOR)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, self.rect)

    def move(self, keys, screen: pygame.Surface):
        move_rect(self.rect, keys, self.VELOCITY)
        keep_inside_surface(screen, self.rect)


def draw(screen: pygame.Surface, player: Player):
    screen.fill(BLACK)

    player.draw(screen)

    pygame.display.flip()


def handle_movement(screen, player: Player):
    keys = pygame.key.get_pressed()

    player.move(keys, screen)


def main():
    running = True

    clock = pygame.time.Clock()

    player = Player(50, HEIGHT // 2)

    while running:
        clock.tick(FPS)

        draw(screen, player)

        handle_movement(screen, player)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

    pygame.quit()


if __name__ == "__main__":
    main()
