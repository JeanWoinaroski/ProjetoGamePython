# Mapa RPG - Dungeon explorável com múltiplos layouts
import random

TILE_SIZE = 50
MAP_TILE_AMOUNT = (10, 10)  # colunas, linhas

# Emule um caminho para um estilo criativo
tile_images = {
    0: (25, 100, 25),  # Verde escuro para grama/chão (mais natural)
    1: (80, 80, 80),   # Cinza escuro para parede (mais elegante)
    5: "assets/images/stone.png",  # Imagem da pedra (transparente)
    2: (150, 75, 0),   # Marrom para terra
    3: (0, 100, 0),    # Verde claro para grama
    4: (139, 69, 19),  # Marrom escuro para madeira
}

# Definição de tiles sólidos
solid_tiles = [1, 5]  # parede e pedra

# MAPAS PREDEFINIDOS - cada um representa um estágio de progresso
map_layouts = [
    # MAPA 0: Floresta Inicial (nenhum boss derrotado)
    [
        [1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,5,0,5,0,5,0,0,1],
        [1,0,0,0,0,0,0,5,0,1],
        [1,0,5,0,5,0,0,0,0,1],
        [1,0,0,0,0,5,0,5,0,1],
        [1,0,5,0,0,0,0,0,0,1],
        [1,0,0,5,0,5,0,5,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1]
    ],

    # MAPA 1: Floresta com riacho (1 boss derrotado)
    [
        [1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,2,2,2,2,2,2,0,1],
        [1,0,2,0,0,0,0,2,0,1],
        [1,0,2,0,5,5,0,2,0,1],
        [1,0,2,0,5,5,0,2,0,1],
        [1,0,2,0,0,0,0,2,0,1],
        [1,0,2,2,2,2,2,2,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1]
    ],

    # MAPA 2: Clareira com árvores (2 bosses derrotados)
    [
        [1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,3,3,3,3,3,3,0,1],
        [1,0,3,0,0,0,0,3,0,1],
        [1,0,3,0,5,0,0,3,0,1],
        [1,0,3,0,0,5,0,3,0,1],
        [1,0,3,0,0,0,0,3,0,1],
        [1,0,3,3,3,3,3,3,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1]
    ],

    # MAPA 3: Floresta densa (3 bosses derrotados)
    [
        [1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,5,5,5,5,5,5,0,1],
        [1,0,5,0,0,0,0,5,0,1],
        [1,0,5,0,5,5,0,5,0,1],
        [1,0,5,0,5,5,0,5,0,1],
        [1,0,5,0,0,0,0,5,0,1],
        [1,0,5,5,5,5,5,5,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1]
    ],

    # MAPA 4: Ruínas antigas (4 bosses derrotados)
    [
        [1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,0,4,4,4,4,4,4,0,1],
        [1,0,4,0,0,0,0,4,0,1],
        [1,0,4,0,5,0,0,4,0,1],
        [1,0,4,0,0,5,0,4,0,1],
        [1,0,4,0,0,0,0,4,0,1],
        [1,0,4,4,4,4,4,4,0,1],
        [1,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1]
    ],

    # MAPA 5: Caverna escura (5+ bosses derrotados)
    [
        [1,1,1,1,1,1,1,1,1,1],
        [1,5,5,5,5,5,5,5,5,1],
        [1,5,0,0,0,0,0,0,5,1],
        [1,5,0,5,5,5,5,0,5,1],
        [1,5,0,5,0,0,5,0,5,1],
        [1,5,0,5,0,0,5,0,5,1],
        [1,5,0,5,5,5,5,0,5,1],
        [1,5,0,0,0,0,0,0,5,1],
        [1,5,5,5,5,5,5,5,5,1],
        [1,1,1,1,1,1,1,1,1,1]
    ]
]

# Função para obter o mapa baseado no progresso
def get_map_for_progress(bosses_defeated):
    """Retorna o layout do mapa baseado no número de bosses derrotados"""
    map_index = min(bosses_defeated, len(map_layouts) - 1)
    return map_layouts[map_index]

# Mapa inicial (será atualizado dinamicamente)
tile_data = map_layouts[0]

# Imagem de fundo do espaço (substitua pelo caminho da sua imagem)
background_image = None  # Sem fundo para RPG