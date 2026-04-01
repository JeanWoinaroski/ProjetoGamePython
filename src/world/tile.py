"""Entidade Tile para construção de níveis"""
import pygame
import sys


class Tile:
    """Representa um único bloco no mundo do jogo"""
    
    def __init__(self, image_path_or_color, x, y, width=48, height=48):
        """
        Inicializa um bloco
        
        Args:
            image_path_or_color (str or tuple): Caminho para imagem ou tupla RGB de cor
            x (int): Posição X em pixels
            y (int): Posição Y em pixels
            width (int): Largura do bloco em pixels
            height (int): Altura do bloco em pixels
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        if isinstance(image_path_or_color, str):
            try:
                self.image = pygame.image.load(image_path_or_color).convert_alpha()
                
                # Remove fundo preto/opaco automaticamente para transparência
                self.image = self._remove_black_background(self.image)
                
                self.image = pygame.transform.smoothscale(self.image, (self.width, self.height))
                self.is_image = True
            except pygame.error as e:
                print(f"Erro ao carregar imagem do bloco '{image_path_or_color}': {e}")
                pygame.quit()
                sys.exit(1)
        else:
            self.color = image_path_or_color
            self.is_image = False

    def _remove_black_background(self, image):
        """
        Substitui fundo preto da imagem pela cor do chão para camuflagem
        
        Args:
            image: Imagem pygame a ser processada
            
        Returns:
            Imagem com fundo preto substituído pela cor do chão
        """
        # Cria uma cópia da imagem
        processed_image = image.copy()
        
        # Converte para formato que permite manipulação de pixels
        processed_image = processed_image.convert()
        
        # Cor do chão para camuflagem
        floor_color = (25, 100, 25)
        
        # Itera por todos os pixels
        width, height = processed_image.get_size()
        for x in range(width):
            for y in range(height):
                # Obtém a cor do pixel
                color = processed_image.get_at((x, y))
                
                # Se for preto ou muito escuro, substitui pela cor do chão
                if color.r < 30 and color.g < 30 and color.b < 30:
                    processed_image.set_at((x, y), floor_color)
        
        return processed_image

    def draw(self, surface):
        """
        Desenha o bloco na superfície dada
        
        Args:
            surface: Superfície pygame onde desenhar
        """
        if self.is_image:
            surface.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))
        
    def colliderect(self, rect):
        """
        Verifica colisão com um retângulo
        
        Args:
            rect: Retângulo pygame para verificar colisão
            
        Returns:
            bool: Verdadeiro se o retângulo colide com este bloco
        """
        tile_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        return tile_rect.colliderect(rect)
