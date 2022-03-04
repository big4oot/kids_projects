import random
import time

import pygame.sprite
from const import *
from pygame.constants import *
from math import atan2, sin, cos, pi
from utils import rot_center, calculate_distance
import numpy as np


class Animator:
    def __init__(self):
        self.ticks_from_last_frame = 0
        self.frame_number = 0
        self.view_direction = 'right'

    def animation(self, obj, frames):
        now = pygame.time.get_ticks()
        if now - self.ticks_from_last_frame > 100:
            self.ticks_from_last_frame = now
            self.frame_number += 1
            if self.frame_number == len(frames) - 1:
                self.frame_number = 0
            _sprite = frames[self.frame_number].convert_alpha()
            obj.image = _sprite if self.view_direction == "right" else pygame.transform.flip(_sprite, True, False)

    def set_idle(self, obj, frame):
        _sprite = frame
        obj.image = _sprite if self.view_direction == "right" else pygame.transform.flip(_sprite, True, False)


class Enemy(pygame.sprite.Sprite, Animator):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        Animator.__init__(self)
        self.image = pygame.image.load("sprites/enemy/Enemy1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_falling = True
        self.side_colliders = pygame.sprite.Group()
        create_side_colliders(self)
        self.possible_move_direction = {'left': True, 'right': True}
        self.max_jump_height = 0
        self.is_jumping = False
        self.health = 50
        self.arrows_on = []
        self.view_direction = 'left'
        self.next_second_for_hit = g.seconds

    def move(self):
        self.view_direction = 'left' if self.rect.x > player.rect.x else 'right'
        distance_to_player = abs(self.rect.x - player.rect.x)
        if distance_to_player > 15 and not self.is_falling:
            if self.view_direction == 'left' and self.possible_move_direction['left']:
                self.rect.x -= 1
            elif self.possible_move_direction['right']:
                self.rect.x += 1

    def die(self):
        global points
        for a in self.arrows_on:
            a.kill()
        del self.side_colliders
        self.kill()
        points += 1
        if points % 10 == 0:
            block = random.choice(list(player.inventory.keys()))  #
            player.inventory[block] += 1

    def update_arrows_connection(self):
        for arrow in self.arrows_on:
            arrow.rect.x = self.rect.x
            arrow.rect.y = self.rect.y

    def update(self):
        self.move()
        gravity(self)
        self.side_colliders.update()
        self.update_arrows_connection()
        self.attack_player()
        check_blocks_collision(self)
        self.animation(self, animation_frames['enemy_walk'])
        if self.is_under_player():
            self.cast_fireball()

    def attack_player(self):
        collision = pygame.sprite.collide_rect(self, player)
        if collision and not player.is_falling:
            player.max_jump_height = self.rect.y - 75
            player.is_jumping = True
            player.health -= 10

    def attack_block(self, block):
        if g.seconds > self.next_second_for_hit:
            print('HIT')
            block.strength -= 1
            block.last_hit_by_player = False
            self.next_second_for_hit = g.seconds + 2

    def is_under_player(self):
        if abs(self.rect.x - player.rect.x) < 5 and self.rect.y - player.rect.y > 96:
            return True
        return False

    def cast_fireball(self):
        if not fireballs:
            fb = Fireball(self.rect.x, self.rect.y)
            sprites.add(fb)
            fireballs.append("fireball!")


class Player(pygame.sprite.Sprite, Animator):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        Animator.__init__(self)
        self.image = pygame.image.load("sprites/player/Player_Walk (1).gif").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2
        self.rect.y = 550
        self.is_falling = True
        self.side_colliders = pygame.sprite.Group()
        create_side_colliders(self)
        self.possible_move_direction = {'left': True, 'right': True}
        self.max_jump_height = 0
        self.is_jumping = False
        self.ammo = 30
        self.active_item = 'Dirt'
        self.health = 100
        self.inventory = {'Dirt': 5, 'Wood': 3, 'Coat': 0, 'Glass': 2, 'Stone': 3}

    def key_checker(self, key, mouse_pos):
        if key == pygame.K_SPACE and not self.is_falling:
            self.max_jump_height = self.rect.y - 75
            self.is_jumping = True
        if key == K_r and self.ammo > 0:
            self.shot(mouse_pos)
            self.ammo -= 1
        if key == 1:
            for block in blocks:
                block.is_clicked(mouse_pos)
        if key == 3:
            player.place_block(mouse_pos)
        item_number = int(key) - 49
        if item_number in range(0, 5):
            blocks_by_name = list(blocks_sprites.keys())
            self.active_item = blocks_by_name[item_number]

    def shot(self, mouse_pos):
        arrow = Arrow(mouse_pos)
        sprites.add(arrow)
        arrows.add(arrow)

    def place_block(self, mouse_pos):
        if calculate_distance(self.rect.x, self.rect.y, mouse_pos[0],
                              mouse_pos[1]) < 150 and self.inventory[self.active_item] > 0:
            xs = [x for x in range(0, 1024, 32)]
            ys = [y for y in range(0, 838, 32)]
            x = xs[np.searchsorted(xs, mouse_pos[0], side="left") - 1]
            y = ys[np.searchsorted(ys, mouse_pos[1], side="left") - 1]
            for sprite in sprites:
                for x_ in range(x, x + 32):
                    for _y in range(y, y + 32):
                        if sprite.rect.collidepoint(x_, _y):
                            return
            block = Block(blocks_sprites[self.active_item], x, y,
                          self.active_item)  # block, x, y, name
            sprites.add(block)
            blocks.add(block)
            self.inventory[self.active_item] -= 1

    def jump(self):
        if self.is_jumping:
            self.rect.y -= 5
            if self.rect.y < self.max_jump_height:
                self.is_jumping = False

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_a] and self.possible_move_direction['left']:
            self.rect.x -= 2
            self.state = "move"
            self.view_direction = "left"
            self.animation(self, animation_frames['player_walk'])
        elif keys[K_d] and self.possible_move_direction['right']:
            self.rect.x += 2
            self.state = "move"
            self.view_direction = "right"
            self.animation(self, animation_frames['player_walk'])
        else:
            self.state = "idle"
            self.set_idle(self, animation_frames['player_walk'][0])

    def update(self):
        gravity(self)
        self.side_colliders.update()
        check_blocks_collision(self)
        self.move()
        self.jump()
        if self.health <= 0 or self.rect.y >= HEIGHT:
            game_over()


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.bg = pygame.image.load("sprites/background.png").convert_alpha()
        self.bg_rect = self.bg.get_rect()
        self.is_continue = True
        self.font = pygame.font.SysFont('Comic Sans MS', 24)
        self.seconds = 0
        self.last_time_tick = time.time()
        self.wave = 1
        self.time_for_next_wave = 1

    def timer(self):
        if time.time() - self.last_time_tick > 1:
            self.seconds += 1
            self.last_time_tick = time.time()

    def run(self):
        while True:
            if self.is_continue:
                self.timer()
                self.surface.fill(BLACK)
                self.surface.blit(self.bg, self.bg_rect)
                self.clock.tick(FPS)
                for event in pygame.event.get():
                    mouse_pos = pygame.mouse.get_pos()
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.KEYDOWN and event.key == K_g:  # debug feature
                        spawn_enemy(mouse_pos)
                    if event.type == pygame.KEYDOWN:
                        player.key_checker(event.key, mouse_pos)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        player.key_checker(event.button, mouse_pos)
                if self.seconds == self.time_for_next_wave:
                    next_wave()
                sprites.update()
                sprites.draw(self.surface)
                show_gui()
                pygame.display.flip()


