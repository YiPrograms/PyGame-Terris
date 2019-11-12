
import pygame

import random
from random import randint
import time
random.seed(time.time())

from copy import deepcopy

NOT_RUNNING = 0
FALLING = 1
DROPPED = 2
GAME_OVER = 3

ROW_BUFFER = 22
ROW = 20
COL = 10
EMPTY_ROW = [0 for i in range(10)]

COLOR = [None, (251, 86, 90), (114, 55, 197), (45, 133, 222), (28, 196, 171), (241, 220, 27)]

FLIP = [1, 0, 0, 0, 0, 0, 0]
TYPE = [[[0, 0, 0, 0],
         [1, 1, 1, 1],
         [0, 0, 0, 0],
         [0, 0, 0, 0]],

        [[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]],
         
        [[1, 1, 0],
         [0, 1, 0],
         [0, 1, 0]],
         
        [[0, 1, 0],
         [0, 1, 0],
         [1, 1, 0]],
         
        [[1, 0, 0],
         [1, 1, 0],
         [0, 1, 0]],
         
        [[0, 0, 1],
         [0, 1, 1],
         [0, 1, 0]],

        [[1, 1],
         [1, 1]]]

class Tetris:
    score = 0
    state = NOT_RUNNING
    table = []
    block = []
    bx = -1
    by = -1
    bsize = 0
    btype = -1
    def __init__(self, size, pos, title, screen):
        self.width = size[0]
        self.height = size[1]
        self.x = pos[0]
        self.y = pos[1]
        self.title = title
        self.screen = screen
        self.drow = self.height/ROW
        self.dcol = self.width/COL
        self.yy = self.y + self.height - self.drow
        
        for i in range(ROW_BUFFER):
            self.table.append(EMPTY_ROW[:])

        self.new_block(randint(0, 6), randint(1, 5))
        self.draw()
    
    def draw(self):
        pygame.draw.rect(self.screen, (67, 95, 120), pygame.Rect(self.x, self.y, self.width, self.height))

        for i in range(ROW):
            for j in range(COL):
                if self.table[i][j] != 0:
                    pygame.draw.rect(self.screen,
                                    COLOR[self.table[i][j]],
                                    pygame.Rect(self.x+self.dcol*j, self.yy-self.drow*i, self.dcol, self.drow))
                elif self.bx-self.bsize<=i and i<self.bx and self.by<=j and j<self.by+self.bsize:
                    if self.block[i-(self.bx-self.bsize)][j-self.by] != 0:
                        pygame.draw.rect(self.screen,
                                    COLOR[self.block[i-(self.bx-self.bsize)][j-self.by]],
                                    pygame.Rect(self.x+self.dcol*j, self.yy-self.drow*i, self.dcol, self.drow))

        for i in range(1, ROW):
            y = self.y+self.drow*i
            pygame.draw.line(self.screen, (197, 227, 236), (self.x, y), (self.x+self.width, y), 1)
        for i in range(1, COL):
            x = self.x+self.dcol*i
            pygame.draw.line(self.screen, (197, 227, 236), (x, self.y), (x, self.y+self.height), 1)
        pygame.draw.rect(self.screen, (197, 227, 236), pygame.Rect(self.x-2, self.y-2, self.width+4, self.height+4), 4)

        pygame.display.flip()

    def new_block(self, typ, color_id):
        self.bsize = len(TYPE[typ])
        self.btype = typ
        self.bx = ROW
        self.by = randint(0, COL-1-self.bsize)
        self.block = deepcopy(TYPE[typ])
        for i in range(self.bsize):
            for j in range(self.bsize):
                if self.block[i][j] == 1:
                    self.block[i][j] = color_id
        
        for i in range(randint(0, 3)):
            self.turn()
        
        self.state = FALLING
    
    def turn(self):
        new_block = deepcopy(self.block)

        if FLIP[self.btype]:
            for i in range(self.bsize):
                for j in range(self.bsize):
                    new_block[i][j] = self.block[j][i]
        else:
            for i in range(self.bsize):
                for j in range(self.bsize):
                    new_block[i][j] = self.block[j][self.bsize-i-1]
        
        self.block = new_block


    
       
