#!/bin/usr/env python

import sys

import pygame
pygame.init()

from tetris import Tetris 



def main():
    screen = pygame.display.set_mode((1280, 960))
    pygame.display.set_caption("Tetris")
    screen.fill((26, 50, 88))

    FALL_EVENT, FALL_TIME = pygame.USEREVENT+1, 700
    HOLD_EVENT, HOLD_TIME = pygame.USEREVENT+2, 200
    pygame.time.set_timer(FALL_EVENT, FALL_TIME)
    pygame.time.set_timer(HOLD_EVENT, HOLD_TIME)

    player = Tetris((400, 800), (60, 75), "Player", screen)

    clock = pygame.time.Clock()
    FPS = 60
    running = True

    last_key = None

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN or event.type == HOLD_EVENT:
                if event.type == pygame.KEYDOWN:
                    last_key = event.key
                elif last_key is None:
                    pass
                    
                if last_key == pygame.K_DOWN:
                    player.fall()
                elif last_key == pygame.K_RIGHT:
                    player.move(1)
                elif last_key == pygame.K_LEFT:
                    player.move(-1)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.turn()

            if event.type == pygame.KEYUP:
                last_key = None
            
            if event.type == FALL_EVENT:
                player.fall()

                    


if __name__ == "__main__":
    while True:
        running = True
        main()
