import pygame, random, math, time

WIDTH = 600
HEIGHT = 600
scale = 25 ## size of blocks in pixels
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT)) 

## A couple colors
WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (0,255,0)
BLACK = (0,0,0)


## the dictionary that keeps track of the grid
blocks = {}



class Block():

    def __init__(self, rect, index):
        
        self.index = index ## Where the block is in the dictionary
        self.rect = rect  ## pygame rect object 
        self.type = "empty" 
        self.color = BLACK 
        self.searched = False  ## all start of not searched, this is so you don't search a block twice
        self.parents = None ## parent is passed when a block is searched so that block knows where it came from
        
    
    def becomeSearched(self, parent):
        self.searched = True
        self.color = (100,100,100)
        self.parent = parent ## the block it came from
        
    def setPath(self):

        self.color = GREEN
        self.type = "path"
        
    def show(self):
        
        pygame.draw.rect(screen, self.color, self.rect)
        
        for event in pygame.event.get():
            pass
        
        pygame.display.update(self.rect) ## to save time I only update the display for each new block
        
    def becomeGoal(self):
        self.type = "goal"
        self.color = GREEN

    def becomeStart(self):
        self.type = "start"
        self.color = RED

    def becomeObstacle(self):
        self.type = "obs"
        self.color = (0,0, 255)

def getAdjacent(index):
    x , y = index
    left= (x-1 , y)
    right = (x+1 , y)
    down = (x, y+1)
    up = (x, y-1)
    return([up,down,left,right]) ## returns all four blocks around a given rect


def initBlocks():
    
    for x in range(math.floor(WIDTH / scale)): ## 
        for y in range(math.floor(HEIGHT / scale)):
            
            local_rect = pygame.Rect(x*scale, y*scale , scale, scale)
            
            blocks[(x,y)] = (Block(local_rect, (x,y))) ## creates a block class object with index = to the position in the blocks dictionary

active = [] ## this is a queue that is used to keep track of which block is being checked


def findPath():
    

    
    
    for block in blocks.values():
        
        if block.type == "start": ## finds starting block and adds to queue 
            active.append(block)
            break
        
        elif block.type == "goal": ## figures out which block you're getting to
            goal = block 

    while len(active) > 0: ## while queue basically
        
        current_block = active.pop(0) ## removes top from queue and makes current bloc
                                      ## ok because active is appened with current block later
        
        blocksAround = getAdjacent(current_block.index) 
        
        random.shuffle(blocksAround) ## this isn't necessary, just adds some noise
        
        for i in blocksAround: ## i is a key, like (3,4) 
            
            if i in blocks.keys(): ## prevents from checking blocks off screen
                
                localBlock = blocks[i] 

                if localBlock.type == "goal": ## if the adjacent block is the goal, start path

                    while current_block != None: 

                        current_block.setPath() ## becomes part of path, aka turns green

                        current_block.show() 
                        
                        current_block = current_block.parent ## repeats with the block it came from 

                        if current_block.type == "start":
                        
                            return ## to break out of the whole function "findPath"

                
                if localBlock.type == "empty" and not localBlock.searched:

                    localBlock.becomeSearched(current_block) ## change to gray (grey) (?)
                    
                    active.append(localBlock) ## if it's a new block add it to queue 

                    localBlock.show()

                #renderScreen()
                
            

    


    


            
            





initBlocks()

over = False
setUp1 = False
setUp2 = False

## These up coming while Loops are the work of a half asleep Eli, please don't judge##
while not setUp1:

    mouse = pygame.mouse.get_pos() 
    left_click = pygame.mouse.get_pressed()[0] ## if I were smart I would've put this in the event loop

    for block in blocks.values(): ## this is the actual block class object as opposed to the key
        if left_click and block.rect.collidepoint(mouse): ## selects the block you clicked
            block.becomeObstacle() 
            block.show()
            
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: ## this doesn't work until the last loop thanks to my dumb design
            setUp1 = over
            over = True
    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: ## breaks out of the first loop
                setUp1 = True
     
    
    pygame.display.update()


while not setUp2:

    mouse = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]

    for block in blocks.values():
        if left_click and block.rect.collidepoint(mouse):
            block.becomeStart()
            block.show()
            setUp2 = True ## breaks out of loop, next click is goal
            pygame.display.update()
            time.sleep(.5) ## this is here so you don't turn the start block into the goal immediately
            
            
            
            
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            setUp2 = True
            over = True
    
      
     
    
    pygame.display.update()


setUp3 = False
while not setUp3:

    mouse = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]

    for block in blocks.values():
        if left_click and block.rect.collidepoint(mouse):
            block.becomeGoal() ## greenify ! :)
            block.show()
            setUp3 = True
            
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            setUp2 = over
            over = True
    
                
     
    
    pygame.display.update()
     

    

findPath() ## spooky magic
    




        
