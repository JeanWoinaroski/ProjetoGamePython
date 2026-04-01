import pygame
pygame.init()
pygame.display.set_mode((1080, 810))

from src.Direction import Direction

print("Testando Direction enum:")
print(f"UP value: {Direction.UP.value}")
print(f"DOWN value: {Direction.DOWN.value}")
print(f"LEFT value: {Direction.LEFT.value}")
print(f"RIGHT value: {Direction.RIGHT.value}")
print(f"NONE value: {Direction.NONE.value}")

print("\nTestando métodos:")
print(f"UP.is_vertical(): {Direction.UP.is_vertical()}")
print(f"RIGHT.is_horizontal(): {Direction.RIGHT.is_horizontal()}")
print(f"UP.is_horizontal(): {Direction.UP.is_horizontal()}")

print("\nTestando Direction.from_keys():")
keys = pygame.key.get_pressed()  # Usa a função correta
print(f"Sem nenhuma tecla pressionada: {Direction.from_keys(keys)}")

print("\nTeste concluído com sucesso!")

