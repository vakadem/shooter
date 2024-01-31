#Створи власний Шутер!

from pygame import *
from pygame.sprite import Sprite
from pygame.transform import scale, flip
from pygame.image import load
from random import randint
from time import time as timer

score = 0
lost = 0
life = 3

class GameSprite(Sprite):
    def __init__ (self, image, x, y, width, height, speed):
        super().__init__()
        self.image = scale(load(image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 620:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx-7, self.rect.top, 15, 20, 10)
        bullets.add(bullet)

#POVOROT RACETU AD
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height:
            self.rect.y = -50
            self.rect.x = randint(0, 620)
            lost = lost + 1
            print(lost, end = '\r')

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= -30:
            self.kill()
#del self

win_width = 700
win_height = 500

window = display.set_mode([win_width, win_height])
background = scale(load("galaxy.jpg"), [win_width, win_height])
ship = Player('rocket.png', 350, 400, 80, 100, 8)

bullets = sprite.Group()

monsters = sprite.Group()
for i in range(4):
    monster = Enemy('ufo.png', randint(0, win_width-50), -50, 80, 50, randint(1, 5))
    monsters.add(monster)

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
mixer.music.set_volume(0.05)
fire_mp3 = mixer.Sound("fire.ogg")
fire_mp3.set_volume(0.15)


font.init()
font1 = font.SysFont('Arial', 36)
font2 = font.SysFont('Arial', 84)
text_win = font2.render(f'You win', True, (0, 255, 0))

text_lose = font2.render(f'You lose', True, (255, 0, 0))


game = True
finish = False
clock = time.Clock()
FPS = 60

ammo = 5
reload = False

while game:
    events = event.get()
    for e in events:
        if e.type == QUIT:
            game = False
        


    if not finish:
        for e in events:
            if e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    if ammo > 0 and reload == False:   
                        ship.fire()
                        fire_mp3.play()
                        ammo -= 1
                    if ammo <= 0 and reload == False:
                        reload = True
                        start_time = timer()
        
        window.blit(background, [0, 0])
        text_score = font1.render(f'PaxyHoK: {score}', True, (255, 255, 255))
        window.blit(text_score, [10, 20])
        text_lost = font1.render(f'Lost: {lost}', True, (255, 255, 255))
        window.blit(text_lost, [10, 60])
        text_life = font1.render(f'Life: {life}', True, (255, 255, 255))
        window.blit(text_life, [10, 100])
        
        if reload:
            now_time = timer()
            delta_t = now_time - start_time
            if delta_t < 3:
                rel = font2.render("wait", True, (150, 0, 0))
                window_blit(rel, [200, 200])
            else:
                ammo = 5
                reload = False
        
        ship.reset()
        ship.update()
        bullets.draw(window)
        bullets.update()
        monsters.draw(window)
        monsters.update()
        if sprite.spritecollide(ship, monsters, True):
            life -= 1
            monster = Enemy('ufo.png', randint(0, win_width-50), -50, 80, 50, randint(1, 5))
            monsters.add(monster)
        if life <= 0 or lost >= 5:
            finish = True
            window.blit(text_lose, [200, 200])
            #music lose
            
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(0, win_width-50), -50, 80, 50, randint(1, 5))
            monsters.add(monster)
        if score == 10:
            finish = True
            text_score = font1.render(f'PaxyHoK: {score}', True, (255, 255, 255))
            window.blit(text_win, [200, 200])
            window.blit(text_lost, [10, 60])
            window.blit(text_score, [10, 20])
    else:
        score = 0
        lost = 0
        life = 3
        monsters.empty()
        bullets.empty()
        time.delay(1000)
        finish = False
        for i in range(4):
            monster = Enemy('ufo.png', randint(0, win_width-50), -50, 80, 50, randint(1, 5))
            monsters.add(monster)

        

    display.update()
    clock.tick(FPS)




































