
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

ROW_BUFFER = 23
ROW = 20
COL = 10
EMPTY_ROW = [0 for i in range(10)]

COLOR = [None, (251, 86, 90), (114, 55, 197), (45, 133, 222), (28, 196, 171), (241, 220, 27)]

from block import Block

class Tetris:
    score = 0
    state = NOT_RUNNING
    table = []
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

        self.new_block()
        self.draw()
    
    def draw(self):
        pygame.draw.rect(self.screen, (67, 95, 120), pygame.Rect(self.x, self.y, self.width, self.height))

        for i in range(ROW):
            for j in range(COL):
                if self.table[i][j] != 0:
                    pygame.draw.rect(self.screen,
                                    COLOR[self.table[i][j]],
                                    pygame.Rect(self.x+self.dcol*j, self.yy-self.drow*i, self.dcol, self.drow))
                elif self.block.x<=i and i<self.block.x+self.block.size and \
                     self.block.y<=j and j<self.block.y+self.block.size:
                    if self.block.block[i-self.block.x][j-self.block.y] != 0:
                        pygame.draw.rect(self.screen,
                                    COLOR[self.block.block[i-self.block.x][j-self.block.y]],
                                    pygame.Rect(self.x+self.dcol*j, self.yy-self.drow*i, self.dcol, self.drow))

        for i in range(1, ROW):
            y = self.y+self.drow*i
            pygame.draw.line(self.screen, (197, 227, 236), (self.x, y), (self.x+self.width, y), 1)
        for i in range(1, COL):
            x = self.x+self.dcol*i
            pygame.draw.line(self.screen, (197, 227, 236), (x, self.y), (x, self.y+self.height), 1)
        pygame.draw.rect(self.screen, (197, 227, 236), pygame.Rect(self.x-2, self.y-2, self.width+4, self.height+4), 4)

        pygame.display.flip()

    def new_block(self):
        self.block = Block(randint(0, 6), randint(1, len(COLOR)-1), (ROW_BUFFER, COL))
        self.state = FALLING
        self.draw()
    
    def fall(self):
        pos = self.block.fall()
        if self.check(self.block.block, pos):
            self.block.x, self.block.y = pos
        else:
            self.hit()
        self.draw()

    def move(self, dir):
        pos = self.block.move(dir)
        if self.check(self.block.block, pos):
            self.block.x, self.block.y = pos
            self.draw()
    
    def turn(self):
        block = self.block.turn()
        if self.check(block, (self.block.x, self.block.y)):
            self.block.block = block
            self.draw()

    def check(self, block, pos):
        print(pos)
        x, y = pos
        size = len(block)

        for i in range(size):
            for j in range(size):
                if block[i][j] != 0:
                    if not (x+i>=0 and y+j>=0 and y+j<COL and self.table[x+i][y+j] == 0):
                        return False
        
        return True

    def hit(self):
        for i in range(self.block.size):
            for j in range(self.block.size):
                if self.block.block[i][j] != 0:
                    self.table[self.block.x+i][self.block.y+j] = self.block.block[i][j]
        
        i = 0
        while i<ROW:
            if 0 not in self.table[i]:
                self.table.pop(i)
                self.table.append(EMPTY_ROW[:])
                i -= 1
            i += 1
        self.draw()

        for i in range(ROW, ROW_BUFFER):
            for j in range(COL):
                if self.table[i][j] != 0:
                    return GAME_OVER

        state = DROPPED
        self.new_block()




    

    


    
       
