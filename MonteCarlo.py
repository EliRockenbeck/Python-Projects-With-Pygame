import pygame, random, math


WIDTH = 600
HEIGHT = WIDTH
pygame.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT)) 

## A couple colors
WHITE = (255,255,255)

COLOR_OF_DOTS_OUTSIDE_CIRCLE = (255, 0, 0)
COLOR_OF_DOTS_INSIDE_CIRCLE = (0,255,0)
BLACK = (0,0,0)

points = []
points_inCircle = []



def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

def message_display(text, x= WIDTH/2, y=HEIGHT/8, size = 20):
    largeText = pygame.font.Font('freesansbold.ttf',size)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (x,y)
    screen.blit(TextSurf, TextRect)


class Point():

    def __init__(self, position):

        self.pos = position
        self.color = BLACK
        self.inCircle = False

    def getInCircle(self, center, radius):

        ## get euclidean distance from center
        x,y = self.pos
        centX, centY = center
        a = x - centX
        b = y - centY
        distance = math.sqrt((a**2+b**2))
        if distance <= radius:
            self.inCircle = True
##        else:
##            return False

    def show(self):

        if self.inCircle:
           self.color = COLOR_OF_DOTS_INSIDE_CIRCLE
        else:
            self.color = COLOR_OF_DOTS_OUTSIDE_CIRCLE
            
        pygame.draw.circle(screen, self.color, self.pos, 1, 1)



def createPoint():
    x,y = (random.randint(0,WIDTH), random.randint(0,HEIGHT))
    point = Point((x,y))
    points.append(point)
    point.getInCircle((WIDTH/2, HEIGHT/2), (WIDTH / 2))
    
    if point.inCircle:
        points_inCircle.append(point)

    point.show()
    
center = (int(WIDTH/2), int(HEIGHT/2))

pi = 0
register = 0
message_display('Pi guestimate = '+str(pi))
clearRect = pygame.Rect(200, 65, 200, 20)
howOftenToCheck = 50 ## more accurate with higher numbers, faster by a lot with smaller


while True:
    register += 1
    pygame.draw.circle(screen, WHITE, center, int(WIDTH/2), 1)
    createPoint()
    for event in pygame.event.get():
        pass
    if len(points_inCircle) > 0:
        pi = 4 * (len(points_inCircle) / len(points))
    if register % howOftenToCheck == 0:
        pygame.draw.rect(screen, BLACK, clearRect)
        message_display('Pi guestimate = '+str(round(pi, 2)))
        
    pygame.display.update()
    
        
        

