from random import *
import pygame 
import time

WIDTH = 1000
HEIGHT = 600
WHITE = (255,255,254)
BLACK = (0,0,0)
data=[]
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def data_set(length):
    for i in range(0,length):
        data.append(randint(0,HEIGHT))
    print(data)

def make_display(data_set):
    for i in range(0,len(data)):
        pygame.draw.rect(screen,WHITE,(i*10,HEIGHT-data[i], 10, data[i]))
    pygame.display.update()
def clear():
    screen.fill(BLACK)
def sort(data):
    shuffle(data)
def Sorted(data):
    for i in range(len(data)-1):
        if data[i] > data[i+1]:
            return False
    return True

meseeks = pygame.time.Clock()
while(True):
    iterations=1
    data = []
    l=input("data set: ")
    data_set(int(l))
    make_display(data)
    while not Sorted(data):
        clear()
        sort(data)
        make_display(data)
        meseeks.tick(100)
        iterations += 1
        for event in pygame.event.get():
            pass
    print(data)
    print(iterations)

        
    
