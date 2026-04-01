"""Motor principal do jogo e controlador"""
import pygame
import random
from src.entities import Heroi, Enemy, Bullet, Item, Laser, PowerUp
from src.world import Map
from src.systems import Direction
from levels.level1 import TILE_SIZE, MAP_TILE_AMOUNT, tile_data, tile_images, solid_tiles, background_image, get_map_for_progress
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WINDOW_TITLE_BASE,
    TARGET_FPS,
    HERO_SPEED,
    SHOT_COOLDOWN,
    BOSS_WAVE_INTERVAL,
    COLOR_BACKGROUND,
    BACKGROUND_MUSIC,
)


class Game:
    # Removido singleton pattern para evitar problemas de inicialização
    
    def __init__(self):
        # Removida verificação de singleton para permitir múltiplas instâncias
            # Inicializar pygame primeiro
            pygame.init()
            
            # Inicializamos com tamanhos de tela padrão, mas vamos ajustar
            # para ficar exato ao número de tiles (simetria 10x10, 9x9 etc).
            tile_cols, tile_rows = MAP_TILE_AMOUNT
            dynamic_tile_size = min(
                SCREEN_WIDTH // tile_cols,
                SCREEN_HEIGHT // tile_rows
            )
            dynamic_tile_size = max(dynamic_tile_size, 32)

            self.screen_width = tile_cols * dynamic_tile_size
            self.screen_height = tile_rows * dynamic_tile_size

            self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
            pygame.display.set_caption(WINDOW_TITLE_BASE)
            self.relogio = pygame.time.Clock()
            
            # Inicializar módulos necessários
            pygame.font.init()
            pygame.mixer.init()
            
            # CARREGA E TOCA A MÚSICA DE FUNDO
            try:
                pygame.mixer.music.load(BACKGROUND_MUSIC)
                pygame.mixer.music.play(-1)  # -1 = loop infinito
                pygame.mixer.music.set_volume(0.3)  # Volume baixo (30%)
                print("Musica de fundo carregada com sucesso!")
            except (pygame.error, FileNotFoundError) as e:
                print(f"AVISO: Nao foi possivel carregar a musica de fundo: {e}")
                print("Para adicionar musica, coloque um arquivo MP3 em assets/sounds/final_fantasy_theme.mp3")
            
            # Inicializar fonte
            self.font = pygame.font.Font(None, 36)
            self.big_font = pygame.font.Font(None, 72)  # Fonte grande para o estágio

            

            # Cria o herói com velocidade configurável e imagem padrão
            self.heroi = Heroi(200, 200, HERO_SPEED, 'assets/images/Ninja.png')

            # Contador de bosses derrotados para mudança de mapa
            self.bosses_defeated = 0

            # Armazenar o tile_size calculado
            self.tile_size = dynamic_tile_size

            # Inicializa o mapa baseado no progresso atual (0 bosses)
            self.update_map_based_on_progress()

            # ❤️ CONTROLE DE DANO
            self.last_hit_time = 0
            self.hit_cooldown = 1000

            self.wave = 1
            self.wave_spawned = False
            self.enemies = []
            self.spawn_wave()

            self.bullets = []
            self.items = []  # Armas coletáveis
            self.powerups = []  # Power-ups temporários
            self.lasers = []  # lasers
            # Não spawna armas inicialmente
            
            self.game_over = False  # Flag para game over
            
            # Define título inicial
            self.update_window_title()

    def spawn_wave(self):
        num_enemies = 4 if self.wave % BOSS_WAVE_INTERVAL != 0 else 1
        for _ in range(num_enemies):
            # Aparece inimigos nas bordas da tela de forma aleatória
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                x = random.randint(0, self.screen_width - 48)
                y = -48
            elif side == 'bottom':
                x = random.randint(0, self.screen_width - 48)
                y = self.screen_height
            elif side == 'left':
                x = -48
                y = random.randint(0, self.screen_height - 48)
            elif side == 'right':
                x = self.screen_width
                y = random.randint(0, self.screen_height - 48)
            
            if self.wave % BOSS_WAVE_INTERVAL == 0:
                # Chefão cresce: a cada 10 ondas, aumenta tamanho e vida
                scale_factor = self.wave // 10
                boss_width = 100 + scale_factor * 20
                boss_height = 150 + scale_factor * 30
                boss_health = 48 + scale_factor * 10  # Vida base 48, +10 a cada 10 ondas
                self.enemies.append(Enemy(x, y, speed=1.5, is_boss=True, boss_width=boss_width, boss_height=boss_height, boss_health=boss_health))
            else:
                self.enemies.append(Enemy(x, y))

        self.wave_spawned = True

    def spawn_items(self):
        """Spawna uma arma coletável ou power-up"""
        if random.random() < 0.7:  # 70% chance de arma, 30% de power-up
            weapon_types = ['basic_gun', 'laser_gun', 'spread_gun']
            weapon_type = random.choice(weapon_types)
            x = random.randint(100, self.screen_width - 100)
            y = random.randint(100, self.screen_height - 100)
            self.items.append(Item(x, y, weapon_type))
        else:
            # Spawna power-up
            x = random.randint(100, self.screen_width - 100)
            y = random.randint(100, self.screen_height - 100)
            self.powerups.append(PowerUp(x, y))

    def check_wave_clear(self):
        if self.wave_spawned and len(self.enemies) == 0:
            if self.wave % BOSS_WAVE_INTERVAL == 0:
                # Depois de matar o chefão, aparece uma arma nova
                self.spawn_items()
            self.wave += 1
            self.spawn_wave()

    def update_map_based_on_progress(self):
        """Atualiza o mapa baseado no número de bosses derrotados"""
        # Obtém o layout do mapa apropriado
        current_map_data = get_map_for_progress(self.bosses_defeated)

        # Recria o mapa com o novo layout
        self.mapa = Map(
            tile_data=current_map_data,
            tile_images=tile_images,
            solid_tiles=solid_tiles,
            tile_size=self.tile_size,
            map_tile_amount=MAP_TILE_AMOUNT,
            background_image=background_image,
            screen_width=self.screen_width,
            screen_height=self.screen_height
        )

    def update_window_title(self):
        """Muda o título da janela para mostrar a onda atual"""
        title = f"{WINDOW_TITLE_BASE} - Wave {self.wave}"
        pygame.display.set_caption(title)

    def toggle_music(self):
        """Pausa ou retoma a música de fundo (tecla M)"""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def run(self):
        app_running = True
        last_shot = 0

        while app_running:
            current_time = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    app_running = False
                elif event.type == pygame.KEYDOWN:
                    if self.game_over:
                        if event.key == pygame.K_r:
                            # Reinicia o jogo criando uma nova instância
                            return "restart"  # Sinal para reiniciar
                        elif event.key == pygame.K_ESCAPE:
                            app_running = False
                    else:
                        # CONTROLE DA MÚSICA (tecla M)
                        if event.key == pygame.K_m:
                            self.toggle_music()

            if not self.game_over:
                keys = pygame.key.get_pressed()

                # Movimento com verificação de colisão no mapa
                previous_x, previous_y = self.heroi.x, self.heroi.y
                self.heroi.move(keys)
                self.heroi.rect.topleft = (self.heroi.x + 10, self.heroi.y + 10)
                if self.mapa.collide_detection(self.heroi.rect):
                    self.heroi.x, self.heroi.y = previous_x, previous_y
                    self.heroi.rect.topleft = (self.heroi.x + 10, self.heroi.y + 10)

                self.heroi.update()

                # Atualiza power-ups (animação pulsante)
                for powerup in self.powerups:
                    powerup.update()

                # Limites da tela/mapa
                max_x = min(self.screen_width, self.mapa.map_pixel_width) - 48
                max_y = min(self.screen_height, self.mapa.map_pixel_height) - 48
                self.heroi.x = max(0, min(self.heroi.x, max_x))
                self.heroi.y = max(0, min(self.heroi.y, max_y))
                self.heroi.rect.topleft = (self.heroi.x + 10, self.heroi.y + 10)

                # Atirar
                direction = Direction.from_keys(keys)
                if direction != Direction.NONE and current_time - last_shot > SHOT_COOLDOWN:
                    projectiles = self.heroi.shoot(direction, self.screen_width, self.screen_height)
                    for projectile in projectiles:
                        if isinstance(projectile, Laser):
                            self.lasers.append(projectile)
                        else:
                            self.bullets.append(projectile)
                    last_shot = current_time

                # Balas se movem
                for bullet in self.bullets[:]:
                    bullet.move()
                    if bullet.is_off_screen(self.screen_width, self.screen_height):
                        self.bullets.remove(bullet)

                # Lasers são atualizados (verifica duração)
                for laser in self.lasers[:]:
                    laser.update()

            # RPG: Lasers causam dano instantâneo, desaparecem depois da duração
            for laser in self.lasers[:]:
                hit_enemies = laser.check_collision(self.enemies)
                for enemy in hit_enemies:
                    if enemy.take_damage():
                        if enemy.is_boss:
                            self.bosses_defeated += 1
                            self.update_map_based_on_progress()  # Atualiza mapa quando boss é derrotado
                        self.enemies.remove(enemy)
                        self.heroi.gain_exp(10)
                # Remove laser se não estiver mais ativo (duração expirou)
                if not laser.active:
                    self.lasers.remove(laser)

            if not self.game_over:
                # Inimigos se movem
                for enemy in self.enemies:
                    enemy.move_towards_hero(self.heroi.x, self.heroi.y)

                # 💥 DANO POR PROXIMIDADE
                for enemy in self.enemies:
                    dx = enemy.x - self.heroi.x
                    dy = enemy.y - self.heroi.y
                    distancia = (dx**2 + dy**2) ** 0.5

                    if distancia < 40:
                        if current_time - self.last_hit_time > self.hit_cooldown:
                            self.heroi.take_damage(1)
                            self.last_hit_time = current_time
                            if self.heroi.health <= 0:
                                self.game_over = True

                # RPG: Colisão com itens (armas)
                for item in self.items[:]:
                    if self.heroi.rect.colliderect(item.rect):
                        self.heroi.equip_weapon(item.item_type)
                        self.items.remove(item)

                # 🛡️ Colisão com power-ups
                for powerup in self.powerups[:]:
                    if self.heroi.rect.colliderect(powerup.rect):
                        effect = powerup.get_effect()
                        self.heroi.apply_buff(powerup.power_type, effect)
                        self.powerups.remove(powerup)

                # Colisão bala
                for bullet in self.bullets[:]:
                    for enemy in self.enemies[:]:
                        if bullet.rect.colliderect(enemy.rect):
                            if enemy.take_damage():
                                if enemy.is_boss:
                                    self.bosses_defeated += 1
                                    self.update_map_based_on_progress()  # Atualiza mapa quando boss é derrotado
                                self.enemies.remove(enemy)
                                self.heroi.gain_exp(10)  # RPG: ganha experiência
                            
                            if bullet in self.bullets:
                                self.bullets.remove(bullet)
                            break

                self.check_wave_clear()
                
                # Atualiza título da janela com o estágio atual
                self.update_window_title()

            # DESENHAR NA TELA
            self.window.fill(COLOR_BACKGROUND)
            self.mapa.draw(self.window)

            for enemy in self.enemies:
                enemy.draw(self.window)

            for bullet in self.bullets:
                bullet.draw(self.window)

            # RPG: Desenha lasers
            for laser in self.lasers:
                laser.draw(self.window)

            # RPG: Desenha itens
            for item in self.items:
                item.draw(self.window)

            # 🛡️ Desenha power-ups
            for powerup in self.powerups:
                powerup.draw(self.window)

            self.heroi.draw(self.window)

            self.draw_ui()

            pygame.display.update()
            self.relogio.tick(TARGET_FPS)

        # PARA A MÚSICA QUANDO O JOGO ACABAR
        pygame.mixer.music.stop()
        pygame.quit()
        return None  # Retorno normal

    def draw_ui(self):
        if self.game_over:
            # Tela de fim de jogo
            game_over_text = self.big_font.render("GAME OVER", True, (255, 0, 0))
            restart_text = self.font.render("Pressione R para reiniciar ou ESC para sair", True, (255, 255, 255))
            
            # Centralizar
            go_x = self.screen_width // 2 - game_over_text.get_width() // 2
            go_y = self.screen_height // 2 - game_over_text.get_height() // 2 - 50
            self.window.blit(game_over_text, (go_x, go_y))
            
            rt_x = self.screen_width // 2 - restart_text.get_width() // 2
            rt_y = go_y + game_over_text.get_height() + 20
            self.window.blit(restart_text, (rt_x, rt_y))
        else:
            # Fundo semi-transparente removido - só mostra o texto

            vida_texto = self.font.render(f"VIDA: {self.heroi.health}/{self.heroi.max_health}", True, (255, 0, 0))
            self.window.blit(vida_texto, (50, 50))
            
            # RPG: Mostra nível e experiência
            level_texto = self.font.render(f"LEVEL: {self.heroi.level}", True, (0, 255, 0))
            self.window.blit(level_texto, (50, 80))
            
            exp_texto = self.font.render(f"EXP: {self.heroi.exp}/{self.heroi.exp_to_next}", True, (0, 255, 0))
            self.window.blit(exp_texto, (50, 110))
            
            # RPG: Mostra arma atual
            weapon_texto = self.font.render(f"ARMA: {self.heroi.current_weapon.replace('_', ' ').title()}", True, (255, 255, 0))
            self.window.blit(weapon_texto, (50, 140))

            # 🛡️ Mostra buffs ativos
            buff_y = 170
            current_time = pygame.time.get_ticks()
            for buff_type, buff_data in self.heroi.active_buffs.items():
                remaining_time = max(0, (buff_data['end_time'] - current_time) // 1000)
                buff_name = buff_type.replace('_', ' ').title()
                buff_texto = self.font.render(f"{buff_name}: {remaining_time}s", True, buff_data['effect'].get('color', (255, 255, 255)))
                self.window.blit(buff_texto, (50, buff_y))
                buff_y += 30

            # Mostra a onda atual no centro da tela com transparência
            stage_texto = self.big_font.render(f"WAVE {self.wave}", True, (255, 255, 0))
            text_width = stage_texto.get_width()
            text_height = stage_texto.get_height()
            center_x = self.screen_width // 2 - text_width // 2
            center_y = self.screen_height // 2 - text_height // 2
            # Cria superfície transparente para o texto
            text_surface = pygame.Surface((text_width, text_height), pygame.SRCALPHA)
            text_surface.blit(stage_texto, (0, 0))
            # Aplica transparência (alpha 200 de 255)
            text_surface.set_alpha(200)
            self.window.blit(text_surface, (center_x, center_y))