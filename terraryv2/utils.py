import pygame
from math import sqrt

def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    return rot_image


def calculate_distance(obj1x, obj1y, obj2x, obj2y):
    distance = sqrt((obj2x - obj1x) ** 2 + (obj1y - obj2y) ** 2)
    return distance


def create_ground():
    for x in range(0, 1024, 32):
        ground_block = Block(blocks_sprites['Dirt'], x, 608, "dirt")
        sprites.add(ground_block)
        blocks.add(ground_block)
