import pygame, sys
import random, math

pygame.init()
DISPLAY_WIDTH = 1300
DISPLAY_HEIGHT = 700

PROGRAM_DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIME = (0, 255, 0)
PURPLE = (128, 0, 128)
TEAL = (0, 128, 128)
YELLOW = (255, 255, 0)
AQUA = (0, 255, 255)
SILVER = (192, 192, 192)
LIGHT_BLUE = (60, 60, 255)
LIGHT_GREEN = (0, 255, 0)
VIOLET = (250, 0, 250)




def cover_up(background_type, x_coord, y_coord, width, height, background_img = None, background_color = None):
    """
    Function that 'erases' a part of the display before a new button is drawn, or when a button is set off.
    """
    if background_type == "Image":
        PROGRAM_DISPLAY.blit(background_img, (x_coord, y_coord), (x_coord, y_coord, width, height))
    else:
        PROGRAM_DISPLAY.fill(background_color, (x_coord, y_coord, width, height))






class Image_Button:
    def __init__(self, img_button_name, img1, img2, img_x , img_y, img_width, img_height, background_type, background_img, background_color):
        self._on = False
        self.img_button_name = img_button_name
        self.img1 = img1
        self.img2 = img2
        self._x = img_x
        self._y = img_y
        self.img_width = img_width
        self.img_height = img_height
        self._scr_background_type = background_type
        self._scr_background_img = background_img
        self._scr_background_color = background_color
        self.animated = True

        self._init_img_width = img_width
        self._init_img_height = img_height
        self._init_x = img_x
        self._init_y = img_y



    def draw(self):
        if self._on:
            if self.is_hovered_on():
                cover_up(self._scr_background_type, self._x, self._y, self.img_width, self.img_height, self._scr_background_img, self._scr_background_color)
                _img_2 = pygame.transform.scale(self.img2, (self.img_width - 6, self.img_height - 6))
                PROGRAM_DISPLAY.blit(_img_2, (self._x + 3, self._y + 3))
            else:
                cover_up(self._scr_background_type, self._x, self._y, self.img_width, self.img_height, self._scr_background_img, self._scr_background_color)
                _img_1 = pygame.transform.scale(self.img1, (self.img_width, self.img_height))
                PROGRAM_DISPLAY.blit(_img_1, (self._x, self._y))
                
        
        
    def set_on(self, loc = None, width = None, height = None, colors = None, text = None, text_color = None, text_config = None):
        self._on = True
        if loc:
            self._x = loc[0]
            self._y = loc[1]
        else:
            self._x = self._init_x
            self._y = self._init_y
        if width:
            self.img_width = width
        else:
            self.img_width = self._init_img_width
        if height:
            self.img_height = height
        else:
            self.img_height = self._init_img_height


    def is_on(self):
        return self._on
             
        
        
    def set_off(self):
        self._on = False
        cover_up(self._scr_background_type, self._x, self._y, self.img_width, self.img_height, self._scr_background_img, self._scr_background_color)



    def is_hovered_on(self):
        if self._on and self.animated:
            mouse_pos = pygame.mouse.get_pos()
            return self._x < mouse_pos[0] < self._x + self.img_width and self._y < mouse_pos[1] < self._y + self.img_height


    def unanimated(self):
        if self._on:
            self.animated = False
            return self.animated
        


    def is_pressed(self):
        if self._on:
            mouse_click = pygame.mouse.get_pressed()
            if self.is_hovered_on():
                return mouse_click[0] == 1


    def change_x(self, change):
        if self._on:
            self._x += change


    def change_y(self, change):
        if self._on:
            self._y += change


    def change_width(self, change):
        if self._on:
            self.img_width += change


    def change_height(self, change):
        if self._on :
            self.img_height += change


    def get_img_button_rect(self):
        return (self._x, self._y, self.img_width, self.img_height)


    def get_loc(self):
        return (self._x, self._y)


    def get_width(self):
        return self.img_width


    def get_height(self):
        return self.img_height



    def get_name(self):
        return self.img_button_name


    def get_init_vals(self):
        return {"init x": self._init_x,
                "init y": self._init_y,
                "init width": self._init_img_width,
                "init height": self._init_img_height}


    def get_scr_background_type(self):
        return self._scr_background_type


    def get_scr_background_img(self):
        return self._scr_background_img


    def get_scr_background_color(self):
        return self._scr_background_color













