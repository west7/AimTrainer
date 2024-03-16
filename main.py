import pygame
import math
import random
import time

pygame.init()

WIDTH, HEIGHT = 1200, 800

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

class Target:
    MAX_SIZE = 50
    GROWTH_RATE = 0.2
    COLOR = "red"

    def __init__(self, x, y):
        self.x = x 
        self.y = y
        self.size = 0
        self.grow = True

    def update(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE
        



def main():
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

    pygame.quit()

if __name__ == "__main__":
    main()