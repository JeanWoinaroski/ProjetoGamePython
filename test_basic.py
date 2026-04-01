import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((1080, 810))

# Teste básico: criar pyscripts
from src.Heroi import Heroi

heroi = Heroi(100, 100, 2, 'assets/images/Ninja.png')
print(f"Herói criado em: ({heroi.x}, {heroi.y})")

# Simular tecla pressionada
keys = [False] * 512
keys[pygame.K_d] = True

print(f"Antes de mover: ({heroi.x}, {heroi.y})")
heroi.move(keys)
print(f"Depois de mover (simulando D pressionado): ({heroi.x}, {heroi.y})")

if heroi.x != 102:
    print("ERRO: Herói não se moveu!")
else:
    print("OK: Herói se moveu corretamente!")
