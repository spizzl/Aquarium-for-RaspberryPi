import pygame
import sys
import math

class Aquarium():

    def __init__(self):
        pygame.init()
        self.screen = Display()
        pygame.mouse.set_visible(1)
        pygame.key.set_repeat(1, 30)
        self.clock = MainClock()
        self.run_state = True
        self.backgroud = Object("back1_small.ppm")
        self.thomas = Fish()
        self.bubbles = []

    def MainLoop(self):
        x = 1
        while self.run_state:
            self.clock.tick()
            self.EventHandling()
            self.backgroud.place()
            for b in self.bubbles:
                if b.visible:
                    b.clock()
                else:
                    b = None
            self.thomas.clock()
            self.screen.load()
    def EventHandling(self):
        #-------ESCAPE EVENT Handling
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.run_state = False
            if e.type == pygame.MOUSEBUTTONUP:
                self.thomas.tab(pygame.mouse.get_pos())
                self.bubbles.append(Bubbles(self.thomas.posx, self.thomas.posy, self.thomas.dir))
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
        elif self.y <= 0:
            self.visible = False
    def clock(self):
        self.moveup()
        self.image.place(self.x, self.y)

class Fish():
    def __init__(self):
        self.fishl = Object("fishl.png")
        self.fishr = Object("fishr.png")
        self.posx = 53
        self.posy = 23
        self.estimatedcords = []
        reacting = [0, 0, 5, 10, 12, 20, 21, 21, 25, 30, 37, 44, 44, 49, 63, 112, -1, -1, -1]
        self.freeze = True
        self.speed = 1
        self.speedx = 0
        self.dir = 'l'
        self.speedy = 0

    def tab(self, mouse):
        self.calc(mouse)
        self.freeze = False
        #53
        #23

    def move(self):
        self.posx += self.speedx
        self.posy += self.speedy

    def clock(self):
        if self.dir == 'l':
            self.fishl.place(self.posx, self.posy)
        else:
            self.fishr.place(self.posx, self.posy)

        if not self.freeze:
            self.move()
            if math.ceil(self.calcdist()[0]) == 0: self.freeze = True

    def calcdist(self):
        distx = self.estimatedcords[0]-(self.posx+45)#Actual Center
        disty = self.estimatedcords[1]-(self.posy+23)
        return (distx, disty)


    def calc(self, cords):
        self.estimatedcords = cords
        distx, disty = self.calcdist()
        rads = math.atan2(distx, disty)
        rads %= 2*math.pi
        degs = math.ceil(math.degrees(rads))
        self.speedx = math.sin(rads) * self.speed
        self.speedy = math.cos(rads) * self.speed

        if degs <= 180:
            self.dir = 'r'
        else:
            self.dir = 'l'
