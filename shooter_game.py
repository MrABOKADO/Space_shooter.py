from random import *
from pygame import *
font.init()
font2 = font.SysFont('Arial', 36)
mixer.init()
game = True
finish = False
FPS = 80
lost = 0
score = 0
clock = time.Clock()
win = display.set_mode((700, 500))
display.set_caption('Шутер')
backround = transform.scale(image.load('galaxy.jpg'), (700, 500))


mixer.music.load('space.ogg')
mixer.music.play()


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, player_speed, size_x, size_y):
        super().__init__()
        self.image=transform.scale(image.load(player_image),(size_x, size_y))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 700:
            self.rect.x = randint(80, 500 - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
bullets = sprite.Group()

rocket = Player('rocket.png', 100, 400, 5, 50, 50)
ufo = Enemy('ufo.png', 400, 200, 1, 50, 50)

monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png', randint(40, 500 - 80), -40,randint(1, 2), 50, 50)
    monsters.add(monster)

while game:
    if finish != True:
        win.blit(backround, (0, 0))
        rocket.reset()
        rocket.update()
        monsters.draw(win)
        monsters.update()
        bullets.draw(win)
        bullets.update()
        lose = font2.render('Пропусков ' + str(lost), 1, (255, 0, 0))
        loser = font2.render('You LOST!', 2, (255, 0, 0))
        wins = font2.render('You WIN!', 2, (255, 255, 0))
        win.blit(lose, (0, 0))
        winner = font2.render('Есть пробитие: '+ str(score), 1, (100, 255, 255))
        win.blit(winner, (0, 25))
    if sprite.spritecollide(rocket, monsters, False):
        win.blit(loser, (300, 250))
        finish = True
    if lost == 3:
        win.blit(loser, (300, 250))
        finish = True
    if sprite.groupcollide( monsters, bullets, True, True):
        score += 1
        monster = Enemy('ufo.png', randint(40, 500 - 80), -40,randint(1, 2), 50, 50)
        monsters.add(monster)
        if score == 10:
            finish = True
            win.blit(wins, (300, 250))
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()

    clock.tick(FPS)
    display.update()