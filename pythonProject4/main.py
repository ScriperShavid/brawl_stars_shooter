#Создай собственный Шутер!
import random
from pygame import *
from time import time as timer

win_width = 700
win_height = 500
display.set_caption('Бравл Старс')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load('acid-lakes-solo-showdown-map.f2d9110341.png'), (win_width, win_height))

font.init()
font1 = font.SysFont(None, 80)
font2 = font.SysFont(None, 36)
win = font1.render('Победа!', True, (0, 255, 0))
lose = font1.render('ПРОИГРЫШ!', True, (255, 0, 0))

score = 0
lost = 0
max_lost = 5
goal = 10
life = 3

mixer.init()
mixer.music.load('brawl_stars_menu_01.mp3')
#mixer.music.play()
fire_sound = mixer.Sound('fire.mp3')

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('Bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = random.randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = random.randint(80, win_width - 80)
            self.rect.y = 0

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

shelly = Player('shely.png', 310, win_height - 100, 80, 100, 10)

mortises = sprite.Group()
for i in range(1, 6):
    mortis = Enemy('mortis.png', random.randint(80, win_width - 80), -40, 80, 100, random.randint(1, 5))
    mortises.add(mortis)

bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(1, 6):
    asteroid = Asteroid('ufo.png', random.randint(80, win_width - 30), -40, 80, 50, random.randint(1, 7))
    asteroids.add(asteroid)

finish = False
run = True

num_fire = 0
rel_time = False
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE]:
            if num_fire < 5 and rel_time == False:
                num_fire += 1
                shelly.fire()
                fire_sound.play()
            if num_fire >= 5 and rel_time == False:
                last_time = timer()
                rel_time = True

    if not finish:
        window.blit(background, (0, 0))
        shelly.update()
        mortises.update()
        mortises.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)
        shelly.reset()
        text = font2.render('Счёт: ' + str(score), 1, (255, 255, 0))
        window.blit(text, (10, 20))
        text2 = font2.render('Пропущено: ' + str(lost), 1, (255, 255, 0))
        window.blit(text2, (10, 50))

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render('ПОДОЖДИ ПЕРЕЗАРЯДКУ!', 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(mortises, bullets, True, True)
        for i in collides:
            score += 1
            mortis = Enemy('mortis.png', random.randint(80, win_width - 80), -40, 80, 100, random.randint(1, 5))
            mortises.add(mortis)

        if sprite.spritecollide(shelly, mortises, False) or sprite.spritecollide(shelly, asteroids, False):
            sprite.spritecollide(shelly, mortises, True)
            sprite.spritecollide(shelly, asteroids, True)
            life -= 1

        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        if life == 3:
            life_color = (0, 150, 0)
        if life == 2:
            life_color = (150, 150, 0)
        if life == 1:
            life_color = (150, 0, 0)

        text_life = font1.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
        display.update()


    time.delay(50)