class Block(pygame.sprite.Sprite):
    def __init__(self, block, x, y, name):
        pygame.sprite.Sprite.__init__(self)
        self.image = block.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
        self.arrows_on = []
        self.strength = blocks_strenghts[self.name.capitalize()]
        self.last_hit_by_player = False

    def is_clicked(self, pos):
        if self.rect.collidepoint(pos):
            if calculate_distance(self.rect.x, self.rect.y, player.rect.x,
                                  player.rect.y) < 70:
                self.strength -= 1
                self.last_hit_by_player = True

    def update(self):
        if self.strength <= 0:
            for arrow in self.arrows_on:
                arrow.kill()
            if self.last_hit_by_player:
                player.inventory[self.name.capitalize()] += 1
            self.kill()


class SideCollider(pygame.sprite.Sprite):
    def __init__(self, side, obj):
        pygame.sprite.Sprite.__init__(self)
        self.obj = obj
        self.side = side
        if side == "left" or side == "right":
            self.image = pygame.Surface((1, 45))
        else:
            self.image = pygame.Surface((20, 1))
        self.rect = self.image.get_rect()

    def update(self):
        if self.side == "left":
            self.rect.right = self.obj.rect.left
            self.rect.top = self.obj.rect.top
        if self.side == "right":
            self.rect.left = self.obj.rect.right
            self.rect.top = self.obj.rect.top
        if self.side == "top":
            self.rect.bottom = self.obj.rect.top
            self.rect.left = self.obj.rect.left + 5
        if self.side == "bottom":
            self.rect.top = self.obj.rect.bottom
            self.rect.left = self.obj.rect.left + 5


