import pygame as p
import pygame.freetype
from random import randint
import sys
import os

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (35, 35)

fps = 60
frameTime = 1000/fps

red = 100, 0, 0
gre = 0, 100, 0
blu = 0, 0, 100
yel = 200, 200, 0


def clip(val, minval, maxval):
    return min(max(val, minval), maxval)


def dist(c1, c2):
    return ((c2.x - c1.x) ** 2 + (c2.y - c1.y) ** 2)**0.5


def press(pressed):
    global pressMem
    pre = pressed[0]

    if pre == 0:
        pressMem = []
        return 0
    elif pre == 1 and 1 in pressMem:
        pressMem.append(1)
        return 0
    elif pre == 1 and 1 not in pressMem:
        pressMem.append(1)
        return 1


def img(filename, surface, xy):
    surface.blit(images[filename], xy)


class entity:
    def __init__(self, x, y, r, lives, vx=0, vy=0):
        self.r = r
        self.speed = [vx, vy]
        self.rect = p.Rect(x - self.r, y - self.r, 2 * self.r, 2 * self.r)
        self.x = self.rect.left + self.r
        self.y = self.rect.top + self.r
        self.lives = lives
        self.points = lives

    def act(self):
        self.rect = self.rect.move(self.speed)

        #border collision
        #if self.rect.left < 0:
        #    self.speed[0] *= -1
        #if self.rect.right > dim[0]:
        #    self.speed[0] *= -1
        #if self.rect.top < 0:
        #    self.speed[1] *= -1
        #if self.rect.bottom > dim[1]:
        #    self.speed[1] *= -1

        #clipping
        #self.rect.left = clip(self.rect.left, 0, dim[0])
        #self.rect.right = clip(self.rect.right, 0, dim[0])
        #self.rect.top = clip(self.rect.top, 0, dim[1])
        #self.rect.bottom = clip(self.rect.bottom, 0, dim[1])

    def rev(self):
        self.speed[0] *= -1
        self.speed[1] *= -1


p.init()
p.font.init()

dim = [800, 600]
sur = p.display.set_mode(dim)
bg = p.Surface(sur.get_size())
bg.fill((0, 0, 0))

font = p.freetype.Font(r'Resources\Pixeled.ttf', 20)

images = {'ene1': p.transform.scale(p.image.load(r'Resources\ene1.png'), [40, 40]),
          'ene2': p.transform.scale(p.image.load(r'Resources\ene2.png'), [40, 40]),
          'ene3': p.transform.scale(p.image.load(r'Resources\ene3.png'), [40, 40]),
          'ene4': p.transform.scale(p.image.load(r'Resources\ene4.png'), [40, 40]),
          'play': p.transform.scale(p.image.load(r'Resources\play.png'), [40, 40]),
          'bullet': p.transform.scale(p.image.load(r'Resources\bullet.png'), [8, 8])
          }

points = 0

r = 20

enemies = []
bulls = []

for y in range(1, 5):
    for x in range(1, 15):
        enemies.append(entity(x * 50, 10 + y * 50, 20, 1 + x%4, 1, 0))

tmp = 1
pressMem = []
time = 0

while 1:
    for event in p.event.get():
        if event.type == p.QUIT:
            sys.exit()

    mousePos = p.mouse.get_pos()
    pressed = p.mouse.get_pressed()

    sur.blit(bg, (0, 0))

    font.render_to(sur, (10, 10), 'Score: ' + str(points), yel)

    img('play', sur, [int(mousePos[0] - r), dim[1] - r - 40])

    time += 1
    shot = -1

    for x in enemies:
        img(str('ene' + str(x.lives)), sur, x)
        x.act()

        if press(pressed):
            bulls.append(entity(int(mousePos[0]), dim[1] - r - 40, 4, 0, 0, -10))

        if time == 30:
            x.rev()

    for x in bulls:
        img(str('bullet'), sur, x)
        x.act()

        hit = x.rect.collidelist(enemies)
        if hit != -1:
            bulls.remove(x)
            shot = hit

        if x.rect.top < 0 - 2 * x.r:
            bulls.remove(x)

    if shot != -1:
        if enemies[shot].lives > 1:
            enemies[shot].lives -= 1
        else:
            points += enemies[shot].points
            enemies.pop(shot)

    if time == 30:
        time = 0

    p.time.delay(int(frameTime))
    p.display.flip()

