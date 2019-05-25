import pygame
import sys
from random import randint
 
### playable by humans
cPlayers = 2
cRobots = 0
cApples = 1
speed = 80
# how long to wait between moves, in milliseconds
initialLength = 5
lengthPerApple = 10
dXSquare = 10 # size of each square, in pixels
dXScreen = 60 # width of game screen, in squares
dYScreen = 60
# height of game screen, in squares
 
### fun to watch
##cPlayers = 0
##cRobots = 100
##cApples = 2000
##speed = 5 # how long to wait between moves, in milliseconds
##initialLength = 1
##lengthPerApple = 200
##dXSquare = 1 # size of each square, in pixels
##dXScreen = 800 # width of game screen, in squares
##dYScreen = 800 # height of game screen, in squares
 
dXBorder = 0 # border width, in pixels
 
 
def drawSquare(scr,xy,color):
    pygame.draw.rect(scr, color, (xy[0] * dXSquare + dXBorder, xy[1] * dXSquare + dXBorder,dXSquare,dXSquare))
 
class Dir():
    East,North,West,South = range(4)
 
def left(d):
    return (d + 1) % 4
def right(d):
    return (d + 3) % 4
def opposite(d):
    return (d + 2) % 4
 
def squareAdjacent(xy, d):
    #return (x,y) one step in given direction
    if d not in range(0,4):
        print (d, d%4)
    (dX,dY) = [(1,0),(0,-1),(-1,0),(0,1)][d]
    return (xy[0] + dX, xy[1] + dY)
 
class Snake():
    def __init__(self,xy,length,d,color):
        self.squares = [xy]
        self.length = length
        self.d = d
##        self.dPrev = d
        self.color = color
        self.mpKeyDir = {}
 
    def setKeys(self,keyNorth,keySouth,keyEast,keyWest):
        self.mpKeyDir[keyNorth] = Dir.North
        self.mpKeyDir[keySouth] = Dir.South
        self.mpKeyDir[keyEast] = Dir.East
        self.mpKeyDir[keyWest] = Dir.West
 
    def handleKey(self,key):
        if key in self.mpKeyDir:
            dNew = self.mpKeyDir[key]
            if dNew != opposite(self.dPrev):
                self.d = dNew
            return True
        else:
            return False
 
    def draw(self,scr):
        for xy in self.squares:
            drawSquare(scr, xy, self.color)
 
    def chooseMove(self,game):
        xy = self.squares[0] # head of snake
        xyAhead = squareAdjacent(xy,self.d)
        xyLeft = squareAdjacent(xy,left(self.d))
        xyRight = squareAdjacent(xy,right(self.d))
 
        leftOpen = game.isSquareOpen(xyLeft)
        rightOpen = game.isSquareOpen(xyRight)
         
        # apple immediately ahead?
        if xyAhead in game.apples:
            return # keep on
 
        # open space ahead?
        if game.isSquareOpen(xyAhead):
             
            # randomly turn from time to time
            if randint(0,self.length) == 0 and leftOpen:
                self.d = left(self.d)
            elif randint(0,self.length) == 0 and rightOpen:
                self.d = right(self.d)
             
            # turn towards apples?
            # turn towards opponent(s)?
         
        else:
            if leftOpen and rightOpen:
                if randint(0,1) == 0:
                    self.d = left(self.d)
                else:
                    self.d = right(self.d)
            elif leftOpen:
                   self.d = left(self.d)
            elif rightOpen:
                self.d = right(self.d)
            else:
                # we're screwed
                pass
 
    def move(self,game):

        self.dPrev = self.d
 
        if len(self.mpKeyDir) == 0:
            self.chooseMove(game)
         
        xyHead = self.squares[0]
        xyNew = squareAdjacent(xyHead,self.d)
 
        # hit something?      
        if not game.isSquareOpen(xyNew):
            game.killSnake(self)
            return True # dead
 
        # extend head
        self.squares[0:0] = [xyNew]
        game.setXY.add(xyNew)
 
        # consume apple?
        if xyNew in game.apples:
            game.apples.remove(xyNew)
            game.newApple()
            self.length += lengthPerApple
 
        # remove tail
        if len(self.squares) > self.length:
            xyTail = self.squares.pop()
            game.setXY.remove(xyTail)
 
        return False # not dead
 
