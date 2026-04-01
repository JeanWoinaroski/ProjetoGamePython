# 🏗️ Arquitetura do Projeto - Documentação

## Visão Geral

Este projeto segue a arquitetura **Object-Oriented Game Development** com separação clara de responsabilidades e padrão de design baseado em componentes.

## 📚 Estrutura de Módulos

### 1. **src/core/** - Game Engine Principal

**Responsabilidade**: Loop principal do jogo, gerenciamento de estado e coordenação de sistemas.

#### `game.py` - Classe Game
```python
Game:
  ├── __init__()           # Inicializa window, fonts, entities
  ├── run()                # Main loop (60 FPS)
  ├── spawn_wave()         # Wave spawning system
  ├── check_wave_clear()   # Wave clear detection
  ├── draw_ui()            # UI rendering
  └── draw_wave_display()  # Epic wave transitions
```

**Responsabilidades**:
- Loop principal (input → update → render)
- Gerenciamento de entidades (heroi, enemies, bullets)
- Colisão (bullet vs enemy)
- Sistema de ondas

---

### 2. **src/entities/** - Objetos do Jogo

**Responsabilidade**: Classe de entidades do jogo - cada uma gerencia seu próprio estado e renderização.

#### `heroi.py` - Classe Heroi (Player)
```python
Heroi:
  ├── x, y, speed         # Position and movement
  ├── image, is_leftside  # Rendering
  ├── move(keys)          # Handle WASD input
  └── shoot(direction)    # Bullet spawn position
```

**Características**:
- Movimento WASD (A, D, W, S)
- Sprite flipping automático
- Bounds checking (limites da tela)

#### `enemy.py` - Classe Enemy
```python
Enemy:
  ├── x, y, speed          # Position and movement
  ├── health, width, height # Stats and size
  ├── color, is_strong, is_boss
  ├── take_damage()         # Damage system
  ├── move_towards_hero()   # AI (pathfinding simples)
  └── draw()                # Rendering com contornos
```

**Tipos**:
- **Normal**: 1 HP, speed=1.5, vermelho
- **Strong**: 2 HP, speed=2, rosa
- **Boss**: 8 HP, speed=1.5, dourado (80x100px)

#### `bullet.py` - Classe Bullet
```python
Bullet:
  ├── x, y, direction, speed  # Position and movement
  ├── move()                  # Update position
  ├── draw()                  # Render
  └── is_off_screen()         # Cleanup detection
```

---

### 3. **src/systems/** - Sistemas Auxiliares

**Responsabilidade**: Systems e utilities reutilizáveis.

#### `direction.py` - Direction Enum
```python
Direction (Enum):
  ├── UP, DOWN, LEFT, RIGHT, NONE
  ├── from_keys()           # Map keyboard input to Direction
  ├── is_vertical()         # Check if vertical
  └── is_horizontal()       # Check if horizontal
```

**Uso**:
```python
direction = Direction.from_keys(pygame.key.get_pressed())
if direction == Direction.UP:
    # Shoot up
```

---

### 4. **src/world/** - Sistema de Mapa/Mundo

**Responsabilidade**: Tile-based world rendering e collision detection.

#### `tile.py` - Classe Tile
```python
Tile:
  ├── x, y, width, height      # Position and size
  ├── image or color           # Rendering
  ├── draw()                   # Render tile
  └── colliderect(rect)        # Collision check
```

#### `map.py` - Classe Map
```python
Map:
  ├── tiles (list)             # All tiles
  ├── solid_tiles (list)       # Collidable tile types
  ├── draw()                   # Render all tiles
  └── collide_detection(rect)  # Check collisions
```

**Dados**: Carregados de `levels/level1.py`

---

### 5. **levels/** - Definição de Níveis

#### `level1.py`
```python
tile_data = [
    [0, 0, 1, 1, ...],  # 2D array of tile IDs
    [0, 2, 0, 0, ...],  # 0=grass, 1=wall, 2=water
    ...
]

tile_images = {
    0: (0, 255, 0),      # Green (grass)
    1: (128, 128, 128),  # Gray (wall)
    2: (0, 0, 255)       # Blue (water)
}

solid_tiles = [1]  # Only tile ID 1 is solid
```

---

## 🔄 Fluxo de Dados

### Game Loop (60 FPS)

```
┌─────────────────────────────────────────┐
│           pygame.event.get()            │ INPUT
├─────────────────────────────────────────┤
│      pygame.key.get_pressed()           │
│      heroi.move(keys)                   │
├─────────────────────────────────────────┤
│      heroi position = clamp bounds      │ UPDATE
│      Direction.from_keys()              │
│      enemy.move_towards_hero()          │
│      bullet.move()                      │
│      check collisions                   │
│      check_wave_clear()                 │
├─────────────────────────────────────────┤
│      mapa.draw()                        │ RENDER
│      enemy.draw()                       │
│      bullet.draw()                      │
│      heroi.draw()                       │
│      draw_ui()                          │
│      draw_wave_display()                │
│      pygame.display.update()            │
└─────────────────────────────────────────┘
         tick(60)  ↲
```

