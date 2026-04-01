#!/usr/bin/env python3
"""
Teste do loop principal do jogo
"""
import pygame
from src.core import Game

print('Criando jogo...')
game = Game()
print('Jogo criado com sucesso!')

print('Testando loop por 3 segundos...')
start_time = pygame.time.get_ticks()

while pygame.time.get_ticks() - start_time < 3000:  # 3 segundos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    # Simular um frame básico
    game.window.fill((0, 0, 0))
    pygame.display.update()
    game.relogio.tick(60)

print('Loop testado com sucesso!')
pygame.quit()