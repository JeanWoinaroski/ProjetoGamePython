"""Power-ups temporários coletáveis"""
import pygame
import random


class PowerUp:
    def __init__(self, x, y, power_type=None):
        self.x = x
        self.y = y
        self.power_type = power_type or random.choice(['speed_boost', 'shield', 'damage_boost', 'health_regen'])

        # Define propriedades baseadas no tipo
        self.effects = {
            'speed_boost': {'duration': 10000, 'speed_multiplier': 2.0, 'color': (0, 255, 0)},  # Verde
            'shield': {'duration': 8000, 'invincible': True, 'color': (0, 0, 255)},  # Azul
            'damage_boost': {'duration': 12000, 'damage_multiplier': 1.5, 'color': (255, 0, 0)},  # Vermelho
            'health_regen': {'duration': 0, 'heal_amount': 2, 'color': (255, 255, 0)}  # Amarelo
        }

        self.color = self.effects[self.power_type]['color']
        self.size = 20
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

        # Animação pulsante
        self.pulse_timer = 0
        self.pulse_speed = 0.1

    def update(self):
        """Animação pulsante"""
        self.pulse_timer += self.pulse_speed
        scale = 1 + 0.2 * abs(pygame.math.Vector2(0, 1).rotate(self.pulse_timer * 10).y)

        # Atualiza tamanho baseado na pulsação
        current_size = int(self.size * scale)
        self.rect = pygame.Rect(
            self.x - (current_size - self.size) // 2,
            self.y - (current_size - self.size) // 2,
            current_size,
            current_size
        )

    def draw(self, window):
        """Desenha o power-up com efeito visual"""
        # Círculo pulsante
        pygame.draw.circle(window, self.color, self.rect.center, self.rect.width // 2)

        # Brilho interno
        inner_color = tuple(min(255, c + 50) for c in self.color)
        pygame.draw.circle(window, inner_color, self.rect.center, self.rect.width // 4)

        # Ícone baseado no tipo
        icon_size = self.rect.width // 3
        if self.power_type == 'speed_boost':
            # Seta para velocidade
            points = [
                (self.rect.centerx, self.rect.centery - icon_size),
                (self.rect.centerx - icon_size, self.rect.centery + icon_size),
                (self.rect.centerx + icon_size, self.rect.centery + icon_size)
            ]
        elif self.power_type == 'shield':
            # Escudo circular
            pygame.draw.circle(window, (255, 255, 255), self.rect.center, icon_size)
        elif self.power_type == 'damage_boost':
            # Raio
            pygame.draw.line(window, (255, 255, 255),
                           (self.rect.centerx - icon_size, self.rect.centery - icon_size),
                           (self.rect.centerx + icon_size, self.rect.centery + icon_size), 2)
            pygame.draw.line(window, (255, 255, 255),
                           (self.rect.centerx + icon_size, self.rect.centery - icon_size),
                           (self.rect.centerx - icon_size, self.rect.centery + icon_size), 2)
        elif self.power_type == 'health_regen':
            # Cruz de vida
            pygame.draw.line(window, (255, 255, 255),
                           (self.rect.centerx, self.rect.centery - icon_size),
                           (self.rect.centerx, self.rect.centery + icon_size), 2)
            pygame.draw.line(window, (255, 255, 255),
                           (self.rect.centerx - icon_size, self.rect.centery),
                           (self.rect.centerx + icon_size, self.rect.centery), 2)

    def get_effect(self):
        """Retorna os efeitos do power-up"""
        return self.effects[self.power_type]