class Arrow(pygame.sprite.Sprite):
    def __init__(self, mouse_pos):
        pygame.sprite.Sprite.__init__(self)
        self.direction = 1 if player.view_direction == 'right' else -1
        self.image = arrow.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x
        self.rect.y = player.rect.y
        self.is_active = True
        self.mouse_pos = mouse_pos
        self.angle = atan2((self.mouse_pos[1] - self.rect.y),
                           (self.mouse_pos[0] - self.rect.x))
        self.deg = (self.angle / pi * 180) + (0 if self.angle > 0 else 360)
        self.image = rot_center(self.image, -self.deg)
        self.created_time = time.time()
        self.damage = 25
        self.speed = 5

    def update(self):
        self.check_collision()
        if self.is_active:
            self.rect.x += self.speed * cos(self.angle)
            self.rect.y += self.speed * sin(self.angle)
        if self.rect.x < -50 or self.rect.x > WIDTH + 50 or time.time(
        ) - self.created_time > 5:
            self.kill()

    def check_collision(self):
        if self.is_active:
            collisions = pygame.sprite.spritecollide(self, blocks, False)
            collisions.extend(pygame.sprite.spritecollide(self, enemies, False))
            if collisions:
                for obj in collisions:
                    obj.arrows_on.append(self)
                    if isinstance(obj, Enemy):
                        obj.health -= self.damage
                        if obj.health <= 0:
                            player.ammo += 2
                            obj.die()
                        break
                self.is_active = False


class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("sprites/enemy/fireball.png")
        self.image = pygame.transform.scale(self.image, (32, 32))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def check_collision(self):
        collisions = pygame.sprite.spritecollide(self, blocks, False)
        if self.rect.colliderect(player.rect):
            player.health -= 50
            fireballs.pop()
            self.kill()
        for obj in collisions:
            obj.strength -= 100
            print(obj)

    def update(self):
        self.rect.y -= 1
        self.check_collision()


def create_ground():
    for x in range(0, 1024, 32):
        # первый уровень
        block = Block(blocks_sprites['Dirt'], x, 608, "dirt")
        sprites.add(block)
        blocks.add(block)

        # второй уровень
        block = Block(blocks_sprites['Stone'], x, 640, "stone")
        sprites.add(block)
        blocks.add(block)

        # третий уровень
        block_name = random.choice((['Stone'] * 5) + (['Coat'] * 2))
        block = Block(blocks_sprites[block_name], x, 672, block_name.lower())
        sprites.add(block)
        blocks.add(block)

        # четвёртый уровень
        block_name = random.choice((['Stone'] * 5) + (['Coat'] * 2))
        block = Block(blocks_sprites[block_name], x, 704, block_name.lower())
        sprites.add(block)
        blocks.add(block)

        # пятый уровень
        block_name = random.choice((['Stone'] * 5) + (['Coat'] * 2))
        block = Block(blocks_sprites[block_name], x, 736, block_name.lower())
        sprites.add(block)
        blocks.add(block)


