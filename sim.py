import pygame, sys, random, math, time, pygame_gui
from pygame.locals import *

pygame.init()
vec = pygame.math.Vector2

## Organism variables

OSIZE = 5 #size of the 3x3 organism
ORGANISMS = 10 #the number of organisms on the screen

## Food variables

FSIZE = 10
FOODS = 1000

## Light variables#
LSIZE = 1
LIGHTSPEED = 10

## Creation variables
BSIZE = 27


## Game variables

WIDTH = 1100
HEIGHT = 700
FPS = 12
FramesPerSecond = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Evolution game')

##attempting to setup a gui window

manager = pygame_gui.UIManager((WIDTH, HEIGHT))

reset_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, HEIGHT-75), (WIDTH/11, HEIGHT/14)),text='Restart',manager=manager)

generate_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((850, HEIGHT-50), (WIDTH/11, HEIGHT/14)),text='Generate',manager=manager)


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
        #print('##### \n','speed: ', self.speed, '\n', 'mouths: ', self.mouth, '\n', 'poopers: ', self.production, '\n', 'movement scheme: ', self.movement, '\n', 'health: ', self.health, '\n', 'vision: ', self.sight, '\n', '#####\n')        
        #print(self.makeUp)

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
        if self.pos.y > HEIGHT-HEIGHT/4:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT-HEIGHT/4

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
         hitWall = pygame.sprite.spritecollide(self, all_walls, False)

         if hitFood:
             self.kill()

