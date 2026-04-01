"""Enum de direção para movimento e tiro em 4 direções"""
from enum import Enum
import pygame


class Direction(Enum):
    """Enum que representa as quatro direções cardeais"""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    NONE = None

    @staticmethod
    def from_keys(keys_pressed):
        """Retorna a direção baseada nas teclas pressionadas (SETAS DO TECLADO)"""
        if keys_pressed[pygame.K_UP]:
            return Direction.UP
        elif keys_pressed[pygame.K_DOWN]:
            return Direction.DOWN
        elif keys_pressed[pygame.K_LEFT]:
            return Direction.LEFT
        elif keys_pressed[pygame.K_RIGHT]:
            return Direction.RIGHT
        return Direction.NONE
