"""Entidade do personagem herói/jogador"""
import pygame
import sys
from src.systems import Direction
from .bullet import Bullet
from .laser import Laser


class Heroi:
    """Representa o jogador (ninja) com movimento, tiro e sistema de vida"""

    def __init__(self, x, y, speed, image_path):

        # Posição inicial na tela
        self.x = x
        self.y = y

        # Velocidade de movimento
        self.speed = speed

        # Direção que está olhando (esquerda ou direita)
        self.is_leftside = True

        # ❤️ SISTEMA DE VIDA
        self.max_health = 5
        self.health = self.max_health

        # RPG - SISTEMA DE EXPERIÊNCIA E NÍVEL
        self.level = 1
        self.exp = 0
        self.exp_to_next = 100
        self.current_weapon = 'basic_gun'  # Arma que está usando agora

        # TAMANHO DAS BALAS - cresce com o nível
        self.bullet_size = 10

        # 💥 EFEITO VISUAL QUANDO LEVA DANO (PISCAR)
        self.is_hit = False
        self.hit_timer = 0
        self.hit_duration = 300  # milissegundos que dura o efeito

        # 🛡️ SISTEMA DE BUFFS TEMPORÁRIOS
        self.active_buffs = {}  # {'buff_type': {'end_time': timestamp, 'effect': value}}
        self.invincible = False

        try:
            self.image_original = pygame.image.load(image_path).convert_alpha()
            self.image_original = pygame.transform.smoothscale(self.image_original, (48, 48))
            self.image = self.image_original.copy()

        except (pygame.error, FileNotFoundError) as e:
            print(f"Erro ao carregar imagem do herói '{image_path}': {e}")
            pygame.quit()
            sys.exit(1)

        # Hitbox menor que a imagem (para colisão mais precisa)
        self.rect = pygame.Rect(self.x + 10, self.y + 10, 28, 28)

    # 🔥 MÉTODO FORA DO __init__ PARA ATUALIZAR EFEITOS
    def update(self):
        """Atualiza o efeito de dano (fazer o personagem piscar) e buffs temporários"""
        current_time = pygame.time.get_ticks()

        # Atualiza efeito de dano
        if self.is_hit:
            if current_time - self.hit_timer > self.hit_duration:
                self.is_hit = False

        # Atualiza buffs temporários
        expired_buffs = []
        for buff_type, buff_data in self.active_buffs.items():
            if current_time > buff_data['end_time']:
                expired_buffs.append(buff_type)

        # Remove buffs expirados
        for buff_type in expired_buffs:
            self.remove_buff(buff_type)

    def apply_buff(self, buff_type, effect_data):
        """Aplica um buff temporário ao herói"""
        current_time = pygame.time.get_ticks()

        if buff_type == 'health_regen':
            # Regeneração instantânea
            self.health = min(self.max_health, self.health + effect_data.get('heal_amount', 1))
        else:
            # Buffs temporários
            duration = effect_data.get('duration', 5000)
            self.active_buffs[buff_type] = {
                'end_time': current_time + duration,
                'effect': effect_data
            }

            # Aplica efeito imediato
            if buff_type == 'speed_boost':
                pass  # Velocidade é aplicada no movimento
            elif buff_type == 'shield':
                self.invincible = True
            elif buff_type == 'damage_boost':
                pass  # Dano é aplicado no tiro

    def remove_buff(self, buff_type):
        """Remove um buff específico"""
        if buff_type in self.active_buffs:
            del self.active_buffs[buff_type]

            # Remove efeitos
            if buff_type == 'shield':
                self.invincible = False

    def get_current_speed(self):
        """Retorna velocidade atual considerando buffs"""
        base_speed = self.speed
        if 'speed_boost' in self.active_buffs:
            multiplier = self.active_buffs['speed_boost']['effect'].get('speed_multiplier', 1.0)
            base_speed *= multiplier
        return base_speed

    def get_current_damage(self):
        """Retorna multiplicador de dano atual"""
        multiplier = 1.0
        if 'damage_boost' in self.active_buffs:
            multiplier *= self.active_buffs['damage_boost']['effect'].get('damage_multiplier', 1.0)
        return multiplier

    def move(self, keys):
        current_speed = self.get_current_speed()

        if keys[pygame.K_a]:
            self.x -= current_speed
            if self.is_leftside:
                self.image = self.image_original.copy()
                self.is_leftside = False

        if keys[pygame.K_d]:
            self.x += current_speed
            if not self.is_leftside:
                self.image = pygame.transform.flip(self.image_original, True, False)
                self.is_leftside = True

        if keys[pygame.K_w]:
            self.y -= current_speed

        if keys[pygame.K_s]:
            self.y += current_speed

        # Atualiza a posição da hitbox junto com o personagem
        self.rect.topleft = (self.x + 10, self.y + 10)

    def take_damage(self, amount=1):
        if self.invincible:
            return False  # Não toma dano se estiver invencível

        self.health -= amount

        # 💥 ATIVA O EFEITO DE PISCAR
        self.is_hit = True
        self.hit_timer = pygame.time.get_ticks()

        # RPG: perde experiência quando leva dano
        self.exp = max(0, self.exp - 5)

        if self.health <= 0:
            self.health = 0
            return True

        return False

    def gain_exp(self, amount):
        """Ganha pontos de experiência e verifica se sobe de nível"""
        self.exp += amount
        while self.exp >= self.exp_to_next:
            self.level_up()

    def level_up(self):
        """Sobe um nível no jogo"""
        self.exp -= self.exp_to_next
        self.level += 1
        self.exp_to_next = int(self.exp_to_next * 1.5)  # Experiência necessária aumenta
        self.max_health += 2
        self.health = self.max_health  # Cura completamente
        self.speed += 0.5  # Fica mais rápido
        self.bullet_size += 5  # Balas ficam maiores

    def equip_weapon(self, weapon_type):
        """Equipa uma nova arma no personagem"""
        self.current_weapon = weapon_type

    def shoot(self, direction, screen_width=1360, screen_height=920):
        """Cria e retorna projéteis na direção que o jogador apontou"""
        projectiles = []

        if self.current_weapon == 'laser_gun':
            # MODO LASER
            if direction == Direction.UP:
                start_x, start_y = self.x + 24, self.y
            elif direction == Direction.DOWN:
                start_x, start_y = self.x + 24, self.y + 48
            elif direction == Direction.LEFT:
                start_x, start_y = self.x, self.y + 24
            elif direction == Direction.RIGHT:
                start_x, start_y = self.x + 48, self.y + 24

            projectiles.append(Laser(start_x, start_y, direction, screen_width, screen_height))

        elif self.current_weapon == 'spread_gun':
            # MODO ESPALHAR - 3 balas em leque
            if direction in [Direction.UP, Direction.DOWN]:
                # Espalhar na vertical
                for offset in [-10, 0, 10]:
                    if direction == Direction.UP:
                        bx, by = self.x + 24 - self.bullet_size//2 + offset, self.y - self.bullet_size
                    else:
                        bx, by = self.x + 24 - self.bullet_size//2 + offset, self.y + 48
                    projectiles.append(Bullet(bx, by, direction, size=self.bullet_size))
            else:
                # Espalhar na horizontal
                for offset in [-10, 0, 10]:
                    if direction == Direction.LEFT:
                        bx, by = self.x - self.bullet_size, self.y + 24 - self.bullet_size//2 + offset
                    else:
                        bx, by = self.x + 48, self.y + 24 - self.bullet_size//2 + offset
                    projectiles.append(Bullet(bx, by, direction, size=self.bullet_size))

        else:  # basic_gun
            # BALAS NORMAIS
            if direction == Direction.UP:
                bx, by = self.x + 24 - self.bullet_size//2, self.y - self.bullet_size
            elif direction == Direction.DOWN:
                bx, by = self.x + 24 - self.bullet_size//2, self.y + 48
            elif direction == Direction.LEFT:
                bx, by = self.x - self.bullet_size, self.y + 24 - self.bullet_size//2
            elif direction == Direction.RIGHT:
                bx, by = self.x + 48, self.y + 24 - self.bullet_size//2

            projectiles.append(Bullet(bx, by, direction, size=self.bullet_size))

        return projectiles

    # 🔥 DESENHO COM EFEITO DE PISCAR
    def draw(self, surface):
        if self.is_hit:
            # pisca (aparece e desaparece rapidamente)
            if pygame.time.get_ticks() % 200 < 100:
                surface.blit(self.image, (self.x, self.y))
        else:
            surface.blit(self.image, (self.x, self.y))