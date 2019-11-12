#!/bin/usr/env python

import sys
import pygame
from pygame.locals import QUIT

NOT_RUNNING = 0
FALLING = 1
DROPPED = 2
GAME_OVER = 3

class Terris(pygame.sprite.Sprite):
    row = 20
    dead_row = 18
    col = 10
    score = 0
    state = NOT_RUNNING
    table = []
    def __init__(self, size=(300, 500) , location=(50, 50) , name="Player"):
        super().__init__()
        self.size = size
        self.location = location
        self.name = name

        for i in range(self.row):
            init_row = [0 for j in range(self.col)]
            self.table.append(init_row)
        
        self.draw()

    def draw(self):
        print(self.table)

    def fall(self):
        if self.state != FALLING:
            pass

    def drop(self):
        if self.state != FALLING:
            pass
        while self.state == FALLING:
            self.fall()

    def count(self):

    
    def new_block(self, type):
        



def run():
    pygame.init()
    window_surface = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Hello World:)')
    window_surface.fill((255, 255, 255))

    head_font = pygame.font.SysFont(None, 60)
    text_surface = head_font.render('Hello World!', True, (0, 0, 0))
    window_surface.blit(text_surface, (10, 10))

    pygame.display.update()

    terris = Terris()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


run()