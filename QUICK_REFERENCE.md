# 🗂️ Quick Reference - Estrutura do Projeto

## 📌 Onde Encontrar O Quê

### **Para Logica do Jogo**
```
src/core/game.py
  ├── Game.__init__()           ← Inicializar jogo
  ├── Game.run()                ← Loop principal (60 FPS)
  ├── Game.spawn_wave()         ← Sistema de ondas
  ├── Game.check_wave_clear()   ← Detectar fim de onda
  └── Game.draw_ui()            ← Renderizar UI
```

### **Para Jogador (Heroi)**
```
src/entities/heroi.py
  ├── Heroi.move()              ← WASD movement
  ├── Heroi.shoot()             ← Disparo
  └── Heroi.image               ← Sprite do jogador
```

### **Para Inimigos**
```
src/entities/enemy.py
  ├── Enemy.take_damage()       ← Sistema de dano
  ├── Enemy.move_towards_hero() ← IA de perseguição
  ├── Enemy.health              ← HP (1, 2 ou 8)
  ├── Enemy.is_strong           ← Flag tipo forte
  └── Enemy.is_boss             ← Flag tipo boss
```

### **Para Balas**
```
src/entities/bullet.py
  ├── Bullet.move()             ← Atualizar posição
  ├── Bullet.is_off_screen()    ← Detectar limpeza
  └── Bullet.direction          ← Direção (Direction enum)
```

### **Para Direção/Input**
```
src/systems/direction.py
  ├── Direction.from_keys()     ← Mapear teclado → Direção
  └── Direction enum            ← UP, DOWN, LEFT, RIGHT, NONE
```

### **Para Mapa/Mundo**
```
src/world/map.py
  ├── Map.draw()                ← Renderizar tiles
  └── Map.collide_detection()   ← Detectar colisão

src/world/tile.py
  ├── Tile.draw()               ← Renderizar tile
  └── Tile.colliderect()        ← Check colisão
```

### **Para Dados de Level**
```
levels/level1.py
  ├── tile_data[][]             ← Grid de IDs de tiles (30x20)
  ├── tile_images{}             ← Mapping ID → cor
  └── solid_tiles[]             ← Tipos de tile sólidos
```

---

## 🔄 Fluxo Comum de Edição

### Mudar a Velocidade do Herói
```
1. Abrir: src/core/game.py
2. Procurar: Heroi(200, 200, 2, ...)
3. Mudar: 2 para novo valor (e.g., 3)
```

### Mudar a Saúde de um Inimigo Normal
```
1. Abrir: src/entities/enemy.py
2. Procurar: self.health = 1  (linha normal enemy)
3. Mudar: para novo valor
```

### Mudar Cores de Inimigos
```
1. Abrir: src/entities/enemy.py
2. Procurar: self.color = (255, 0, 0)  (red)
3. Mudar: para novo RGB (e.g., (0, 255, 0) for green)
```

### Mudar Pontos de Score
```
1. Abrir: src/core/game.py
2. Procurar: self.score += 50  (ou 100, ou 1000)
3. Mudar: para novo valor
```

### Adicionar Novo Tipo de Inimigo
```
1. Editar: src/entities/enemy.py
2. No __init__:
   if is_elite:
       self.health = 3
       self.color = (200, 100, 255)  # Purple
```

### Adicionar Item Novo ao Mapa
```
1. Editar: levels/level1.py
2. Mudar: tile_data e tile_images
3. Nota: 0=grass, 1=wall, 2=water
```

---

## 🎯 Imports Para Usar

Se criar arquivo novo em `src/`, use:

```python
# Para usar o herói
from src.entities import Heroi

# Para usar todos os entities
from src.entities import Heroi, Enemy, Bullet

# Para usar direction
from src.systems import Direction

# Para usar map
from src.world import Map, Tile

# Para usar o game
from src.core import Game
```

---

## 📊 Constantes Importantes

| Constante | Localização | Valor |
|-----------|----------|-------|
| SCREEN_WIDTH | Game.__init__() | 1440 |
| SCREEN_HEIGHT | Game.__init__() | 1080 |
| HERO_SPEED | Game.__init__() | 2 |
| BULLET_SPEED | Bullet.__init__() | 5 |
| NORMAL_HEALTH | Enemy.__init__() | 1 |
| STRONG_HEALTH | Enemy.__init__() | 2 |
| BOSS_HEALTH | Enemy.__init__() | 8 |
| NORMAL_COLOR | Enemy.__init__() | (255, 0, 0) |
| STRONG_COLOR | Enemy.__init__() | (255, 100, 100) |
| BOSS_COLOR | Enemy.__init__() | (255, 215, 0) |

---

## 🧪 Testes

```bash
# Validate structure
python test_structure.py

# Run game
python main.py

# Run unit tests
python -m pytest tests/
```

---

## 📚 Arquivos de Documentação

| Arquivo | Propósito |
|---------|-----------|
| **README.md** | Features, controles, como rodar |
| **ARCHITECTURE.md** | Visão técnica, fluxo de dados, patterns |
| **ORGANIZATION_SUMMARY.md** | Antes/depois, mudanças, benefícios |
| **QUICK_REFERENCE.md** | Este arquivo - referência rápida |

---

## 🚀 Dicas Pro

1. **Usar Ctrl+P em VS Code** para buscar arquivo
   - `Heroi` → acha heroi.py
   - `enemy` → acha enemy.py

2. **Use Ctrl+Shift+F** para buscar em todos os arquivos
   - Busca em todo projeto por texto

3. **Estrutura modular permite**:
   - Editar uma classe sem afetar outras
   - Testar classes isoladamente
   - Reutilizar código em novos projetos

4. **Game.py é o "maestro"**:
   - Coordena todas as classes
   - Se algo não funciona, olhe Game.run()

---

## 🎓 Próximas Funcionalidades

Para adicionar cada nova feature:

1. **Power-ups**: criar `src/entities/powerup.py`
2. **Som**: criar `src/systems/audio.py`
3. **Partículas**: criar `src/systems/particles.py`
4. **Menu**: criar `src/ui/menu.py`
5. **Settings**: criar `config.py` (centralizado)

---

**Precisando de ajuda? Consulte ARCHITECTURE.md para detalhes técnicos.**
