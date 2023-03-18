"""Tipos de datos comunes para el proyecto."""

from enum import Enum

Coordinate = tuple[int, int]
Direction = Enum("Direction", "left right up down")
