import pygame, sys, random, math, time
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2

## Organism variables

OSIZE = 5 #size of the 3x3 organism
ORGANISMS = 100 #the number of organisms on the screen

## Food variables

FSIZE = 10
FOODS = 1000

## Light variables#
LSIZE = 1
LIGHTSPEED = 10
## Game variables

WIDTH = 1100
HEIGHT = 700
FPS = 12
FramesPerSecond = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Evolution game')

##Defining classes

class Organism(pygame.sprite.Sprite):
    def __init__(self, posx, posy, heartSize, moveScheme, composition):
        super().__init__()
        self.surf = pygame.Surface((OSIZE*3, OSIZE*3))
        #self.surf.fill((255,255,255))                           #should be left blank and filled by cells later, might be visible for testing
        self.rect = self.surf.get_rect(center=(posx, posy))

        self.pos = vec((posx, posy))
        self.makeUp = composition
        self.compo = []

        self.health = heartSize
        self.hunger = 0
        self.movement = moveScheme
        self.speed = 5
        self.mouth = 0
        self.production = 0
        self.sight = 0

        
        #print('************ \n',self.makeUp , '\n',len(self.makeUp), '\n', '************ \n')

        if self.makeUp == ['genOne']:
            self.makeUp.pop()
            for i in [0, OSIZE, 2*OSIZE]:  #lazily placing all the cells 
                for j in [0, OSIZE, 2*OSIZE]:
                    RC = random.randint(0, 100) #can control the probability of each cell
                    if RC in range(0, 14):
                        self.Cell(i, j, (247, 23, 53), 'heart')
                    if RC in range(15, 29):
                        self.Cell(i, j, (254, 185, 95 ), 'mouth')
                    if RC in range(30, 44):
                        self.Cell(i, j, (78, 128, 152), 'mover')
                    if RC in range(45, 54):
                        self.Cell(i, j, (242, 206, 230), 'armour')
                    if RC in range(55, 60):
                        self.Cell(i, j, (172, 216, 170), 'eye')
                    if RC in range(61, 70):
                        self.Cell(i, j, (82, 50, 73), 'pooper')
                    if RC in range(71, 100):
                        self.Cell(i, j, (0, 0, 0), 'empty')
        else:
            if len(self.makeUp) > 9:
                del self.makeUp[:9]
            #print(self.makeUp)
            #print(len(self.makeUp))
            counter = 0
            #random.shuffle(self.makeUp)
            for i in [0, OSIZE, 2*OSIZE]:  #lazily placing all the cells 
                for j in [0, OSIZE, 2*OSIZE]:   
                    counter += 1
                    self.Cell(i, j, self.makeUp[counter][2], self.makeUp[counter][0])


        self.setStats()
        if self.sight >= 1:
            self.movement = 5
        print('##### \n','speed: ', self.speed, '\n', 'mouths: ', self.mouth, '\n', 'poopers: ', self.production, '\n', 'movement scheme: ', self.movement, '\n', 'health: ', self.health, '\n', 'vision: ', self.sight, '\n', '#####\n')
        

    ## defining all the different cell types for the organism
    def Cell(self, posx, posy, color, type): #each cell will be defined in the generation
        pygame.draw.rect(self.surf, ((color)), (posx, posy, OSIZE, OSIZE))
        cell = [type, (posx, posy), color]
        self.makeUp.append(cell)

    def setStats(self):
        for cell in self.makeUp:
            if cell[0] == 'heart':
                self.health += 10
            if cell[0] == 'mover':
                self.speed += 5
            if cell[0] == 'mouth':
                self.mouth += 1
            if cell[0] == 'pooper':
                self.production += 1
            if cell[0] == 'eye':
                self.sight += 1

    def look(self):
        pass


    def move(self):
        #setting up the different movement scheme
        if self.movement == 0 and self.speed == 5: #static without mover cell
            self.pos.x += 0
            self.pos.y += 0
        
        if self.movement == 0 and self.speed > 5: #poor guys just gonna loop and loop
            self.pos.x += self.speed
        
        if self.movement == 1 and self.speed > 5: #random with small range
            RL = random.randint(0,1)
            shifter = random.randint(-self.speed, self.speed)
            if RL == 1:
                self.pos.y += shifter
            if RL == 0:
                self.pos.x += shifter
        
        if self.movement == 2 and self.speed > 5: #random with large range
            RL = random.randint(0,1)
            shifter = random.randint(-self.speed*5, self.speed*5)
            if RL == 1:
                self.pos.y += shifter
            if RL == 0:
                self.pos.x += shifter

        if self.movement == 3 and self.speed > 5: #only moves vertically along y
            shifter = random.randint(-self.speed*2, self.speed*2)
            self.pos.y += shifter

        if self.movement == 4 and self.speed > 5: #only moves horizontally along x
            shifter = random.randint(-self.speed*2, self.speed*2)
            self.pos.x += shifter
        
        if self.movement == 5:
            self.movement = 0
            
        if self.movement == 6:
            self.pos.x += 10
                

        self.rect = self.surf.get_rect(center = (self.pos.x, self.pos.y))

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT

    def update(self):
        self.move()
        self.health -= 1 
        self.hunger -= 1                                   #Health drain per frame

        if self.health <= 0 and self.hunger >= 100:
            ORGANISM = Organism(self.pos.x+30, self.pos.y+30, 100, self.movement, self.makeUp)
            all_sprites.add(ORGANISM)
            all_organisms.add(ORGANISM)
            self.kill()
        if self.health<= 0 and self.hunger < 100:
            self.kill()

        if self.health <= 0 and self.hunger >= 200:
            ORGANISM = Organism(self.pos.x+30, self.pos.y+30, 100, self.movement, self.makeUp)
            all_sprites.add(ORGANISM)
            all_organisms.add(ORGANISM)
            self.kill()
        if self.health<= 0 and self.hunger < 100:
            self.kill()

        if self.mouth > 0:
            eating = pygame.sprite.spritecollide(self, all_foods, True)

            if eating:
                self.hunger += 10*self.mouth
        
            

        if self.production > 0:
            poop = random.randint(0,100)
            #print(self.hunger)
            if poop == 0:
                FOOD = Food(self.pos.x+30, self.pos.y+30)
                all_sprites.add(FOOD)
                all_foods.add(FOOD)
                self.hunger -= 1
        
        frameCounter = 0
        frameCheck = WIDTH/LIGHTSPEED
        if self.sight >= 1:
            #print(self.pos)
            LIGHTR = Light(self.pos.x+3*OSIZE, self.pos.y, 'forward')
            #LIGHTD = Light(self.pos.x, self.pos.y+3*OSIZE, 'down')
            all_sprites.add(LIGHTR)#, LIGHTD)
            all_lights.add(LIGHTR)#, LIGHTD)
            
            seeLight = pygame.sprite.spritecollide(self, all_lights, True)
            frameCounter += 1

            if seeLight and frameCounter != frameCheck:
                self.movement = 5
            else:
                self.movement = 6
                frameCounter = 0
        
       
