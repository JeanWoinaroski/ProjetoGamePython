"""Sistema de mapa para renderizar níveis baseados em tiles (blocos)"""
import pygame
from src.world.tile import Tile


class Map:
    """Gerencia o mapa do jogo"""

    @staticmethod
    def generate_tile_data(cols, rows, border_tile=1, floor_tile=0, feature_tile=2):
        """Gera um mapa retangular simples (bordas são paredes)."""
        data = []
        for r in range(rows):
            row = []
            for c in range(cols):
                if r == 0 or r == rows - 1 or c == 0 or c == cols - 1:
                    row.append(border_tile)
                else:
                    # cria variação simples: 1 em padrão x/y para cabo de água
                    if (r % 2 == 0 and c % 2 == 0) and (r > 1 and c > 1):
                        row.append(feature_tile)
                    else:
                        row.append(floor_tile)
            data.append(row)
        return data

    def __init__(
        self,
        tile_data=None,
        tile_images=None,
        solid_tiles=None,
        tile_size=48,
        map_tile_amount=(10, 10),
        background_image=None,
        screen_width=1360,
        screen_height=920
    ):
        """Inicializa o mapa."""
        # Define o tile_data gerado automaticamente quando não fornecido
        if tile_data is None:
            cols, rows = map_tile_amount
            tile_data = Map.generate_tile_data(cols, rows)

        
        # Guarda o tamanho de cada tile
        self.tile_size = tile_size

        # Lista dos tiles do mapa
        self.tiles = []

        # Tiles sólidos
        self.solid_tiles = solid_tiles or []

        # Guarda o caminho da imagem escolhida
        self.background_image = background_image

        # Guarda tamanho da tela
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Variável da imagem carregada
        self.background = None

        # Carrega a imagem de fundo
        if self.background_image:
            try:
                print("Carregando fundo:", self.background_image)

                self.background = pygame.image.load(
                    self.background_image
                ).convert()

                # Ajusta a imagem para o tamanho da tela
                self.background = pygame.transform.scale(
                    self.background,
                    (self.screen_width, self.screen_height)
                )

                print("Fundo carregado com sucesso!")

            except Exception as e:
                print("Erro ao carregar imagem:", e)
                self.background = None

        # Cria os tiles do mapa
        for row_idx, row in enumerate(tile_data):
            for col_idx, tile_type in enumerate(row):

                if tile_type in tile_images:
                    image_or_color = tile_images[tile_type]

                    x = col_idx * self.tile_size
                    y = row_idx * self.tile_size

                    tile = Tile(
                        image_or_color,
                        x,
                        y,
                        self.tile_size,
                        self.tile_size
                    )

                    tile.tile_type = tile_type
                    self.tiles.append(tile)

        # Arquivo adicional de map titles (parâmetros de escala)
        self.map_width_tiles = len(tile_data[0]) if len(tile_data) > 0 else 0
        self.map_height_tiles = len(tile_data)
        self.map_pixel_width = self.map_width_tiles * self.tile_size
        self.map_pixel_height = self.map_height_tiles * self.tile_size

    def draw(self, surface):
        # Desenha a imagem de fundo primeiro
        if self.background:
            surface.blit(self.background, (0, 0))

        # Depois desenha os tiles
        for tile in self.tiles:
            tile.draw(surface)

    def collide_detection(self, rect):
        for tile in self.tiles:
            if tile.tile_type in self.solid_tiles:
                if tile.colliderect(rect):
                    return True

        return False