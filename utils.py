import pygame


def move_rect(rect: pygame.Rect, keys, velocity: int):
    if keys[pygame.K_LEFT]:
        rect.x -= velocity
    if keys[pygame.K_RIGHT]:
        rect.x += velocity
    if keys[pygame.K_UP]:
        rect.y -= velocity
    if keys[pygame.K_DOWN]:
        rect.y += velocity


def keep_inside_surface(surface: pygame.Surface, rect: pygame.Rect):
    rect.left = max(0, rect.left)
    rect.right = min(surface.get_width(), rect.right)
    rect.top = max(0, rect.top)
    rect.bottom = min(surface.get_height(), rect.bottom)
