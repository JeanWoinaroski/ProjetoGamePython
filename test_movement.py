import pygame
from src.Heroi import Heroi

pygame.init()
screen = pygame.display.set_mode((1080, 810))
pygame.display.set_caption("Teste de Movimento")
clock = pygame.time.Clock()

heroi = Heroi(100, 100, 2, 'assets/images/Ninja.png')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()
    print(f"Keys: A={keys[pygame.K_a]}, D={keys[pygame.K_d]}, W={keys[pygame.K_w]}, S={keys[pygame.K_s]}")
    print(f"Posição antes: {heroi.x}, {heroi.y}")
    
    heroi.move(keys)
    
    print(f"Posição depois: {heroi.x}, {heroi.y}")
    print("---")
    
    screen.fill((0, 0, 0))
    screen.blit(heroi.image, (heroi.x, heroi.y))
    pygame.display.update()
    clock.tick(2)  # Lento para ver os prints

pygame.quit()
