import pygame

pygame.init()
screen = pygame.display.set_mode((1080, 810))

from src.Heroi import Heroi

heroi = Heroi(200, 200, 2, 'assets/images/Ninja.png')
print(f"Posição inicial: ({heroi.x}, {heroi.y})")

# Teste para cada direção
directions = [
    (pygame.K_d, "Direita"),
    (pygame.K_a, "Esquerda"),
    (pygame.K_w, "Cima"),
    (pygame.K_s, "Baixo")
]

for key_code, direction_name in directions:
    old_x, old_y = heroi.x, heroi.y
    keys = [False] * 512
    keys[key_code] = True
    heroi.move(keys)
    print(f"{direction_name}: ({old_x}, {old_y}) -> ({heroi.x}, {heroi.y})")
    # Resetar posição
    heroi.x, heroi.y = 200, 200

print("Teste concluído!")
