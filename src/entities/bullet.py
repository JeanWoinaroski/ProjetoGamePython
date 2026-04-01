"""Entidade de bala/projétil"""
import pygame
from src.systems import Direction


class Bullet:
    """Representa um projétil disparado pelo herói"""

    def __init__(self, x, y, direction, speed=5, size=10):
        """
        Inicializa uma bala

        Args:
            x (int): Posição X inicial
            y (int): Posição Y inicial
            direction (Direction): Direção que a bala vai seguir
            speed (float): Velocidade de movimento em pixels por quadro
            size (int): Tamanho da bala (largura e altura)
        """
        self.x = x
        self.y = y
        self.speed = speed
        self.direction = direction  # Enum de direção
        self.size = size
        self.width = size
        self.height = size
        self.color = (255, 255, 0)  # Amarelo para bala
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def move(self):
        """Move a bala na sua direção"""
        if self.direction == Direction.UP:
            self.y -= self.speed
        elif self.direction == Direction.DOWN:
            self.y += self.speed
        elif self.direction == Direction.LEFT:
            self.x -= self.speed
        elif self.direction == Direction.RIGHT:
            self.x += self.speed

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        """
        Desenha a bala na superfície dada

        Args:
            surface: Superfície pygame onde desenhar
        """
        pygame.draw.rect(surface, self.color, self.rect)

    def is_off_screen(self, screen_width, screen_height):
        """
        Verifica se a bala saiu da tela

        Args:
            screen_width (int): Largura da tela
            screen_height (int): Altura da tela

        Returns:
            bool: Verdadeiro se a bala está fora da tela
        """
        return self.x < 0 or self.x > screen_width or self.y < 0 or self.y > screen_height
