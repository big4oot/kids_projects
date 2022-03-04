import pygame
import random

from pygame import sprite
from pygame import rect
from pygame.constants import K_DOWN, K_SPACE, K_UP
from pygame.display import update

class Missle (pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load('missle.png')
        self.image=pygame.transform.scale(self.image,(70,60))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

    def update(self):
        self.rect.x-=5
        if self.rect.right<0:
            self.kill()



class Player (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load('plane.png')
        self.image=pygame.transform.scale(self.image,(60,50))
        self.rect=self.image.get_rect()
        self.health=10
        self.ammo=15

    def shoot(self):
        if self.ammo>0:
            bull=Bullet(self.rect.right,self.rect.centery)
            sprites.add(bull)
            bullets.add(bull)
            self.ammo-=1

    def update(self):
        self.move()
        self.check_collision()
        self.check_health()

    def key_handler(self,key):
        if key==K_SPACE:
            self.shoot()


    def move(self):
        keys=pygame.key.get_pressed()
        if keys[K_DOWN] and self.rect.bottom<HEIGHT:
            self.rect.y+=3
        if keys[K_UP] and self.rect.top>0:
            self.rect.y-=3

    def check_collision(self):
        collisions=pygame.sprite.spritecollide(self,missiles,True)
        for col in collisions:
            self.health-=1
            
    def check_health(self):
        if self.health<=0:
            game_over()
    


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load('cloud.png')
        self.image=pygame.transform.scale(self.image,(70,60))
        self.rect=self.image.get_rect()
        self.rect.x=random.randint(WIDTH,WIDTH+200)
        self.rect.y=random.randint(0,HEIGHT)

    def update(self):
        self.rect.x-=1
        if self.rect.right<0:
            self.rect.x=random.randint(WIDTH,WIDTH+200)
            self.rect.y=random.randint(0,HEIGHT)


class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()
        self.image=pygame.image.load('bullet.png')
        self.image=pygame.transform.scale(self.image,(16,16))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y

    def check_enemi_hit(self):
        hieted_enemys=pygame.sprite.spritecollide(self,enemies,False)

        for col in hieted_enemys:
            col.health-=1
            self.explode()
            player.ammo+=2
            self.kill()
            break

    def explode(self):
        exp=Explosion(self.rect.centerx,self.rect.centery)
        sprites.add(exp)


    def update(self):
        self.rect.x+=10
        if self.rect.x>WIDTH:
            self.kill()
        self.check_enemi_hit()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load('enemy.png')
        self.image=pygame.transform.scale(self.image,(110,26))
        self.rect=self.image.get_rect()
        self.rect.x=random.randint(WIDTH,WIDTH+500)
        self.rect.y=random.randint(0,HEIGHT)
        self.health=2

    def update(self):
        self.rect.x-=1
        if self.rect.right<0:
            self.rect.x=random.randint(WIDTH,WIDTH+500)
            self.rect.y=random.randint(0,HEIGHT)
        if self.is_player_opposite() and len(missiles)<10:
            self.launch_rocket()
        if self.health<=0:
            self.kill()

    def launch_rocket(self):
        missile=Missle(self.rect.left, self.rect.bottom)
        sprites.add(missile)
        missiles.add(missile)


    def is_player_opposite(self):
        if abs(self.rect.y-player.rect.y)<5:
            return True
        else:
            return False


class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=explosions_srites[0]
        self.rect=self.image.get_rect()
        self.image_number=0
        self.rect.centerx=x+25
        self.rect.centery=y+25
    

    def update(self):
        self.image_number+=1
        if self.image_number==9:
            self.kill()
        else:
            self.image=explosions_srites[self.image_number]


def creat_clouds():
    for _ in range(6):
        cloud=Cloud()
        sprites.add(cloud)

def creat_enemies():
    for _ in range(5):
        enemy=Enemy()
        sprites.add(enemy)
        enemies.add(enemy)

def game_over():
    global game_is_continue
    game_is_continue=False


def show_gui():
    hp_text=font.render(f'HP:{player.health}',True,BLACK)
    window.blit(hp_text,(WIDTH-100,HEIGHT-50))
    ammo_text=font.render(f'ammo:{player.ammo}',True,BLACK)
    window.blit(ammo_text,(WIDTH-250,HEIGHT-50))


    

WIDTH=480
HEIGHT=480
BLACK=(0,0,0)
RED=(255,0,0)
FPS=30

game_is_continue=True

pygame.init()
font=pygame.font.SysFont('Comic Sans MS',30)
sprites=pygame.sprite.Group()
missiles=pygame.sprite.Group()
bullets=pygame.sprite.Group()
enemies=pygame.sprite.Group()

window=pygame.display.set_mode((WIDTH,HEIGHT))
clock=pygame.time.Clock()

explosions_srites=[]
for i in range(9):
    s=pygame.image.load(f'explosions\\regularExplosion0{i}.png')
    explosions_srites.append(s)

player=Player()
sprites.add(player)

creat_clouds()
creat_enemies()

#игровой цыкл
while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
        if event.type==pygame.KEYDOWN:
            player.key_handler(event.key)
    window.fill((117,187,253))
    if game_is_continue:
        sprites.update()
        sprites.draw(window)
        show_gui()
    else:
        text=font.render('Вы проиграли',True,BLACK)
        window.blit(text,(WIDTH/2-100,HEIGHT/2))
    pygame.display.flip()
    
