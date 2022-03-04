import pygame


class Block(pygame.sprite.Sprite):
    def __init__(self, block, x, y, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = block.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.arrows_on_block = []
        self.strength = blocks_strenghts[self.name.capitalize()]

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            if calculate_distance(self.rect.x, self.rect.y, player.rect.x,
                                  player.rect.y) < 70:
                self.strength -= 1
                if self.strength == 0:
                    for arrow in self.arrows_on_block:
                        arrow.kill()
                    self.kill()


blocks_strenghts = dict(Dirt=1, Wood=3, Coat=5, Glass=1)
