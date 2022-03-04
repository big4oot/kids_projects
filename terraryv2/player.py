import pygame
from pygame.locals import *
from utils import calculate_distance
import np as np
from main import animation_frames

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.name = "Player"
        self.image = pygame.image.load("sprites/player/Player_Walk (1).gif").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 400
        self.is_falling = True
        self.state = "idle"
        self.frame_number = 0
        self.ticks_from_last_frame = pygame.time.get_ticks()
        self.view_direction = "right"
        self.is_jumping = False
        self.active_item = "Dirt"
        self.possible_move_direction = {"left": True, "right": True}
        self.health = 100
        self.ammo = 20

        
    def place_block(self, mouse_pos):
        if calculate_distance(self.rect.x, self.rect.y, mouse_pos[0], mouse_pos[1]) < 150:
            xs = [x for x in range(0, 1024, 32)]
            ys = [y for y in range(0, 838, 32)]
            x = xs[np.searchsorted(xs, mouse_pos[0], side="left")-1]
            y = ys[np.searchsorted(ys, mouse_pos[1], side="left")-1]
            for sprite in sprites:
                for x_ in range(x, x+32):
                    for _y in range(y, y+32):
                        if sprite.rect.collidepoint(x_, _y):
                            return
            block = Block(blocks_sprites[self.active_item], x, y, self.active_item) # block, x, y, name
            sprites.add(block)
            blocks.add(block)

  
        
    def shot(self, mouse_pos):
        arrow = Arrow(mouse_pos)
        sprites.add(arrow)
        arrows.add(arrow)
        
    def key_checker(self, key, mouse_pos):
        if key == pygame.K_SPACE and not self.is_falling:
            self.max_jump_height = self.rect.y - 75
            self.is_jumping = True
        if key == K_r and self.ammo > 0:
            self.shot(mouse_pos)
            self.ammo -= 1
        item_number = int(key) - 49
        if item_number in range(0,4):
            blocks_by_name = list(blocks_sprites.keys()) 
            self.active_item = blocks_by_name[item_number]

    def jump(self):
        if self.is_jumping:
            self.rect.y -= 5
            if self.rect.y < self.max_jump_height:
                self.is_jumping = False

    def animation(self, state="move"):
        now = pygame.time.get_ticks()
        if now - self.ticks_from_last_frame > 100:
            self.ticks_from_last_frame = now
            self.frame_number += 1
            if self.frame_number == 14:
                self.frame_number = 0
            _sprite = animation_frames["player_walk"][self.frame_number].convert_alpha()
            self.image = _sprite if self.view_direction == "right" else pygame.transform.flip(_sprite, True, False)


    def set_idle(self):
        _sprite = pygame.image.load("sprites/player/Player_Walk (1).gif")
        self.image = _sprite if self.view_direction == "right" else pygame.transform.flip(_sprite, True, False)
      

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_a] and self.possible_move_direction['left']:
            self.rect.x -= 2
            self.state = "move"
            self.view_direction = "left"
        elif keys[K_d] and self.possible_move_direction['right']:
            self.rect.x += 2
            self.state = "move"
            self.view_direction = "right"
        else:
            self.state = "idle"
            self.set_idle()

    def gravity(self):
        if self.is_falling:
            self.rect.y += 2

    def update(self):
        #print(self.rect.x)
        self.gravity()
        self.move()
        if self.state == "move":
            self.animation()
        self.jump()
        if self.health < 0:
          self.kill()
          g.is_continue = False
