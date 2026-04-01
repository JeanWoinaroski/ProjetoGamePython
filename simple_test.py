#!/usr/bin/env python3
"""
Teste simplificado do jogo
"""
import pygame
from src.core import Game

print('Criando jogo...')
game = Game()
print('Jogo criado!')

print('Executando versão simplificada por 5 segundos...')

start_time = pygame.time.get_ticks()
running = True

while running and pygame.time.get_ticks() - start_time < 5000:  # 5 segundos
    # Processar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Desenhar tela básica
    game.window.fill((0, 0, 0))  # Fundo preto

    # Desenhar texto simples
    font = pygame.font.Font(None, 36)
    text = font.render("Jogo funcionando! Fechando em alguns segundos...", True, (255, 255, 255))
    game.window.blit(text, (50, 50))

    pygame.display.update()
    game.relogio.tick(60)

print('Teste simplificado concluído!')
pygame.quit()