class Game():
    def __init__(self):
        self.reset()
 
    def addSnake(self,snake):
        self.snakes.append(snake)
         
        # add snake head to set of occupied squares
        self.setXY.add(snake.squares[0])
 
    def reset(self):
        # restart if paused
        self.paused = False
 
        self.snakes = []
        self.setXY = set()
        self.apples = set()
 
        if cPlayers > 0:
            # add a snake on the right side controlled with arrow keys
            snake1 = Snake((dXScreen - 1, dYScreen / 2), initialLength, Dir.West, (255,255,255))
            snake1.setKeys(pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT)
            self.addSnake(snake1)
 
        if cPlayers > 1:
            # add snake on the left side controlled with WASD
            snake0 = Snake((0, dYScreen / 2), initialLength, Dir.East, (0,255,0))
            snake0.setKeys(pygame.K_w, pygame.K_s, pygame.K_d, pygame.K_a)
            self.addSnake(snake0)
 
        for i in range(0,cRobots):
            xy = self.chooseEmpty()
            if xy != None:
                snake = Snake(xy, initialLength, randint(0,3), (randint(100,255),randint(100,255),randint(100,255)))
                self.addSnake(snake)
 
        # add some apples
        for i in range(0,cApples):
            self.newApple()
 
    def chooseEmpty(self):
        # choose random position which isn't already occupied by snake or apple
 
        for i in range(0,1000):
            x = randint(0,dXScreen - 1)
            y = randint(0,dYScreen - 1)
            if (x,y) not in self.setXY and (x,y) not in self.apples:
                return(x,y)
 
        return None
     
    def newApple(self):
        # choose random position for apple which isn't already occupied by snake or apple
 
        xy = self.chooseEmpty()
        if xy != None:
            self.apples.add(xy)
 
    def isSquareOpen(self,xy):
        # hit wall?       
        if xy[0] < 0 or xy[0] >= dXScreen or xy[1] < 0 or xy[1] >= dYScreen:
            return False
 
        # hit snake?
        if xy in game.setXY:
            return False
 
        return True
 
    def killSnake(self,snake):
        if len(snake.mpKeyDir) > 0: # player-controlled snake?
            # turn snake red and pause game (r to reset)
            snake.color = (255,0,0)
            self.paused = True
        else: # computer-controlled snake
            # remove snake
            for xy in snake.squares:
                self.setXY.remove(xy)
            self.snakes.remove(snake)
 
        # would be nice to add to list of snakes to animate dying
 
    def tick(self):
        if self.paused:
            return
         
        for snake in self.snakes:
            snake.move(self)
 
        if len(self.snakes) == 0:
            self.reset()
 
    def draw(self,scr):
        # draw background and border
        scr.fill((200,200,200))
        pygame.draw.rect(scr, (0,0,0), (dXBorder,dXBorder,dXScreen * dXSquare,dYScreen*dXSquare))
 
        # draw snakes
        for snake in self.snakes:
            snake.draw(scr)
 
        # draw apples
        for xy in self.apples:
            drawSquare(scr, xy, (255,100,0))
 
pygame.init()
scr = pygame.display.set_mode((dXScreen * dXSquare + 2 * dXBorder,dYScreen*dXSquare + 2 * dXBorder))
pygame.time.set_timer(pygame.USEREVENT+1, speed)
 
game = Game()
 
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            #print event
 
            for snake in game.snakes:
                snake.handleKey(event.key)
 
            if event.key == pygame.K_r:
                game.reset()
 
            elif event.key == pygame.K_SPACE:
                done = True
             
        elif event.type == pygame.USEREVENT + 1:
            game.tick()
 
    game.draw(scr)
    pygame.display.update()
 
 
pygame.display.quit()
pygame.quit()
print ("quitting")
