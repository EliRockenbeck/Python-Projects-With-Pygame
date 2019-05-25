##                                geneticCircle                             ##
import random
import math
import pygame
import operator
import time
from matplotlib import pyplot as plt

WIDTH = 1000
HEIGHT = 800


WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Genetic Algorithm")


population = 50
generations = 200
scale = 5 ## couldn't think of a better word, it's the range of starting numbers
mutationChance = 15 ## put in percent, i.e mutationChance = 10 means 10 percent
number_of_dots = 4 ## the smaller the faster, the bigger the more impressive
randomize_dots= False
corners = 0
dots = []
scores = []
plot_x = []
for i in range(generations):
    plot_x.append(i)

if WIDTH <= scale:
    WIDTH = scale + 1
if HEIGHT <= scale:
    HEIGHT = scale + 1
class Dot():
    def __init__(self,position):
        self.pos = position
        self.radius = 2

    def show(self):
        pygame.draw.ellipse(screen,WHITE,(self.pos[0], self.pos[1], 2*self.radius, 2*self.radius))
    
class Circle():

    def __init__(self, radius, position):

        self.radius = int(radius)
        self.pos = position
        self.color = WHITE
        self.area = (2*math.pi*self.radius)*(2*math.pi*self.radius)
        self.diameter = self.radius * 2
        self.fitness = 0
        self.center = (self.pos[0] + self.radius, self.pos[1] + self.radius)
        
    
    def eval(self):

        self.diameter = self.radius * 2
        self.area = math.pi*(self.radius)**2
        self.fitness = self.area / (WIDTH * HEIGHT)


        
        
        
    def offScreen(self):
        bottom_right = (self.pos[0] + self.diameter, self.pos[1] + self.diameter)
        if bottom_right[0] > WIDTH or bottom_right[0] < 0:
            self.fitness = -100
        if bottom_right[1] > HEIGHT or bottom_right[1] < 0:
            self.fitness = -100
        if self.pos[0] <= 0:
            self.fitness = -100
        if self.pos[1] <=0:
            self.fitness = -100



    ### VIEW HERE, IT'S TO SEE IF THE CIRCLE IS TOUCHING OR COVERING DOTS ###      
    def obstruction(self):
        self.center = (self.pos[0] + self.radius, self.pos[1] + self.radius)
        
        for dot in dots:
            dotCenter = (dot.pos[0] + dot.radius, dot.pos[1] + dot.radius)

            
            dist = math.hypot(self.center[0] - dotCenter[0] , self.center[1] - dotCenter[1])
            
            
            if dist <= (dot.radius + self.radius):
                self.fitness = self.fitness - 1
                self.color = RED


            
    def show(self):

        top_left = ((self.pos[0] - self.radius, self.pos[1] - self.radius))
        pygame.draw.ellipse(screen,self.color,(self.pos[0], self.pos[1], self.diameter, self.diameter))

    def dump(self):

        print("Radius: ",self.radius,"\nX position: ",self.pos[0],"\nY position: ",self.pos[1],"\nFitness: ",self.fitness)



def genetic():
    
    init_dots(randomize_dots, corners)
    #dotsPos = []
    
    circles = init_circles(population)

    for generation in range(generations):
        #print("Generation: ", generation)

        screen.fill(BLACK)
        for circle in circles:
            screen.fill(BLACK)
            circle.eval()
            circle.offScreen()
            circle.obstruction()
            circle.show()
            
        circles = selection(circles)

        crossover(circles)

        mutation(circles, mutationChance)

        #pygame.draw.lines(screen, WHITE, False, dotsPos)

        scores.append(circles[0].fitness)
        
        for event in pygame.event.get():
            pass
        
        #circles[0].show()
        
        for dot in dots:
            dot.show()

        circles[0].show()
        pygame.display.update()
        
    return circles[0]
        
    
    

    


        



    
##    for circle in sortedCircles:
##        print(circle.radius)
    
    




def init_circles(population):
    
    circles = []
    for i in range(population):
        radius = random.randint(1, scale)
        posX = random.randint(0, WIDTH - radius)
        posY = random.randint(0, HEIGHT - radius)
        position = (posX, posY)
        circle = Circle(radius , position)
        circles.append(circle)
    return circles


def init_dots(randomize = False, corners = False):
    if randomize:
        for i in range(number_of_dots):
            posX = random.randint(0,WIDTH - 4)
            posY = random.randint(0, HEIGHT - 4)
            dots.append(Dot((posX,posY)))
    if corners:
        dots.append(Dot((0,0)))
        dots.append(Dot((WIDTH, 0 )))
        dots.append(Dot((0,HEIGHT)))
        dots.append(Dot((WIDTH, HEIGHT)))
        
    else:
        while len(dots) != number_of_dots:
            for event in pygame.event.get():
                pass
            left_click = pygame.mouse.get_pressed()[0]
            mouseX = pygame.mouse.get_pos()[0]
            mouseY = pygame.mouse.get_pos()[1]
            if left_click == 1:
                dots.append(Dot((mouseX,mouseY)))
                time.sleep(.2)
            for dot in dots:
                dot.show()
            pygame.display.update()
                
        
def selection(circles):
    
    circles.sort(key=operator.attrgetter('fitness'))
    circles = list(reversed(circles))
    circles = circles[:int(.2 * len(circles))]
    return circles


def crossover(circles):
    
    for i in range(population):
        parent1 = random.choice(circles)
        parent2 = random.choice(circles)
        midpoint = ((parent1.pos[0]-parent2.pos[0]/2),(parent1.pos[1]-parent2.pos[1]/2))
        child1 = Circle(parent1.radius, midpoint)
        child2 = Circle(parent2.radius, midpoint)
        circles.append(child1)
        circles.append(child2)

def mutation(circles, percentChance):
    
    for circle in circles:

        if random.randint(0,100) <= percentChance:

            circle.radius = circle.radius + (random.randint(-4,40))
            circle.pos = (circle.pos[0] + (random.randint(-4,4)), circle.pos[1] + (random.randint(-4,4)))
        
        
def distance(p1,p2):
    distance = math.sqrt(((p1[0] - p2[0])**2) + (p1[1] - p2[1])**2)
    return distance
    



best = genetic()
best.dump()

plt.plot(plot_x,scores)

while True:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        pass
    for dot in dots:
        dot.show()
    best.show()
    pygame.display.update()
    plt.show()
    
    

    
