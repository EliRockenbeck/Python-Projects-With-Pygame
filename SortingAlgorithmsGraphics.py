from random import *
import pygame 
import time
WIDTH = 1275
HEIGHT = 500
 
WHITE = (255,255,255)
RED = (255,0,0)
BLACK = (0,0,0)
data=[]
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def data_set(length):
    for i in range(0,length):
        data.append(randint(0,HEIGHT))
    print(data)

def make_display(data_set):
    for event in pygame.event.get():
            pass
    for i in range(0,len(data)):
        pygame.draw.rect(screen,(WHITE),(i*(WIDTH/int(l)),HEIGHT-data[i], WIDTH/int(l), data[i]))
    pygame.display.update()
    
def sort(data, sort = 'bubble'):

##  #bubblesort
    if sort == 'bubble':
        for i in range(0,len(data)-1):
            if data[i] > data[i+1]:
                store = data[i]
                data[i] = data[i+1]
                data[i+1] = store
        make_display(data)
            

##  #selection sort
    elif sort == 'selection':
        for i in range(0,len(data)):
            minVal = i
            for j in range(i+1, len(data)):
                if data[j]>data[minVal]:
                    minVal = j
            x = data[minVal]
            data[minVal] = data[i]
            data[i] = x
            
def Sorted(data):
    for i in range(len(data)-1):
        if data[i] > data[i+1]:
            return False
    return True


while(True):
    data = []
    l=input("Data size: ")
    #l = 255
    r=int(len(data)/2)
    data_set(int(l))
    gap = int(len(data))
    while not Sorted(data[::-1]):
        screen.fill(BLACK)
        sort(data)
        time.sleep(.01)
    print(data)
