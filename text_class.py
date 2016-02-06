import pygame, sys
import random, math
pygame.init()

DISPLAY_WIDTH = 1300
DISPLAY_HEIGHT = 700

PROGRAM_DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))



class Text:
    def __init__(self, text, text_color, font, size, loc, scr_background_type, scr_background_img, scr_background_color):
        self._text = text
        self._text_color = text_color
        self._font = font
        self._size = size
        self._config = pygame.font.Font(self._font, self._size)
        self._loc = loc
        self._surface = self._config.render(self._text, True, self._text_color)
        self._rect = self._surface.get_rect()
        self._rect.center = self._loc
        self._width = self._rect[2]
        self._height = self._rect[3]

        self._scr_background_type = scr_background_type
        self._scr_background_img = scr_background_img
        self._scr_background_color = scr_background_color


    def draw(self):
        PROGRAM_DISPLAY.blit(self._surface, self._rect)


    def change_loc(self, x_change, y_change):
        self.cover_up()
        self._loc[0] += x_change
        self._loc[1] += y_change
        self._rect.center = self._loc
        self.draw()


    def change_size(self, change):
        self.cover_up()
        self._size += change
        self._config = pygame.font.Font(self._font, self._size)
        self._surface = self._config.render(self._text, True, self._text_color)
        self._rect = self._surface.get_rect()
        self._rect.center = self._loc
        self.draw()


    def cover_up(self):
        topleft = center_to_topleft(self._loc, self._rect[2], self._rect[3])
        cover_up(self._scr_background_type, topleft[0], topleft[1], self._rect[2], self._rect[3], self._scr_background_img, self._scr_background_color)


    def get_width(self):
        return self._width


    def get_height(self):
        return self._height


    def get_loc(self):
        return self._loc


    def get_size(self):
        return self._size


