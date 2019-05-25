## linear regression calculator using pygame ##
import pygame, sys, os, time
import math

WIDTH = 600
HEIGHT = 600
scale = 100
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
WHITE = (255,255,255)

points = []

def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()


def initGrid(surface):
    new = 0
    
    for i in range (int(WIDTH / scale)):
        new = new + i*scale
        pygame.draw.line(surface, WHITE,(new,0),(new,HEIGHT))
        new = 0
        
    
    for i in range(int(HEIGHT / scale)):
        new = new + i*scale
        pygame.draw.line(surface, WHITE,(0,new),(WIDTH,new))
        new = 0

def message_display(text, x= WIDTH/2, y=HEIGHT/2, size = 20):
    largeText = pygame.font.Font('freesansbold.ttf',size)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x,y)
    screen.blit(TextSurf, TextRect)

def regression(lst):
    xpoints = []
    ypoints = []
    for point in lst:
        xpoints.append(point[0])
        ypoints.append(point[1])

    xMean = (sum(xpoints)) / len(xpoints)
    yMean = (sum(ypoints)) / len(ypoints)

    slopeTop = 0
    slopeBottom = 0

    
    
    for point in lst:
        
        slopeTop += (point[0]-xMean)*(point[1]-yMean)
        slopeBottom += (point[0]-xMean)*(point[0]-xMean)

    slope = slopeTop / slopeBottom
        
    
    yIntercept = yMean - (slope*xMean)


    return slope, yIntercept

    


done = False


slope = 0
yIntercept = 0
while not done:
    initGrid(screen)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    mouse_pos= pygame.mouse.get_pos()
    clicked = bool(pygame.mouse.get_pressed()[0])

    if clicked:
        points.append(mouse_pos)

    if len(points) >= 2:
        graph = regression(points)
        slope = round(graph[0],4)
        yIntercept = round(graph[1],4)

        y1 = (0,yIntercept)
        y2 = (WIDTH, (WIDTH*slope+yIntercept))
        pygame.draw.line(screen, (255,0,0), y1, y2, 5)
    
    message_display('Slope: '+str(slope), WIDTH - 300, 100,50)

    message_display('Equation: y= '+str(slope)+'x'+str(yIntercept), WIDTH - 290, HEIGHT-90,10)
    
    
    time.sleep(.1)
    
    for point in points:
        pygame.draw.circle(screen,WHITE,(point[0],point[1]),5)
        
    pygame.display.update()

    screen.fill((0,0,0))
    
    
    
pygame.display.quit()
pygame.quit()
print ("quitting")
