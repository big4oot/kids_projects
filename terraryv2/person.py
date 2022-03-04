import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            "sprites/player/Player_Walk (1).gif").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 400
        self.is_falling = True
        self.state = "idle"
        self.view_direction = "right"
        self.is_jumping = False
        self.active_item = "Dirt"
        self.possible_move_direction = {"left": True, "right": True}
        self.health = 100
        self.ammo = 20
        self.side_colliders = pygame.sprite.Group()


    
    

