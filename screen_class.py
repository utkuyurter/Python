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






class Screen:
    """
    A class for a screen in the program. Keeps track of the background image, images on the screen,
    buttons on the screen, and text on the screen.
    """
    def __init__(self):
        """
        Initialize everything. The screen is initialized as inactive (self._on is False).
        """
        self._on = False
        self._img_button_dict = {}
        self._img_dict = {}
        self._text_dict = {}
        self._background_type = None
        self._background_img = None
        self._background_color = None
        self._screen_number = None 

                    

    def draw_img_buttons(self, img_button, img_button_list = None):
        if self._on and self._background_type:
            if not img_button and img_button_list:
                for a_img_button in img_button_list:
                    if a_img_button.get_name() not in self._img_button_dict.keys():
                        self._img_button_dict[a_img_button.get_name()] = a_img_button.get_img_button_rect()
                    a_img_button.draw()


    def draw_image(self, img, img_name, x_coord, y_coord, img_width = None, img_height = None):
        if self._on:
            if img_width and img_height:
                image = pygame.transform.scale(img, (img_width, img_height))
                image_rect = image.get_rect()
                image_rect.center = (x_coord, y_coord)
                PROGRAM_DISPLAY.blit(image, image_rect)
            elif not img_width and not img_height:
                image_rect = image.get_rect()
                image_rect.center = (x_coord, y_coord)
                PROGRAM_DISPLAY.blit(img, image_rect)
                img_width, img_height = image_rect[2], image_rect[3]
            self._img_dict[img_name] = (x_coord, y_coord, img_width, img_height)
            
          
            
    def draw_text(self, text, text_label, color, x_coord, y_coord, text_config):
        if self._on:
            text_surface = text_config.render(text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.center = (x_coord, y_coord)
            PROGRAM_DISPLAY.blit(text_surface, text_rect)
            text_x, text_y = text_rect[0], text_rect[1]
            text_width, text_height = text_rect[2], text_rect[3]
            self._text_dict[text_label] = (text_x, text_y, text_width, text_height)
            
             
    def set_on(self):
        self._on = True
        

    def set_off(self):
        self._on = False
        PROGRAM_DISPLAY.fill(WHITE)
        self._img_button_dict = {}
        self._img_dict = {}
        self._text_dict = {}
        self._background_type = None
        self._background_img = None
        self._background_color = None

        
    def set_background(self, background):
        if self._on:
            if type(background) == pygame.Surface:
                img = pygame.transform.scale(background, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
                PROGRAM_DISPLAY.blit(img, (0, 0))
                self._background_type = "Image"
                self._background_img = img
                self._background_color = None
            else:
                color = background
                PROGRAM_DISPLAY.fill(color)
                self._background_type = "Color Fill"
                self._background_color = color
                self._background_img = None

            
    def get_buttons(self):
        return self._img_button_dict
    
    
    def get_images(self):
        return self._img_dict


    def get_texts(self):
        return self._text_dict
    

    def get_background_type(self):
        return self._background_type


    def get_background_img(self):
        return self._background_img


    def get_background_color(self):
        return self._background_color


    def is_running(self):
        return self._on

   










