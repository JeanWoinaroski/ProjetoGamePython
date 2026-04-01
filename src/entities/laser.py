"""Classe do Laser"""
import pygame
from src.systems import Direction


class Laser:
    """
    Representa o tiro da arma Laser.

    Quando o jogador atira, o laser nasce na posição do personagem
    e vai até a borda da tela na direção escolhida.
    """

    def __init__(self, start_x, start_y, direction, screen_width, screen_height):

        # Guarda a posição onde o laser começa
        self.start_x = start_x
        self.start_y = start_y

        # Guarda a direção em que o jogador está olhando
        self.direction = direction

        # Guarda o tamanho da tela
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Cor do laser (roxo)
        self.color = (255, 0, 255)

        # Grossura da linha do laser
        # Pode aumentar se quiser deixar mais visível
        self.width = 6

        # Quanto tempo o laser fica visível na tela
        # 150 = 150 milissegundos = 0,15 segundos
        self.duration = 150

        # Diz se o laser ainda está ativo
        self.active = True

        # Salva o horário exato em que o laser foi criado
        # pygame.time.get_ticks() devolve quantos milissegundos
        # já se passaram desde que o jogo começou
        self.spawn_time = pygame.time.get_ticks()

        # Aqui escolhemos até onde o laser vai,
        # dependendo da direção do jogador

        # Se estiver olhando para cima,
        # o laser vai até o topo da tela
        if direction == Direction.UP:
            self.end_x = start_x
            self.end_y = 0

        # Se estiver olhando para baixo,
        # o laser vai até o final da tela
        elif direction == Direction.DOWN:
            self.end_x = start_x
            self.end_y = screen_height

        # Se estiver olhando para a esquerda,
        # o laser vai até a borda esquerda
        elif direction == Direction.LEFT:
            self.end_x = 0
            self.end_y = start_y

        # Se estiver olhando para a direita,
        # o laser vai até a borda direita
        elif direction == Direction.RIGHT:
            self.end_x = screen_width
            self.end_y = start_y

    def update(self):
        """
        Atualiza o laser.

        Esta função verifica se já passou tempo suficiente
        para o laser desaparecer.
        """

        # Pega o horário atual do jogo
        current_time = pygame.time.get_ticks()

        # Se já passou mais tempo do que a duração do laser
        if current_time - self.spawn_time >= self.duration:

            # O laser deixa de existir
            self.active = False

    def draw(self, surface):
        """
        Desenha o laser na tela.
        """

        # Só desenha se ele ainda estiver ativo
        if self.active:

            # Desenha uma linha:
            # surface = tela
            # self.color = cor
            # (self.start_x, self.start_y) = começo da linha
            # (self.end_x, self.end_y) = final da linha
            # self.width = grossura
            pygame.draw.line(
                surface,
                self.color,
                (self.start_x, self.start_y),
                (self.end_x, self.end_y),
                self.width
            )

    def check_collision(self, enemies):
        """
        Verifica quais inimigos foram atingidos pelo laser.

        Retorna uma lista contendo os inimigos acertados.
        """

        # Lista vazia para guardar os inimigos atingidos
        hit_enemies = []

        # Passa por todos os inimigos do jogo
        for enemy in enemies:

            # Se o laser estiver para cima ou para baixo,
            # ele é um laser "vertical"
            if self.direction in [Direction.UP, Direction.DOWN]:

                # Verifica se o inimigo está perto do X do laser
                # e entre o começo e o final da linha
                if (
                    self.start_x - 20 <= enemy.x <= self.start_x + 20
                    and min(self.start_y, self.end_y) <= enemy.y <= max(self.start_y, self.end_y)
                ):
                    hit_enemies.append(enemy)

            # Se não, então o laser está para esquerda ou direita
            else:

                # Agora verificamos se o inimigo está perto do Y do laser
                # e entre o começo e o final da linha
                if (
                    self.start_y - 20 <= enemy.y <= self.start_y + 20
                    and min(self.start_x, self.end_x) <= enemy.x <= max(self.start_x, self.end_x)
                ):
                    hit_enemies.append(enemy)

        # Devolve todos os inimigos atingidos
        return hit_enemies

    def is_off_screen(self):
        """
        Diz se o laser deve ser removido.

        Se active for False, o jogo pode apagar ele da lista.
        """
        return not self.active