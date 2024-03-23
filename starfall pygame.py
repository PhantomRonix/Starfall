import random
import pygame

from math import ceil
pygame.init()
pygame.display.set_caption('Starfall')
WIDTH,HEIGHT = 1440,810
frames = 60

star_size_min = 1
star_size_max = 8

gravity_min = 1
gravity_max = 5

trail_lifetime_min = 1
trail_lifetime_max = 7

fade_min = 1
fade_max = 8

spawnchance = 0.200

BLACK = (0,0,0)
WHITE = (255,255,255)

def randomcolour():
    a = random.randint(0,255)
    b = random.randint(0,255)
    c = random.randint(0,255)
    return a,b,c


class star(pygame.sprite.Sprite):
    def __init__(self,scene):
        super().__init__()
        self.scene = scene
        self.colour = randomcolour()
        self.x = random.randint(0,WIDTH)
        self.y = 0
        self.size = random.randint(star_size_min,star_size_max)
        self.gravity = random.uniform(gravity_min,gravity_max)
        self.trail_lifetime = random.uniform(trail_lifetime_min,trail_lifetime_max)
        if random.randint(0,1) == 0:
            self.red_fade = random.randint(fade_min,fade_max)
            self.green_fade = random.randint(fade_min,fade_max)
            self.blue_fade = random.randint(fade_min,fade_max)

        else:
            self.red_fade = 1
            self.green_fade = 1
            self.blue_fade = 1
        self.image = pygame.Surface((self.size,self.size))
        self.image.fill(self.colour)
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x,self.y
        self.ground = random.randint(0,1) #0=fore,1=back
        if self.ground == 0:
            self.scene.foreground_objects.add(self)
        if self.ground == 1:
            self.scene.background_objects.add(self)
    def update(self):
        if self.y >= HEIGHT:
            if self.ground == 0:
                self.scene.foreground_objects.remove(self)
            elif self.ground == 1:
                self.scene.background_objects.remove(self)
        self.trail = trail(self,self.scene)
        self.y += self.gravity
        self.rect.topleft = self.x,self.y
        
        
class trail(pygame.sprite.Sprite):
    def __init__(self,parent,scene):
        super().__init__()
        self.parent = parent
        self.scene = scene
        self.colour = []
        self.alpha = 255
        self.red = int(parent.colour[0])
        self.green = int(parent.colour[1])
        self.blue = int(parent.colour[2])
        self.lifetime = self.parent.trail_lifetime
        self.x = parent.rect.left
        self.y = parent.rect.top
        self.image = pygame.Surface((parent.size,ceil(self.parent.gravity)))
        self.image.fill((self.red,self.green,self.blue))
        self.image.set_alpha(self.alpha)
        self.rect = self.image.get_rect()

        self.rect.topleft = self.x,self.y

        if self.parent.ground == 0:
            self.scene.foreground_objects.add(self)
        elif self.parent.ground == 1:
            self.scene.background_objects.add(self)
    def update(self):
        if self.red == 0 and self.green == 0 and self.blue == 0:
            if self.parent.ground == 0:
                self.scene.foreground_objects.remove(self)
            elif self.parent.ground == 1:
                self.scene.background_objects.remove(self)
        else:
            self.red = self.red - self.lifetime*self.parent.red_fade
            self.green = self.green - self.lifetime*self.parent.green_fade
            self.blue = self.blue - self.lifetime*self.parent.blue_fade
            self.alpha -= self.lifetime
            if self.red <= 0:
                self.red = 0
            if self.blue <= 0:
                self.blue = 0
            if self.green <= 0:
                self.green = 0
            self.colour = [self.red,self.green,self.blue]
            self.image.fill(self.colour)
            #self.image.set_alpha(self.alpha)
        
class Scene():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        self.foreground_objects = pygame.sprite.Group()
        self.background_objects = pygame.sprite.Group()
        self.entity_counter = 0
        self.end = False
        self.run()

    def update(self):
        self.foreground_objects.update()
        self.background_objects.update()
    def render(self):
        self.screen.fill(BLACK)
        self.foreground_objects.draw(self.screen)
        self.background_objects.draw(self.screen)
        pygame.display.update()

    def process(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        if random.random() <= spawnchance:
            self.star = star(self)
##        for entity in self.objects:
##            self.entity_counter += 1
##        print(self.entity_counter)
        self.entity_counter = 0
    def run(self):
        while not self.end:
            self.update()
            self.process()
            self.render()
            self.clock.tick(frames)

window = Scene()
