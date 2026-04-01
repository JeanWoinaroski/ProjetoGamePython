# ==========================================
# CONFIGURAÇÕES GLOBAIS DO JOGO
# ==========================================

# Dimensões da tela
SCREEN_WIDTH = 1360
SCREEN_HEIGHT = 920

# Título base da janela (será atualizado dinamicamente com o estágio)
WINDOW_TITLE_BASE = "Space Defender"

# FPS
TARGET_FPS = 60

# ==========================================
# CONFIGURAÇÕES DO HERÓI
# ==========================================
HERO_SPEED = 2

# ==========================================
# CONFIGURAÇÕES DE COMBATE
# ==========================================
SHOT_COOLDOWN = 200  # ms entre tiros

# ==========================================
# CONFIGURAÇÕES DE INIMIGOS
# ==========================================
ENEMY_BASE_SPEED = 1.5
ENEMY_BOSS_SPEED = 1.5

BOSS_WAVE_INTERVAL = 5

# ==========================================
# PATHS DE IMAGENS
# ==========================================
ASSETS_PATH = "assets/images/"
HERO_IMAGE = ASSETS_PATH + "Ninja.png"
ENEMY_IMAGE = ASSETS_PATH + "pngegg.png"
ITEM_IMAGE_BASIC_GUN = ASSETS_PATH + "basic_gun.png"
ITEM_IMAGE_LASER_GUN = ASSETS_PATH + "laser_gun.png"
ITEM_IMAGE_SPREAD_GUN = ASSETS_PATH + "spread_gun.png"
MAP_BACKGROUND_IMAGE = None  # Ajuste aqui se usar imagem de background

# ==========================================
# PATHS DE SONS E MÚSICA
# ==========================================
SOUNDS_PATH = "assets/sounds/"
BACKGROUND_MUSIC = SOUNDS_PATH + "final_fantasy_theme.mp3"  # Música de fundo estilo Final Fantasy

# ==========================================
UI_BAR_WIDTH = 300
UI_BAR_HEIGHT = 20
SPAWN_COOLDOWN = 1500  # ms entre spawns
WAVE_DISPLAY_DURATION = 3000  # ms mostrando a onda
BOSS_WAVE_INTERVAL = 5  # a cada 5 ondas tem chefe

# ==========================================
# CONFIGURAÇÕES DE PONTUAÇÃO
# ==========================================
SCORE_ENEMY_NORMAL = 50
SCORE_ENEMY_STRONG = 100
SCORE_ENEMY_BOSS = 1000

# ==========================================
# CORES
# ==========================================
COLOR_BACKGROUND = (0, 0, 0)
COLOR_ENEMY_NORMAL = (255, 0, 0)
COLOR_ENEMY_STRONG = (255, 100, 100)
COLOR_ENEMY_BOSS = (255, 215, 0)
COLOR_TEXT_PRIMARY = (255, 255, 0)
COLOR_TEXT_SECONDARY = (100, 255, 100)
COLOR_SCORE = (0, 255, 0)

# ==========================================
# TAMANHOS DE FONTE
# ==========================================
FONT_SIZE_SMALL = 36
FONT_SIZE_MEDIUM = 60
FONT_SIZE_LARGE = 120
