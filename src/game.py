import pygame

from const import *

class Game:
    def __init__(self):
        pass

    #Show methods
    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200) # Light square color
                else:
                    color = (119, 154, 88) # Dark square color

                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                
                pygame.draw.rect(surface, color, rect)