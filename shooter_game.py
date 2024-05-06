#Создай собственный Шутер!

from pygame import *
from random import randint

lost = 0 
score = 0
life = 3


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x >5:
            self.rect.x -=self.speed
        if keys_pressed[K_RIGHT] and self.rect.x <620:
            self.rect.x +=self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        
        if self.rect.y > win_height: 
            self.rect.y = 0
            self.rect.x = randint(80,win_width - 80)
            lost +=1
            

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.x < 0:
            self.kill
            
            


 




win_width = 700
win_height = 500       

player = Player('rocket.png', 5, 400, 80, 100, 20)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(3, 6))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 3))
    asteroids.add(asteroid)

bullets = sprite.Group()

window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
background = transform.scale(image.load("galaxy.jpg"),(win_width, win_height))

font.init()
font1 = font.SysFont('Arial',36)
font2 = font.SysFont('Arial', 90)
lose = font2.render('YOU LOSE!', True, (180, 0, 0))
win = font2.render('YOU WIN!', True, (180, 0, 0))

game = True
finish = False 
clock = time.Clock()





mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

while game:
    
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    if finish != True: 
        window.blit(background,(0, 0))

        text = font1.render('Пропущено:' + str(lost),1,(255,255,255))
        window.blit(text,(10, 50))

        text = font1.render('Счёт:' + str(score),1,(255,255,255))
        window.blit(text,(10, 20))

        text = font1.render( 'Жизни:' + str(life),1,(255,255,255))
        window.blit(text,(10, 80))

        if lost >= 3:
            finish = True
            window.blit(lose, (200,200))
        if score >= 10:
            finish = True
            window.blit(win, (200,200))
        
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(3, 6))
            monsters.add(monster)
            score+=1

        if sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, asteroids, True)
            life = life -1




        
    

        player.update()
        asteroids.update()
        monsters.update()
        bullets.update()
        player.reset() 
        bullets.draw(window)
        asteroids.draw(window) 
        monsters.draw(window)     
        display.update()
    time.delay(50)