def gravity(obj):
    if obj.is_falling:
        obj.rect.y += 2


def create_side_colliders(obj):
    obj.side_colliders.add(SideCollider("left", obj))
    obj.side_colliders.add(SideCollider("right", obj))
    obj.side_colliders.add(SideCollider("top", obj))
    obj.side_colliders.add(SideCollider("bottom", obj))


def check_blocks_collision(obj):
    obj_block_collision = pygame.sprite.groupcollide(obj.side_colliders, blocks, False, False)
    colliders = [
        col.side for col in list(obj_block_collision.keys())
    ]
    if 'bottom' in colliders:
        obj.is_falling = False
    else:
        obj.is_falling = True

    if 'top' in colliders and obj.is_jumping:
        obj.is_jumping = False
        obj.is_falling = True

    if 'left' in colliders:
        obj.possible_move_direction['left'] = False
        if isinstance(obj, Enemy):
            obj.attack_block(list(obj_block_collision.values())[0][0])
    else:
        obj.possible_move_direction['left'] = True

    if 'right' in colliders:
        obj.possible_move_direction['right'] = False
        if isinstance(obj, Enemy):
            obj.attack_block(list(obj_block_collision.values())[0][0])
    else:
        obj.possible_move_direction['right'] = True


def show_gui():
    text_active_block = g.font.render(player.active_item, True, (255, 255, 255))
    text_hp = g.font.render(str(player.health), True, (255, 255, 255))
    text_ammo = g.font.render(str(player.ammo), True,
                              (255, 255, 255))
    text_point = g.font.render(f'Points  {points}', True,
                               (255, 255, 255))
    block_count = g.font.render(str(player.inventory[player.active_item]), True, (255, 255, 255))
    g.surface.blit(blocks_sprites[player.active_item], (10, 50))
    g.surface.blit(text_active_block, (10, 10))
    g.surface.blit(hearth, (WIDTH - 240, 10))
    g.surface.blit(text_hp, (WIDTH - 200, 10))
    g.surface.blit(arrow, (WIDTH - 240, 50))
    g.surface.blit(text_ammo, (WIDTH - 200, 50))
    g.surface.blit(text_point, (WIDTH - WIDTH / 2, 10))
    g.surface.blit(block_count, (10, 80))


def spawn_enemy(mouse_pos=None):
    if not mouse_pos:
        x = random.choice((random.randint(10, 246), (random.randint(778, WIDTH - 10))))
        y = random.randint(304, 500)
    else:
        x = mouse_pos[0]
        y = mouse_pos[1]
    enemy = Enemy(x, y)
    sprites.add(enemy)
    enemies.add(enemy)


def game_over():
    global points
    sprites.empty()
    blocks.empty()
    arrows.empty()
    enemies.empty()
    over_text = g.font.render("GAME OVER", True, (255, 255, 255))
    points_text = g.font.render(f"POINTS:{points}", True, (255, 255, 255))

    g.is_continue = False
    points = 0
    is_restart = False
    while not is_restart:
        g.surface.blit(over_text, (WIDTH / 2, HEIGHT / 2))
        g.surface.blit(points_text, (WIDTH / 2, HEIGHT / 2 + 50))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                is_restart = True
    new_game()


def new_game():
    global player
    global points
    points = 0
    create_ground()
    player = Player()
    sprites.add(player)
    g.is_continue = True
    g.wave = 1
    g.time_for_next_wave = 1
    g.seconds = 0


def next_wave():
    print('Wave', str(g.wave), '  Seconds:', str(g.seconds))
    for i in range(g.wave * 3):
        spawn_enemy()
    g.wave += 1
    g.time_for_next_wave = g.seconds + 3 * g.wave


player = None
sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
arrows = pygame.sprite.Group()
enemies = pygame.sprite.Group()
fireballs = []
points = 0

if __name__ == '__main__':
    g = Game()
    new_game()
    g.run()
