import pygame

import main
from const import *


class Game:
    def __init__(self):
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load("sprites/background.png").convert_alpha()
        self.bg_rect = self.bg.get_rect()
        self.is_continue = True
        self.font = pygame.font.SysFont('Comic Sans MS', 24)

    def run(self):
        while self.is_continue:
            self.surface.fill(BLACK)
            self.surface.blit(self.bg, self.bg_rect)
            self.clock.tick(FPS)
            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    pygame.quit()
            sprites.draw(self.surface)
            pygame.display.flip()

def create_ground():
    for x in range(0, 1024, 32):
        ground_block = Block(blocks_sprites['Dirt'], x, 608, "dirt")
        sprites.add(ground_block)
        blocks.add(ground_block)

sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()


if __name__ == '__main__':
    g = Game()
    create_ground()
