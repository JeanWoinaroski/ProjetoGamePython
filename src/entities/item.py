"""Entidade de item coletável (arma)"""
import pygame


class Item:
    """Arma que pode ser coletada no mapa"""

    def __init__(self, x, y, item_type):
        self.x = x
        self.y = y
        self.item_type = item_type  # 'basic_gun', 'laser_gun', 'spread_gun'

        # Imagem opcional baseada no tipo (mude em config se quiser)
        from config import ITEM_IMAGE_BASIC_GUN, ITEM_IMAGE_LASER_GUN, ITEM_IMAGE_SPREAD_GUN

        if item_type == 'basic_gun':
            image_path = ITEM_IMAGE_BASIC_GUN
        elif item_type == 'laser_gun':
            image_path = ITEM_IMAGE_LASER_GUN
        elif item_type == 'spread_gun':
            image_path = ITEM_IMAGE_SPREAD_GUN
        else:
            image_path = None

        self.size = 20
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

        if image_path:
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.smoothscale(self.image, (self.size, self.size))
            except (pygame.error, FileNotFoundError):
                self.image = None
        else:
            self.image = None

    def draw(self, surface):
        """Desenha a arma na tela"""
        if self.image:
            surface.blit(self.image, (self.x, self.y))
        else:
            # visual de reserva se não conseguir carregar imagem
            pygame.draw.circle(surface, (255, 255, 0), (self.x + self.size // 2, self.y + self.size // 2), self.size // 2)