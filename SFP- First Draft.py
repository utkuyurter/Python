"""
SFP- SAT Fun Prep
First draft of the program.
"""

import pygame , sys
from pygame.locals import *

pygame.init()

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600

PROGRAM_DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("SAT Fun Prep")

#COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIME = (0, 255, 0)
PURPLE = (128, 0, 128)
TEAL = (0, 128, 128)
YELLOW = (255, 255, 0)


BUTTON_TEXT = pygame.font.Font("freesansbold.ttf", 20)


class Screen:
    def __init__(self):
        self._on = False
        self._button_dict = {}
        self._img_dict = {}
        
    def draw_button(self, button_name, x_coord, y_coord, button_width, button_height, color1, color2, text, text_color):
        if self._on:
            self._button_dict[button_name] = (x_coord, y_coord, button_width, button_height)
            mouse_pos = pygame.mouse.get_pos()
            if x_coord < mouse_pos[0] < x_coord + button_width and y_coord < mouse_pos[1] < y_coord + button_height:
                pygame.draw.rect(PROGRAM_DISPLAY, color2, [x_coord, y_coord, button_width, button_height])
            else:
                pygame.draw.rect(PROGRAM_DISPLAY, color1, [x_coord, y_coord, button_width, button_height])
            button_text_surface = BUTTON_TEXT.render(text, True, text_color)
            button_text_rect = button_text_surface.get_rect()
            button_text_rect.center = (x_coord + (button_width / 2), y_coord + (button_height / 2))
            PROGRAM_DISPLAY.blit(button_text_surface, button_text_rect)

    def draw_image(self, img, img_name, x_coord, y_coord):
        pass

    def set_on():
        self._on = True


    def set_off():
        self._on = False
        

    def set_background(background):
        if type(background) == pygame.Surface:
            img = background
            PROGRAM_DISPLAY.blit(img, (0, 0))
        else:
            color = background
            PROGRAM_DISPLAY.fill(color)

    def get_buttons():
        return self._button_dict

    def get_images():
        return self._img_dict








#This is the game loop!
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()










            
