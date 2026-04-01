"""Ponto de entrada principal do jogo"""
import pygame
from src.core import Game


def main():
    """Inicializa o pygame e começa o jogo"""
    while True:  # Loop para permitir reinicialização
        game = Game()
        result = game.run()
        if result != "restart":
            break  # Sai do loop se não for restart


if __name__ == "__main__":
    main()