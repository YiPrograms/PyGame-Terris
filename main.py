#!/bin/usr/env python

import sys

import pygame
pygame.init()

from tetris import Tetris 



def main():
    screen = pygame.display.set_mode((1280, 960))
    pygame.display.set_caption("Tetris")
    screen.fill((26, 50, 88))

    player = Tetris((400, 800), (60, 75), "Player", screen)

    clock = pygame.time.Clock()
    FPS = 60
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player.bx -= 1
                elif event.key == pygame.K_RIGHT:
                    player.by += 1
                elif event.key == pygame.K_LEFT:
                    player.by -= 1 
                elif event.key == pygame.K_UP:
                    player.turn()
                player.draw()
                    


if __name__ == "__main__":
    while True:
        running = True
        main()