### Collision Detection

```
For each bullet:
  For each enemy:
    if bullet.rect.colliderect(enemy.rect):
      if enemy.take_damage():  # Returns True if dead
        enemies.remove(enemy)
        score += points
      bullets.remove(bullet)
      break
```

### Wave Progression

```
Wave 1: 4 enemies (3 + wave)
Wave 2: 5 enemies (3 + wave), 1 strong
Wave 3: 6 enemies (3 + wave), 1 strong
...
Wave 5: 1 BOSS ⚔️ (is_boss_wave = wave % 5 == 0)
```

---

## 📊 State Management

### Game State

```python
self.wave              # Current wave number
self.score             # Total score
self.kills             # Total enemies killed
self.enemies           # List of active enemies
self.bullets           # List of active bullets
self.wave_start_time   # Timestamp of wave start
self.wave_spawned      # Boolean flag
```

### Entity State

**Heroi**:
- x, y (position)
- image, is_leftside (rendering)

**Enemy**:
- x, y (position)
- health (current HP)
- is_strong, is_boss (type flags)
- rect (collision rect)

**Bullet**:
- x, y (position)
- direction (UP/DOWN/LEFT/RIGHT)
- rect (collision rect)

---

## 🎨 Rendering Pipeline

```
self.window.fill((0, 0, 0))      # Black background

mapa.draw()                       # Layer 0: Tiles
for enemy: enemy.draw()           # Layer 1: Enemies
for bullet: bullet.draw()         # Layer 2: Bullets
blit(heroi.image, heroi.pos)      # Layer 3: Hero

draw_ui()                         # Layer 4: UI
draw_wave_display()               # Layer 5: Overlays

pygame.display.update()           # Flip buffers
```

---

## 🔌 Dependency Injection Pattern

```
main.py
  └─→ Game()
       ├─→ Map(tile_data, tile_images, solid_tiles)
       ├─→ Heroi(x, y, speed, image_path)
       ├─→ Enemy(x, y, speed, is_strong, is_boss)
       └─→ Bullet(x, y, direction)
```

**Loose coupling**: Game creates instances, doesn't hard-code dependencies.

---

## 📈 Extensibility Points

### Fácil adicionar:

1. **Novo tipo de inimigo**:
```python
# Adicionar um novo tipo em Enemy.__init__()
if is_elite:
    self.health = 4
    self.color = (255, 165, 0)  # Orange
```

2. **Novo sistema de power-ups**:
```python
# Criar src/systems/powerup.py
class PowerUp:
    def __init__(self, x, y, type):
        self.type = type  # SPEED, AMMO, HEALTH
        self.collected = False
```

3. **Múltiplos níveis**:
```python
# Adicionar levels/level2.py, level3.py
# Carregar em Game.__init__():
if level == 1:
    from levels.level1 import tile_data
elif level == 2:
    from levels.level2 import tile_data
```

4. **Sistema de Som**:
```python
# Criar src/systems/audio.py
class AudioManager:
    def play_sound(self, sound_name):
        pygame.mixer.Sound(...).play()
```

---

## ⚡ Performance Optimizations

- **Rect caching**: Atualizar `rect` após movimento para colisão rápida
- **List slicing**: `for bullet in self.bullets[:]` para modificar durante iteração
- **FPS cap**: `clock.tick(60)` para controlar CPU
- **Rendering order**: Draw background first, UI last

---

## 🧪 Testing Structure

```
tests/
├── test_basic.py        # Smoke tests
├── test_movement.py     # Movement and bounds
├── test_directions.py   # Direction enum
└── test_collision.py    # (Future)
```

---

## 🔐 Design Patterns Utilizados

1. **Object-Oriented Design**: Classes para cada entity
2. **Component-Based Architecture**: Separate systems (core, entities, systems, world)
3. **Dependency Injection**: Game passes dependencies to entities
4. **State Management**: Centralized game state
5. **Separation of Concerns**: Each class has single responsibility

---

## 📝 Convenções de Código

- **Classes**: `PascalCase` (Game, Heroi, Enemy)
- **Métodos**: `snake_case` (spawn_wave, draw_ui)
- **Constants**: `UPPER_CASE` (SCREEN_W, BOSS_HEALTH)
- **Private**: Prefixo `_` (não usado aqui por simplicidade)

---

## 🚀 Próximas Melhorias

- [ ] Resource Manager (textures, sounds)
- [ ] Event System (signal/slot pattern)
- [ ] Input Manager (abstração de input)
- [ ] Particle System
- [ ] Animation System
- [ ] Physics Engine (gravidade, colisão avançada)

---

**Última atualização**: 2024
**Versão**: 1.0.0 (Professional Structure)
