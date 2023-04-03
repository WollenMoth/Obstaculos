"""Módulo que contiene la clase End"""

from .animated import Animated

SPRITE_SIZE = (64, 64)


class End(Animated):
    """Representa el final"""

    def __init__(self, center) -> None:
        """Inicializa el final"""
        super().__init__(center, "end", SPRITE_SIZE, False)

        self.sprite = "idle"
        self.status = "normal"

    def increase_count(self) -> None:
        """Aumenta el contador de animación"""
        self.animation_count += 1

        if self.animation_count == len(self.sprites[self.sprite]):
            self.animation_count = 0

            if self.sprite == "pressed":
                self.status = "pressed"

        self.update_mask()
