import pygame, random, math, time



WIDTH = 200
HEIGHT = 200
scale = 3 ## size of each block in pixels, lower number = higher resolution
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Voronoi")
euclidean = True
manhattan = False

blocks = {}
seeds = []


class Block():

    def __init__(self, rect, index):
        
        self.index = index ## Where the block is in the dictionary
        self.rect = rect  ## pygame rect object 
        self.type = "notSeed" 
        self.color = (0,0,0)
        self.parent = None ## parent is passed when a block is searched so that block knows where it came from


    def becomeSeed(self):
        self.color = randomColor()
        self.type = "seed"

        
    def show(self):
        
        pygame.draw.rect(screen, self.color, self.rect)
        




def randomColor(grey = False):
    if grey:
        greyVal = random.randint(0,255)
        return((greyVal,greyVal,greyVal))
    else:
        return(random.randint(0,255),random.randint(0,255),random.randint(0,255))

    
def getDistance(a, b):


    aX, aY = a
    bX, bY = b

    if manhattan:
        return (abs(aX-bX)+abs(aY-bY))
    elif euclidean:
        return (((aX - bX)**2) + ((aY - bY)**2))

def initBlocks():
    
    for x in range(math.floor(WIDTH / scale)):  
        for y in range(math.floor(HEIGHT / scale)):
            
            local_rect = pygame.Rect(x*scale, y*scale , scale, scale)
            
            blocks[(x,y)] = (Block(local_rect, (x,y)))


##if clicked seeds.append ##

def getClosest(checkBlock):

    shortestDistance = 1000000
    
    
    for seed in seeds:
        #print(getDistance(checkBlock.index, seed.index))
        currentDistance = getDistance(checkBlock.index, seed.index) ## gets distance between seed and block
        
        if  currentDistance < shortestDistance:
            shortestDistance = currentDistance
            closestSeed = seed
            
    return blocks[closestSeed.index]






initBlocks()
setUp = False

while not setUp:
    
    mouse = pygame.mouse.get_pos() 
    left_click = pygame.mouse.get_pressed()[0]
    
    for block in blocks.values():
        
        if left_click and block.rect.collidepoint(mouse): 
            if block not in seeds:
                block.becomeSeed()
                seeds.append(block)
        block.show()

    for event in pygame.event.get():
    
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: ## breaks out of the first loop
                setUp = True
     
    
    pygame.display.update()


for block in blocks.values():
    if block not in seeds:
        block.parent = getClosest(block)
        block.color = block.parent.color
    block.show()
    
for event in pygame.event.get():

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE: ## breaks out of the first loop
            setUp = True
 

pygame.display.update()

    

        
