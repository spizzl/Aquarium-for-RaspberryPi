import pygame
import sys
from math import ceil, sin, cos, atan2, degrees, pi
from random import choice, randrange
class Aquarium():

    def __init__(self):
        pygame.init()
        self.screen = Display()
        pygame.mouse.set_visible(1)
        pygame.key.set_repeat(1, 30)
        self.clock = MainClock()
        self.run_state = True
        self.backgroud1 = Object("back1_small.ppm")
        self.thomas = Fish()
        self.bubbles = []
        self.food = []

    def MainLoop(self):
        x = 1
        while self.run_state:
            self.clock.tick()
            self.EventHandling()
            self.backgroud.place()

            for f in self.food:
                f.clock()

            for b in self.bubbles:
                if b.visible:
                    b.clock()
                else:
                    b = None
            self.thomas.clock(self.food)
            self.screen.load()
    def EventHandling(self):
        #-------ESCAPE EVENT Handling
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.run_state = False
            if e.type == pygame.MOUSEBUTTONUP:
                if e.button == 1:
                    self.thomas.tab(pygame.mouse.get_pos())
                    self.bubbles.append(Bubbles(self.thomas.posx, self.thomas.posy, self.thomas.dir))
                elif e.button == 3:
                    self.food.append(FishFood(pygame.mouse.get_pos()[0]))
                else:
                    pass
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

class MainClock():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.clockspeed = 40

    def tick(self):
        self.clock.tick(self.clockspeed)

class Display():

    def __init__(self):
        self.screen = pygame.display.set_mode((480, 320))
        pygame.display.set_caption("Aquarium")

    def setBackground(self):
        self.screen.fill((255, 0, 0))

    def load(self):
        pygame.display.flip()

class Object(Display):

    def __init__(self, name):
        super().__init__()
        self.image = self.loadImage(name)

    def loadImage(self, filename, colorkey=None):

        image = pygame.image.load(filename)

        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()

        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
                image.set_colorkey(colorkey, pygame.RLEACCEL)

        return image

    def place(self, x=0, y=0):
        self.screen.blit(self.image, (x, y))

class Bubbles():
    def __init__(self, x, y, dir):
        xoffset = 0 if dir == 'l' else 80
        self.image = Object("bubbles.png")
        self.x = x + xoffset
        self.y = y - 20
        self.visible = True

    def activate(self, x, y):
        self.x = x
        self.y = y - 20

    def moveup(self):
        if self.y != None:
            self.y -= 3
        if self.y <= -50:
            self.visible = False
    def clock(self):
        self.moveup()
        self.image.place(self.x, self.y)


class FishFood():

    def __init__(self, x):
        self.x = x
        self.y = 0
        self.image = Object("food{}.png".format(randrange(1, 5)))

    def clock(self):
        if self.y < 303:
            self.y += 1
            self.image.place(self.x, self.y)
            return True
        else:
            self.image.place(self.x, self.y)
        return False


class Fish():
    def __init__(self):
        self.imageL = Object("fishl.png")
        self.imageR = Object("fishr.png")
        self.posx = 53
        self.posy = 23
        self.estimatedcords = []
        self.freeze = True
        self.speedx = 0
        self.speedy = 0
        self.dir = 'l'
        self.wait = -1

    def tab(self, mouse):
        self.calc(mouse)
        if self.freeze:
            reacting = [0, 0, 10, 20, 21, 25, 30, 37, 44, 44, 49, 57, 63, 79, 92, 94, 96, 112, 150, 212, 380, -1, -1]
            self.wait = choice(reacting)
        self.freeze = False
        #53
        #23

    def move(self):
        self.posx += self.speedx
        self.posy += self.speedy

    def clock(self, food):




        if len(food) is not 0:
            self.calc((food[0].x, food[0].y), 2)
            if ceil(self.calcdist(food[0].x, food[0].y)[0]) == 0: food.pop(0)
            self.move()

        if not self.freeze:
            if self.wait is not 0:
                self.wait -= 1
            else:
                if ceil(self.calcdist(self.estimatedcords[0], self.estimatedcords[1])[0]) == 0: self.freeze = True
                self.move()
        else:
            pass

        if self.dir == 'l':
            self.imageL.place(self.posx, self.posy)
        else:
            self.imageR.place(self.posx, self.posy)




    def calcdist(self, x, y):

        offsetx = 10 if self.dir == 'l' else 90
        distx = x-(self.posx+offsetx)#Actual Center
        disty = y-(self.posy+23)
        return (distx, disty)


    def calc(self, cords, speed=1):
        self.estimatedcords = cords
        distx, disty = self.calcdist(self.estimatedcords[0], self.estimatedcords[1])
        rads = atan2(distx, disty)
        rads %= 2*pi
        degs = ceil(degrees(rads))
        self.speedx = sin(rads) * speed
        self.speedy = cos(rads) * speed

        if degs <= 180:
            self.dir = 'r'
        else:
            self.dir = 'l'