## Setting up the Light class
class Light(pygame.sprite.Sprite):
    def __init__(self, posx, posy, direction):
        super().__init__()
        self.surf = pygame.Surface((LSIZE, LSIZE))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect(center=(posx, posy))

        self.pos = vec((posx, posy))
        self.direction = direction

    def move(self):
         
        self.pos.x += LIGHTSPEED
        
                 
        self.rect = self.surf.get_rect(center = (self.pos.x, self.pos.y))

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT

    def update(self):
         self.move()
         hitFood = pygame.sprite.spritecollide(self, all_foods, False)

         if hitFood:
             self.kill()

class Food(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        super().__init__()
        self.surf = pygame.Surface((FSIZE, FSIZE))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center=(posx, posy))

    def update(self):
        pass


## Defining all the sprite groups

all_sprites = pygame.sprite.Group()
all_organisms = pygame.sprite.Group()
all_foods = pygame.sprite.Group()
all_lights = pygame.sprite.Group()


## Defining all functions



## Spawning all sprites into the game

for ORGANISM in range(0, ORGANISMS):
    ORGANISM = Organism(random.randint(0, WIDTH), random.randint(0, HEIGHT), 100, random.randint(0, 4), ['genOne'])
    all_sprites.add(ORGANISM)
    all_organisms.add(ORGANISM)

for FOOD in range(0, FOODS):
    FOOD = Food(random.randint(0, WIDTH), random.randint(0, HEIGHT))
    all_sprites.add(FOOD)
    all_foods.add(FOOD)

## Main event

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == MOUSEBUTTONDOWN:
            #print(pygame.mouse.get_pos()[0])
            FOOD = Food(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            all_sprites.add(FOOD)
            all_foods.add(FOOD)

    screen.fill((0,0,0))

    for entity in all_sprites:  #calling all the sprites
        screen.blit(entity.surf, entity.rect)
        entity.update() #updating all the sprites at the same time

    pygame.display.update()
    FramesPerSecond.tick(FPS)