class Food(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        super().__init__()
        self.surf = pygame.Surface((FSIZE, FSIZE))
        self.surf.fill((0,255,0))
        self.rect = self.surf.get_rect(center=(posx, posy))

        self.life = 0
        self.pos = vec((posx, posy))

    def update(self):
        self.life += 1
        if self.life > 100:
            self.surf = pygame.Surface((FSIZE*2, FSIZE*2))
            self.surf.fill((0,255,0))
            self.rect = self.surf.get_rect(center=(self.pos.x, self.pos.y))

        if self.life > 150:
            FOOD = Food(self.pos.x+2*FSIZE, self.pos.y+2*FSIZE)
            all_sprites.add(FOOD)
            all_foods.add(FOOD)


class Wall(pygame.sprite.Sprite):
    def __init__(self, posx, posy, sizex, sizey):
        super().__init__()
        self.surf = pygame.Surface((sizex, sizey))
        self.surf.fill((173, 169, 183))
        self.rect = self.surf.get_rect(center=(posx, posy))

    def update(self):
        hitFood = pygame.sprite.spritecollide(self, all_foods, True)
        hitLight = pygame.sprite.spritecollide(self, all_lights, True)

class Creation(pygame.sprite.Sprite):
    def __init__(self, posx, posy):
        super().__init__()
        self.surf = pygame.Surface((BSIZE, BSIZE))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect(center=(posx, posy))

        self.color = (0,0,0)

    def update(self, color):
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surf.fill((color))
            self.color = color

class Typecell(pygame.sprite.Sprite):
    def __init__(self, posx, posy, color):
        super().__init__()
        self.surf = pygame.Surface((BSIZE, BSIZE))
        self.surf.fill((color))
        self.rect = self.surf.get_rect(center=(posx, posy))

        self.color = color

    def update(self):
        if pygame.mouse.get_pressed()[0] and self.rect.collidepoint(pygame.mouse.get_pos()):
            #print(self.color)
            return self.color


def count(type):
    counter = 0
    for cock in all_sprites: 
        if str(cock) == type:
            counter += 1
    return counter
            

## Defining all the sprite groups

all_sprites = pygame.sprite.Group()
all_organisms = pygame.sprite.Group()
all_foods = pygame.sprite.Group()
all_lights = pygame.sprite.Group()
all_walls = pygame.sprite.Group()
creation_background = pygame.sprite.Group()
picker_background = pygame.sprite.Group()


def main(food, organism):

    ## Defining all resets
    initFood = food
    initOrganism = organism

    

    ## Spawning all sprites into the game

    WALL = Wall(WIDTH/2, HEIGHT, WIDTH, HEIGHT/4)
    all_sprites.add(WALL)
    all_walls.add(WALL)

    for ORGANISM in range(0, ORGANISMS):
        ORGANISM = Organism(random.randint(0, WIDTH), random.randint(0, HEIGHT-HEIGHT/4), 100, random.randint(0, 4), ['genOne'])
        all_sprites.add(ORGANISM)
        all_organisms.add(ORGANISM)

    for FOOD in range(0, FOODS):
        FOOD = Food(random.randint(0, WIDTH), random.randint(0, HEIGHT))
        all_sprites.add(FOOD)
        all_foods.add(FOOD)

    for i in [1030, 1030+BSIZE, 1030+2*BSIZE]: #placing the background asindividual cells that can be easily colored
        for j in [630, 630+BSIZE, 630+2*BSIZE]:
            BACK = Creation(i, j)
            creation_background.add(BACK)

    for i in [860, 860+BSIZE, 860+2*BSIZE, 860+3*BSIZE, 860+4*BSIZE, 860+5*BSIZE]: #picking what cell type u wanna place
        if i == 860:
            BACK = Typecell(i, 630, (247, 23, 53))
            picker_background.add(BACK)
        if i == 860+1*BSIZE:
            BACK = Typecell(i, 630, (254, 185, 95))
            picker_background.add(BACK)
        if i == 860+2*BSIZE:
            BACK = Typecell(i, 630, (78, 128, 152))
            picker_background.add(BACK)
        if i == 860+3*BSIZE:
            BACK = Typecell(i, 630, (242, 206, 230))
            picker_background.add(BACK)
        if i == 860+4*BSIZE:
            BACK = Typecell(i, 630, (82, 50, 73))
            picker_background.add(BACK)
        if i == 860+5*BSIZE: 
            BACK = Typecell(i, 630, (0,0,0))
            picker_background.add(BACK)



    ## text parameters
    font = pygame.font.Font('freesansbold.ttf', 25)

    ## creation parameter
    current_color = (0,0,0)
    
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

            

            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == reset_button:
                    for entity in all_sprites:
                        entity.kill()
                    main(initFood, initOrganism)

                if event.ui_element == generate_button:
                    new_organism = []
                    position = [(0,0), (0,5), (0,10), (5,0), (5,5), (5,10), (10,0), (10,5), (10,10)]
                    counter = 0
                    for cell in creation_background:
                        if cell.color == (247, 23, 53):
                            new_organism.append(['heart', position[counter],cell.color])
                        if cell.color == (254,185,95):
                            new_organism.append(['mouth', position[counter],cell.color])
                        if cell.color == (78,128,152):
                            new_organism.append(['mover', position[counter],cell.color])
                        if cell.color == (242,206,230):
                            new_organism.append(['armour', position[counter],cell.color])
                        if cell.color == (92,50,73):
                            new_organism.append(['pooper', position[counter],cell.color])
                        if cell.color == (0,0,0):
                            new_organism.append(['empty', position[counter],cell.color])
                        counter += 1
                    ORGANISM = Organism(random.randint(0,WIDTH), random.randint(0, HEIGHT-HEIGHT/4), 100, random.randint(0, 4), new_organism)
                    all_sprites.add(ORGANISM)
                    all_organisms.add(ORGANISM)
                    if counter > len(position):
                        counter = 0

            manager.process_events(event)

        manager.update(FPS)

        screen.fill((0,0,0))

        ## gui stuff

        organism_text = count('<Organism Sprite(in 2 groups)>')
        number_organisms = font.render(('Number of creatures: '+str(organism_text)), True, (17, 157, 164),(45, 46, 46))
        number_organisms_Rect = number_organisms.get_rect(center=(300, HEIGHT-70))

        food_text = count('<Food Sprite(in 2 groups)>')
        number_foods = font.render(('Number of foods: '+str(food_text)), True, (17, 157, 164),(45, 46, 46))
        foods_rect = number_foods.get_rect(center=(300, HEIGHT-35))

        organisms_init = font.render(('Starting creatures: '+str(initOrganism)), True, (17, 157, 164),(45, 46, 46))
        initorgan_rect = organisms_init.get_rect(center=(700, HEIGHT-70))

        foods_init = font.render(('Starting foods: '+str(initFood)), True, (17, 157, 164),(45, 46, 46))
        initfood_rect = foods_init.get_rect(center=(700, HEIGHT-35))


        

        for entity in all_sprites:  #calling all the sprites
            screen.blit(entity.surf, entity.rect)
            entity.update() #updating all the sprites at the same time

        for piece in picker_background:
            screen.blit(piece.surf, piece.rect)
            if str(piece.update()) != 'None':
                current_color = piece.update()
            

        for piece in creation_background:
            screen.blit(piece.surf, piece.rect)
            piece.update(current_color)
        

        screen.blit(number_organisms, number_organisms_Rect)
        screen.blit(number_foods, foods_rect)
        screen.blit(organisms_init, initorgan_rect)
        screen.blit(foods_init, initfood_rect)

        manager.draw_ui(screen)

        pygame.display.update()
        FramesPerSecond.tick(FPS)

main(FOODS, ORGANISMS)