"""Módulo que contiene la clase Fruit"""

import random
from .animated import Animated

SPRITE_SIZE = (32, 32)


class Fruit(Animated):
    """Representa una fruta"""

    def __init__(self, center) -> None:
        """Inicializa la fruta"""
        super().__init__(center, "fruits", SPRITE_SIZE, False)

        self.sprite = random.choice(
            list(k for k in self.sprites if k != "collected")
        )
        self.status = "normal"

    def reset_count(self) -> None:
        """Resetea el contador de animación"""
        if self.animation_count == len(self.sprites[self.sprite]):
            self.animation_count = 0

            if self.sprite == "collected":
                self.status = "collected"
