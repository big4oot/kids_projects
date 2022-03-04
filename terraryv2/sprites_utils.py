import pygame

hearth = pygame.transform.scale(pygame.image.load("sprites/player/hearth.png"),
                                (32, 32))

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
