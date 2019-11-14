#!/bin/usr/env python

import sys

import pygame
pygame.init()

from tetris import Tetris 

NOT_RUNNING = 0
FALLING = 1
DROPPED = 2
GAME_OVER = 3



def main():
    screen = pygame.display.set_mode((1280, 960))
    pygame.display.set_caption("Tetris")
    screen.fill((26, 50, 88))

    FALL_EVENT, FALL_TIME = pygame.USEREVENT+1, 700
    HOLD_EVENT, HOLD_TIME = pygame.USEREVENT+2, 70
    pygame.time.set_timer(FALL_EVENT, FALL_TIME)
    pygame.time.set_timer(HOLD_EVENT, HOLD_TIME)
    
    def new_game():
        return Tetris((400, 800), (60, 75), "Player", screen)

    player = new_game()

    clock = pygame.time.Clock()
    FPS = 60
    running = True

    hold = {pygame.K_DOWN: 0, pygame.K_LEFT: 0, pygame.K_RIGHT: 0}

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if player.state == FALLING:
                if event.type == HOLD_EVENT:
                    for k, v in hold.items():
                        if v>0:
                            if hold[k] >= 7:
                                if k == pygame.K_DOWN:
                                    player.fall()
                                elif k == pygame.K_RIGHT:
                                    player.move(1)
                                elif k == pygame.K_LEFT:
                                    player.move(-1)
                            else:
                                hold[k] += 1

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        player.fall()
                    elif event.key == pygame.K_RIGHT:
                        player.move(1)
                    elif event.key == pygame.K_LEFT:
                        player.move(-1)
                    elif event.key == pygame.K_UP:
                        player.turn()
                    elif event.key == pygame.K_SPACE:
                        player.drop()
                    if event.key in hold.keys():
                        hold[event.key] += 1
                 
                if event.type == pygame.KEYUP:
                    if event.key in hold.keys():
                        hold[event.key] = 0
                
                if event.type == FALL_EVENT:
                    player.fall()

            else:
                if event.type == pygame.KEYDOWN:
                    del player
                    player = new_game()
                    


if __name__ == "__main__":
    while True:
        running = True
        main()
