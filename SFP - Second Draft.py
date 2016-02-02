"""
SFP- SAT Fun Prep
Second draft of the program.
"""

import pygame, sys

pygame.init()

DISPLAY_WIDTH = 1300
DISPLAY_HEIGHT = 700

PROGRAM_DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("SAT FUN PREP")

#COLORS
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

# Width and height of main buttons (like Intro, Math, etc.). SCR1 means screen no. 1
SCR1_MENU_W = 200
SCR1_MENU_H = 75

# Width and height of sub-buttons.
SCR1_SUBMENU_W = 175
SCR1_SUBMENU_H = 60

# Text configurations. One for title, one for main buttons, one for sub-buttons
SCR1_TITLE_TEXT = pygame.font.Font("cour.ttf", 120)
SCR1_MENU_TEXT = pygame.font.Font("cour.ttf", 40)
SCR1_SUBMENU_TEXT = pygame.font.Font("cour.ttf", 20)

def cover_up(background_type, x_coord, y_coord, width, height, background_img = None, background_color = None):
    """
    Function that 'erases' a part of the display before a new button is drawn.
    """
    if background_type == "Image":
        PROGRAM_DISPLAY.blit(background_img, (x_coord, y_coord), (x_coord, y_coord, width, height))
    else:
        PROGRAM_DISPLAY.fill(background_color, (x_coord, y_coord, width, height))




class Button:
    # in addition to the methods below, we will add get methods (like get_buttons in the Screen class)
    def __init__(self, button_name, x_coord, y_coord, button_width, button_height, color1, color2, text, text_color, text_config):
        # make sure u add paramters to this function.
        """
        This should create a button object. It should keep track of
        properties of the button like width, location, etc., because this is what makes this
        class useful. After I thought about it, I decided that the initializer shouldn't draw
        the button immediately like in the draw_button method of the Screen class. Instead, it should
        record data of the button like its name, width, height, text on it, config of text on it, and
        everything else that was a paramter in the draw_button function. There will be another method
        to draw the button.
        """
        pass


    def draw():
        """
        This draws the button on the screen using the data recorded in fields. A field is like
        self._background_img for example. It stores data that u use.
        """
        pass


    def move():
        # u may leave this. We may not even need it. Or u can start implementing it.
        
        pass


    def disappear():
        # move() and disappear() are preliminary. We still will see how and whether we will use them.
        
        pass





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
        self._button_dict = {}
        self._img_dict = {}
        self._text_dict = {}
        self._background_type = None
        self._background_img = None
        self._background_color = None
        

    def draw_button(self, button_name, x_coord, y_coord, button_width, button_height, color1, color2, text, text_color, text_config):
        """
        This logic should be in the Button class's initializer, where a button is created. What this function does is
        to create an instance of the Button class, thus creating a button. The function also records
        the button's data in the button dictionary.
        """
        if self._on and self._background_type:
            self._button_dict[button_name] = (x_coord, y_coord, button_width, button_height)
            mouse_pos = pygame.mouse.get_pos()
            if x_coord < mouse_pos[0] < x_coord + button_width and y_coord < mouse_pos[1] < y_coord + button_height:
                cover_up(self._background_type, x_coord, y_coord, button_width, button_height, self._background_img, self._background_color)
                pygame.draw.rect(PROGRAM_DISPLAY, color2, (x_coord, y_coord, button_width, button_height))
            else:
                cover_up(self._background_type, x_coord, y_coord, button_width, button_height, self._background_img, self._background_color)
                pygame.draw.rect(PROGRAM_DISPLAY, color1, (x_coord, y_coord, button_width, button_height))
            button_text_surface = text_config.render(text, True, text_color)
            button_text_rect = button_text_surface.get_rect()
            button_text_rect.center = (x_coord + (button_width / 2), y_coord + (button_height / 2))
            PROGRAM_DISPLAY.blit(button_text_surface, button_text_rect)


    def draw_image(self, img, img_name, x_coord, y_coord, img_width = None, img_height = None):
        """
        We will most probabaly create an image class too, but not for now. We will first make sure we need it.
        """
        if self._on:
            if img_width and img_height:
                image = pygame.transform.scale(img, (img_width, img_height))
                PROGRAM_DISPLAY.blit(image, (x_coord, y_coord))
            elif not img_width and not img_height:
                PROGRAM_DISPLAY.blit(img, (x_coord, y_coord))
                img_width, img_height = img.get_rect()[2], img.get_rect()[3]
            self._img_dict[img_name] = (x_coord, y_coord, img_width, img_height)
                

    def draw_text(self, text, text_label, color, x_coord, y_coord, text_config):
        """
        Same as with draw_image.
        """
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
        self._button_dict = {}
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
        return self._button_dict
    
    
    def get_images(self):
        return self._img_dict


    def get_texts(self):
        return self._text_dict
    

    def get_background_type(self):
        return self._background_type


    def is_running(self):
        return self._on

    

###########################################
INTRO_SCREEN = Screen()
background = pygame.image.load('background3.jpg')


def intro_screen_loop():
    INTRO_SCREEN.set_on()
    INTRO_SCREEN.set_background(background)
    INTRO_SCREEN.draw_text("SAT FUN PREP", "Title", BLACK, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.15, SCR1_TITLE_TEXT)
    while INTRO_SCREEN.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        INTRO_SCREEN.draw_button("Intro", 50, 250, SCR1_MENU_W, SCR1_MENU_H, GREEN, LIGHT_GREEN, "Intro", BLACK, SCR1_MENU_TEXT)
        INTRO_SCREEN.draw_button("Math", 300, 250, SCR1_MENU_W, SCR1_MENU_H, GREEN, LIGHT_GREEN, "Math", BLACK, SCR1_MENU_TEXT)
        INTRO_SCREEN.draw_button("Reading", 550, 250, SCR1_MENU_W, SCR1_MENU_H, GREEN, LIGHT_GREEN, "Reading", BLACK, SCR1_MENU_TEXT)
        INTRO_SCREEN.draw_button("Writing", 800, 250, SCR1_MENU_W, SCR1_MENU_H, GREEN, LIGHT_GREEN, "Writing", BLACK, SCR1_MENU_TEXT)
        INTRO_SCREEN.draw_button("Random", 1050, 250, SCR1_MENU_W, SCR1_MENU_H, GREEN, LIGHT_GREEN, "Random", BLACK, SCR1_MENU_TEXT)

        INTRO_SCREEN.draw_button("Math- Reference", 325, 340, SCR1_SUBMENU_W, SCR1_SUBMENU_H, LIGHT_BLUE, AQUA, "Reference", BLACK, SCR1_SUBMENU_TEXT)
        INTRO_SCREEN.draw_button("Reading- Vocab", 575, 340, SCR1_SUBMENU_W, SCR1_SUBMENU_H, LIGHT_BLUE, AQUA, "Vocabulary", BLACK, SCR1_SUBMENU_TEXT)
        INTRO_SCREEN.draw_button("Writing- Grammar", 825, 340, SCR1_SUBMENU_W, SCR1_SUBMENU_H, LIGHT_BLUE, AQUA, "Grammar", BLACK, SCR1_SUBMENU_TEXT)
        INTRO_SCREEN.draw_button("Math- Practice", 325, 540, SCR1_SUBMENU_W, SCR1_SUBMENU_H, LIGHT_BLUE, AQUA, "Practice", BLACK, SCR1_SUBMENU_TEXT)        

        
        pygame.display.update()


intro_screen_loop()






            
