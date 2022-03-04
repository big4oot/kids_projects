import pygame

WIDTH = 1024
HEIGHT = 838
FPS = 60
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)


blocks_strenghts = dict(Dirt=1, Wood=3, Coat=5, Glass=1, Stone=4)

hearth = pygame.transform.scale(pygame.image.load("sprites/player/hearth.png"),
                                (32, 32))

arrow = pygame.transform.scale(
            pygame.image.load("sprites/player/arrow.png"),
            (40, 11))

blocks_sprites = {
    'Dirt': pygame.image.load("sprites/blocks/Dirt.png"),
    'Wood': pygame.image.load("sprites/blocks/Wood.png"),
    'Coat': pygame.image.load("sprites/blocks/Coat.png"),
    'Glass': pygame.image.load("sprites/blocks/Glass.png"),
    'Stone': pygame.image.load("sprites/blocks/Stone.png")
}

animation_frames = {"player_walk": [], "enemy_walk": []}
for i in range(1, 15):
    sprite = pygame.image.load(f"sprites/player/Player_Walk ({i}).gif")
    animation_frames["player_walk"].append(sprite)

for i in range(1, 10):
    sprite = pygame.image.load(f"sprites/enemy/Enemy{i}.png")
    animation_frames["enemy_walk"].append(sprite)
