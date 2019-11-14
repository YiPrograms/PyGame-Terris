
import random
from random import randint
import time
random.seed(time.time())

from copy import deepcopy

FLIP = [1, 0, 0, 0, 1, 1, 1]
TYPE = [[[0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0],
         [0, 1, 0, 0]],

        [[0, 1, 0],
         [1, 1, 1],
         [0, 0, 0]],
         
        [[1, 1, 0],
         [0, 1, 0],
         [0, 1, 0]],
         
        [[0, 1, 0],
         [0, 1, 0],
         [1, 1, 0]],
         
        [[0, 1, 0],
         [0, 1, 1],
         [0, 0, 1]],
         
        [[0, 1, 0],
         [1, 1, 0],
         [1, 0, 0]],

        [[1, 1],
         [1, 1]]]

class Block:
    def __init__(self, typ, color):
        self.size = len(TYPE[typ])
        self.typ = typ
        self.x = -1
        self.y = -1
        self.block = deepcopy(TYPE[typ])
        self.ori = False
        for i in range(self.size):
            for j in range(self.size):
                if self.block[i][j] == 1:
                    self.block[i][j] = color
        
        for i in range(randint(0, 3)):
            self.block = self.turn()

    def turn(self):
        new_block = deepcopy(self.block)

        if FLIP[self.typ] and self.ori:
            self.ori = False
            for i in range(self.size):
                for j in range(self.size):
                    new_block[i][j] = self.block[self.size-j-1][i]
        else:
            self.ori = True
            for i in range(self.size):
                for j in range(self.size):
                    new_block[i][j] = self.block[j][self.size-i-1]
        
        return new_block
    
    def fall(self):
        return (self.x-1, self.y)

    def move(self, dir):
        return (self.x, self.y+dir)
    
    def getpos(self):
        return self.x, self.y
    
    def setpos(self, pos):
        self.x, self.y = pos
    

