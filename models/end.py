"""Módulo que contiene la clase End"""

from .animated import Animated

SPRITE_SIZE = (64, 64)


class End(Animated):
    """Representa el final"""

    def __init__(self, center) -> None:
        """Inicializa el final"""
        super().__init__(center, "end", SPRITE_SIZE, False, fps=12)

        self.sprite = "idle"
        self.status = "normal"

    def reset_count(self) -> None:
        """Resetea el contador de animación"""
        if self.animation_count == len(self.sprites[self.sprite]):
            self.animation_count = 0

            if self.sprite == "pressed":
                self.status = "pressed"
