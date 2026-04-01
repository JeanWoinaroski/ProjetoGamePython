#!/usr/bin/env python3
"""
Teste simples para verificar o que está travando o jogo
"""
import pygame
print("1. Pygame importado")

pygame.init()
print("2. Pygame inicializado")

# Criar uma janela antes de testar os objetos
window = pygame.display.set_mode((800, 600))
print("3. Janela criada")

from src.entities import Heroi
print("4. Heroi importado")

from src.world import Map
print("5. Map importado")

from levels.level1 import tile_data, tile_images, solid_tiles, MAP_TILE_AMOUNT
print("6. Level data importado")

print("✅ Todos os imports funcionaram!")
print("Agora testando criação dos objetos...")

try:
    heroi = Heroi(200, 200, 2, 'assets/images/Ninja.png')
    print("✅ Heroi criado")
except Exception as e:
    print(f"❌ Erro no heroi: {e}")

try:
    mapa = Map(
        tile_data=tile_data,
        tile_images=tile_images,
        solid_tiles=solid_tiles,
        tile_size=48,
        map_tile_amount=MAP_TILE_AMOUNT,
        screen_width=1360,
        screen_height=920
    )
    print("✅ Mapa criado")
except Exception as e:
    print(f"❌ Erro no mapa: {e}")

print("Teste concluído!")
pygame.quit()