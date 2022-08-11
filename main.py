"""
Made by Sacha Hallermeier
"""
import pygame
from GameState import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((w, h))
    screen.fill(black)
    pygame.display.set_caption('Covid Them All !')

    font = pygame.font.Font(pygame.font.get_default_font(), 36)
    smaller_font = pygame.font.Font(pygame.font.get_default_font(), 18)

    game = GameState(screen, font, smaller_font)
    while game.playing:
        game.level_manager()
        pygame.time.Clock().tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()