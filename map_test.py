#!/usr/bin/env python3
"""
Teste com mapa e herói
"""
import pygame
from src.core import Game

print('Criando jogo...')
game = Game()
print('Jogo criado!')

print('Mostrando mapa e herói por 5 segundos...')

start_time = pygame.time.get_ticks()
running = True

while running and pygame.time.get_ticks() - start_time < 5000:  # 5 segundos
    # Processar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Desenhar
    game.window.fill(game.COLOR_BACKGROUND)
    game.mapa.draw(game.window)
    game.heroi.draw(game.window)

    # Mostrar texto
    font = pygame.font.Font(None, 24)
    text = font.render("Mapa e Heroi visíveis! Fechando em alguns segundos...", True, (255, 255, 255))
    game.window.blit(text, (50, 50))

    pygame.display.update()
    game.relogio.tick(60)

print('Teste com mapa concluído!')
pygame.quit()