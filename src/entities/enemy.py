"""Sistema de entidade inimiga"""
import pygame


class Enemy:
    def __init__(self, x, y, speed=1, is_strong=False, is_boss=False, boss_width=None, boss_height=None, boss_health=None):
        self.x = x
        self.y = y
        self.speed = speed
        self.is_strong = is_strong
        self.is_boss = is_boss

        # Tamanho do inimigo
        if is_boss:
            self.width = boss_width or 100
            self.height = boss_height or 150
        else:
            self.width = 68
            self.height = 85

        # Carrega a imagem do inimigo
        try:
            from config import ENEMY_IMAGE
            image_path = ENEMY_IMAGE
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except (pygame.error, FileNotFoundError) as e:
            self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            self.image.fill((255, 0, 0))  # cor de reserva se não conseguir carregar imagem
            print(f"Erro ao carregar imagem de inimigo '{image_path}': {e}")

        # Vida do inimigo
        if is_boss:
            self.health = boss_health or 48
        elif is_strong:
            self.health = 5
        else:
            self.health = 2

        self.rect = pygame.Rect(self.x + 10, self.y + 10, self.width - 20, self.height - 20)

    def take_damage(self):
        self.health -= 1
        return self.health <= 0

    def move_towards_hero(self, hero_x, hero_y):
        if self.x < hero_x:
            self.x += self.speed
        elif self.x > hero_x:
            self.x -= self.speed

        if self.y < hero_y:
            self.y += self.speed
        elif self.y > hero_y:
            self.y -= self.speed

        self.rect.topleft = (self.x + 10, self.y + 10)

    def move_down(self):
        self.y += self.speed

        self.rect.topleft = (self.x + 10, self.y + 10)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))