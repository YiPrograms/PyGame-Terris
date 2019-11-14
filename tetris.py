
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
    def __init__(self, size, pos, title, screen):
        self.table = []
        self.block_list = []
        self.state = NOT_RUNNING
        self.score = 0
        self.combo = 0
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

        self.draw_title()
        self.add_score(0)
        self.new_block(True)
        self.draw()
    
    def __del__(self):
        del self
    
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
    
    def draw_title(self):
        if self.title is not None:
            font = pygame.font.SysFont(None, 72)
            text = font.render(self.title, True, (197, 227, 236))
            self.screen.blit(text, (self.x+(self.width-text.get_width())/2, self.y-text.get_height()-10))

    def draw_next(self):
        if self.title is None:
            width = self.dcol*4 + 25*2
            height = self.drow*4*3 + 25*4
            x = self.x + self.width + 50
            y = self.y + 50
            pygame.draw.rect(self.screen, (67, 95, 120), pygame.Rect(self.x+self.width+25, self.y+25, width, height))
            for k in range(3):
                offset = 0
                if self.block_list[k].size == 3:
                    offset = self.drow /2
                elif self.block_list[k].size == 2:
                    offset = self.drow
                for i in range(self.block_list[k].size):
                    for j in range(self.block_list[k].size):
                        if self.block_list[k].block[i][j] != 0:
                            pygame.draw.rect(self.screen,
                                    COLOR[self.block_list[k].block[i][j]],
                                    pygame.Rect(offset + x+self.dcol*j+1, offset + y+self.drow*(self.block_list[k].size-i-1)+1, self.dcol-2, self.drow-2))
                y += self.drow*4 + 25

    def new_block(self, init):
        if init:
            for i in range(3):
                self.block_list.append(Block(randint(0, 6), randint(1, len(COLOR)-1)))
        self.block = self.block_list[0]
        self.block_list.pop(0)
        self.block_list.append(Block(randint(0, 6), randint(1, len(COLOR)-1)))
        self.block.setpos((ROW_BUFFER-self.block.size, randint(0, COL-1-self.block.size)))
        self.state = FALLING
        self.draw_next()
        self.draw()
    
    def fall(self):
        pos = self.block.fall()
        if self.check(self.block.block, pos):
            self.block.setpos(pos)
            self.draw()
        else:
            self.hit()
        
    
    def drop(self):
        x, y = self.block.getpos()
        if not self.check(self.block.block, (x, y)):
            pass

        while self.check(self.block.block, (x-1, y)):
            x -= 1

        self.block.setpos((x, y))
        self.hit()

    def move(self, dir):
        pos = self.block.move(dir)
        if self.check(self.block.block, pos):
            self.block.setpos(pos)
            self.draw()
    
    def turn(self):
        block = self.block.turn()
        x, y = self.block.getpos()
        success = False
        if self.check(block, (x, y)):
            success = True
        elif self.block.size > 2:
            ycan = [y+1, y-1]
            if self.block.size == 4:
                ycan.append(y-2)
            for yx in ycan:
                if self.check(block, (x, yx)):
                    y = yx
                    success = True
        
        if success:
            self.block.setpos((x, y))
            self.block.block = block
            self.draw()

    def check(self, block, pos):
        x, y = pos
        size = len(block)

        for i in range(size):
            for j in range(size):
                if block[i][j] != 0:
                    if not (x+i>=0 and y+j>=0 and y+j<COL and self.table[x+i][y+j] == 0):
                        return False
        
        return True

    def game_over(self):
        self.state = GAME_OVER
        s = pygame.Surface((self.width, self.height))
        s.set_alpha(172)
        s.fill((59, 82, 78))
        self.screen.blit(s, (self.x, self.y))

        font = pygame.font.SysFont(None, 72)
        text = font.render("Game Over", True, (197, 227, 236))
        self.screen.blit(text, (self.x+(self.width-text.get_width())/2, self.y+(self.height-text.get_height())/2))

        pygame.display.flip()

    def add_score(self, score):
        if self.title is None:
            self.score += score * self.combo
            font = pygame.font.SysFont(None, 72)
            text = font.render(str(self.score), True, (197, 227, 236))
            self.screen.blit(text, (self.x+(self.width-text.get_width())/2, self.y-text.get_height()-10))
    
    def hit(self):
        for i in range(self.block.size):
            for j in range(self.block.size):
                if self.block.block[i][j] != 0:
                    self.table[self.block.x+i][self.block.y+j] = self.block.block[i][j]
        
        i = 0
        clear = 0
        while i<ROW:
            if 0 not in self.table[i]:
                self.table.pop(i)
                self.table.append(EMPTY_ROW[:])
                i -= 1
                clear += 1
            i += 1
        
        if clear:
            self.combo += 1
            self.add_score(clear*200-100)
        else:
            self.combo = 0

        self.draw()

        for i in range(ROW, ROW_BUFFER):
            for j in range(COL):
                if self.table[i][j] != 0:
                    self.game_over()
                    return None

        self.state = DROPPED
        self.new_block(False)




    

    


    
       
