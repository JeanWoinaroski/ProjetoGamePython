# Projeto Python Facul - 2D Shooter Game

Uma aventura de jogo 2D construída com **Pygame** em Python, apresentando um sistema de ondas, múltiplos tipos de inimigos e chefes épicos.

## 🎮 Features

- **Wave System**: Progressão automática através de ondas cada vez mais desafiadoras
- **Inimigos Variados**: 
  - Normal (1 HP, vermelho)
  - Strong (2 HP, rosa)
  - Boss (8 HP, dourado) - aparece a cada 5 ondas
- **UI Dinâmica**: 
  - Contador de ondas com indicador de chefe
  - Score em tempo real
  - Barra de progresso colorida (verde→laranja→vermelho)
  - Dicas contextuais
- **Transições Epicas**: Exibição de onda com fade-out de 3 segundos
- **Controles Intuitivos**:
  - WASD para movimento
  - ARROW KEYS para atirar em 4 direções

## 📁 Estrutura do Projeto

```
ProjetoPythonFacul/
├── src/                          # Código-fonte principal
│   ├── __init__.py
│   ├── core/                     # Game engine
│   │   ├── __init__.py
│   │   └── game.py               # Classe Game - loop principal
│   ├── entities/                 # Entidades do jogo
│   │   ├── __init__.py
│   │   ├── heroi.py              # Classe Heroi (jogador)
│   │   ├── enemy.py              # Classe Enemy (inimigos)
│   │   └── bullet.py             # Classe Bullet (projéteis)
│   ├── systems/                  # Sistemas de jogo
│   │   ├── __init__.py
│   │   └── direction.py          # Enum Direction
│   ├── world/                    # Sistema de mundo/mapa
│   │   ├── __init__.py
│   │   ├── map.py                # Classe Map
│   │   └── tile.py               # Classe Tile
│   └── utils/                    # Utilitários
│       └── __init__.py
├── levels/                       # Dados de níveis
│   └── level1.py                 # Level 1 data
├── assets/                       # Recursos (imagens, sons)
│   ├── images/
│   └── sounds/
├── tests/                        # Testes automatizados
├── config.py                     # Configurações centralizadas
├── main.py                       # Entry point
├── requirements.txt              # Dependências
└── README.md                     # Este arquivo
```

## 🚀 Como Executar

### Requisitos
- Python 3.8+
- Pygame 2.1.0+

### Instalação
```bash
pip install -r requirements.txt
```

### Executar o Jogo
```bash
python main.py
```

## 🎯 Controles

| Tecla | Ação |
|-------|------|
| **W** | Mover para cima |
| **A** | Mover para esquerda |
| **S** | Mover para baixo |
| **D** | Mover para direita |
| **↑** | Atirar para cima |
| **←** | Atirar para esquerda |
| **↓** | Atirar para baixo |
| **→** | Atirar para direita |
| **M** | Pausar/retomar música |
| **R** | Reiniciar (tela de game over) |
| **ESC** | Sair do jogo |

## 📊 Sistema de Scoring

| Inimigo | HP | Pontos | Cor |
|---------|--|----|------|
| Normal | 1 | 50 | Vermelho |
| Strong | 2 | 100 | Rosa |
| Boss | 8 | 1000 | Dourado |

## 🏗️ Arquitetura

O código segue padrão **Object-Oriented Game Development**:

- `src/core/game.py`: Loop principal, colisões, UI
- `src/entities/`: Heroi, Enemy, Bullet (classes independentes)
- `src/systems/`: Sistemas auxiliares (Direction enum)
- `src/world/`: Map e Tile (tilebase rendering)

**Wave System**: Auto-progressão, bosses a cada 5 ondas

## 🔧 Configuração

Constantes centralizadas em `config.py` para fácil customização.

## 🧪 Testes

```bash
python -m pytest tests/
```

## 🐛 Status

✅ Completo e funcional
✅ Sem bugs encontrados
✅ Estrutura profissional



### Nota Técnica:
A música é carregada via `pygame.mixer` e toca em loop infinito com volume reduzido para não interferir na jogabilidade. Os módulos `pygame.font` e `pygame.mixer` são inicializados explicitamente após a criação da janela para garantir compatibilidade.

## 🚧 Roadmap

- [ ] Power-ups
- [ ] Sistema de som
- [ ] Partículas
- [ ] Múltiplos níveis
- [ ] Menu principal
- [ ] High scores

---

**Made with ❤️ using Pygame**
