"""
SFP- SAT Fun Prep
Third draft of the program.
"""

import pygame, sys
import math

pygame.init()

DISPLAY_WIDTH = 1300
DISPLAY_HEIGHT = 700

PROGRAM_DISPLAY = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("SAT Fun Prep")

CLOCK = pygame.time.Clock()

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

# Dictionary that maps button configurations to a tuple containing their data,
# so that they can be accessed individually not only as a whole Font object
TEXT_CONFIG_DICT = {SCR1_TITLE_TEXT: ("cour.ttf", 120),
                    SCR1_MENU_TEXT: ("cour.ttf", 40),
                    SCR1_SUBMENU_TEXT: ("cour.ttf", 20)}



def cover_up(background_type, x_coord, y_coord, width, height, background_img = None, background_color = None):
    """
    Function that 'erases' a part of the display before a new button is drawn, or when a button is set off.
    """
    if background_type == "Image":
        PROGRAM_DISPLAY.blit(background_img, (x_coord, y_coord), (x_coord, y_coord, width, height))
    else:
        PROGRAM_DISPLAY.fill(background_color, (x_coord, y_coord, width, height))


def distance_formula(x, y):
    return math.sqrt((x ** 2) + (y ** 2))


def move(thing, type_speed, covered, target_dist):
    if covered < target_dist:
        if type_speed[0] == "Up" or type_speed[0] == "Down":
            old_x = thing.get_loc()[0]
            old_y = thing.get_loc()[1]
            cover_up(thing.get_scr_background_type(), old_x, old_y, thing.get_width(), thing.get_height(), thing.get_scr_background_img(),
                     thing.get_scr_background_color())
            thing.change_y(type_speed[1])
            covered += math.fabs(type_speed[1])
            return covered
        elif type_speed[0] == "Right" or type_speed[0] == "Left":
            old_x = thing.get_loc()[0]
            old_y = thing.get_loc()[1]
            cover_up(thing.get_scr_background_type(), old_x, old_y, thing.get_width(), thing.get_height(), thing.get_scr_background_img(),
                     thing.get_scr_background_color())
            thing.change_x(type_speed[1])
            covered += math.fabs(type_speed[1])
            return covered
        else:
            old_x = thing.get_loc()[0]
            old_y = thing.get_loc()[1]
            cover_up(thing.get_scr_background_type(), old_x, old_y, thing.get_width(), thing.get_height(), thing.get_scr_background_img(),
                     thing.get_scr_background_color())
            thing.change_x(type_speed[1][0])
            thing.change_y(type_speed[1][1])
            covered += math.fabs(distance_formula(type_speed[1][0], type_speed[1][1]))
            return covered
    return True


def shrink_disappear(thing, speed, done, target):
    accomplished = False
    cover_up(thing.get_scr_background_type(), thing.get_loc()[0], thing.get_loc()[1], thing.get_width(), thing.get_height(), thing.get_scr_background_img(),
             thing.get_scr_background_color())
    thing.erase_text()
    thing.change_x(speed[0])
    thing.change_y(speed[0])
    thing.change_width(-2 * speed[0])
    thing.change_height(-2 * speed[0])
    if thing.get_width() < 1 or thing.get_height() < 1:
        thing.set_off()
        accomplished = True
    return accomplished



def simult_animations(things_and_animations):
    while things_and_animations:
        for thing in things_and_animations.keys():
            data = things_and_animations[thing]
            covered = data[2](thing, [param for param in data[3 : -1]], data[0], data[1])
            thing.draw()
            if type(covered) == int or type(covered) == float:
                things_and_animations[thing][0] += covered
            else:
                if covered:
                    things_and_animations[thing][-1] = True
        for thing in things_and_animations.keys():
            if things_and_animations[thing][-1]:
                things_and_animations.pop(thing)
        pygame.display.update()
        CLOCK.tick(20)
            



class Button:
    def __init__(self, button_name, x_coord, y_coord, button_width, button_height, color1, color2, text, text_color, text_config,
                 background_type, background_img = None, background_color = None):
        self._on = False
        self._name = button_name
        self._x = x_coord
        self._y = y_coord
        self._width = button_width
        self._height = button_height
        self._color1 = color1
        self._color2 = color2
        self._text = text
        self._text_color = text_color
        self._text_config = text_config
        self._scr_background_type = background_type
        self._scr_background_img = background_img
        self._scr_background_color = background_color
        self._def_text_font = TEXT_CONFIG_DICT[text_config][0]
        self._def_text_size = TEXT_CONFIG_DICT[text_config][1]
        self._text_erased = False

        self._init_x = x_coord
        self._init_y = y_coord
        self._init_width = button_width
        self._init_height = button_height
        self._init_color1 = color1
        self._init_color2 = color2
        self._init_text = text
        self._init_text_color = text_color
        self._init_text_config = text_config


    def draw(self):
        if self._on:
            if self.is_hovered_on():
                cover_up(self._scr_background_type, self._x, self._y, self._width, self._height, self._scr_background_img, self._scr_background_color)
                pygame.draw.rect(PROGRAM_DISPLAY, self._color2, (self._x, self._y, self._width, self._height))
            else:
                cover_up(self._scr_background_type, self._x, self._y, self._width, self._height, self._scr_background_img, self._scr_background_color)
                pygame.draw.rect(PROGRAM_DISPLAY, self._color1, (self._x, self._y, self._width, self._height))
            if not self._text_erased:
                button_text_surface = self._text_config.render(self._text, True, self._text_color)
                button_text_rect = button_text_surface.get_rect()
                button_text_rect.center = (self._x + (self._width / 2), self._y + (self._height / 2))
                PROGRAM_DISPLAY.blit(button_text_surface, button_text_rect)                


    def move(self, movement, distance, speed = None):
        pass

    def shrink_disappear(self, speed):
        pass

    def fade_disappear(self):
        pass

    def enlarge_appear(self):
        pass

    def fade_appear(self):
        pass
    

    def change_x(self, change):
        if self._on:
            self._x += change


    def change_y(self, change):
        if self._on:
            self._y += change


    def change_width(self, change):
        if self._on:
            self._width += change


    def change_height(self, change):
        if self._on :
            self._height += change


    def change_text_config(self, font = None, size = None):
        if self._on:
            if font and size:
                self._text_config = pygame.font.Font(font, size)
            elif font:
                self._text_config = pygame.font.Font(font, self._def_text_size)
            elif size:
                self._text_config = pygame.font.Font(self._def_text_font, size)
            self.draw()


    def change_main_color(self, color):
        if self._on:
            self._color1 = color
            self.draw()


    def change_secondary_color(self, color):
        if self._on:
            self._color2 = color
            self.draw()


    def is_hovered_on(self):
        if self._on:
            mouse_pos = pygame.mouse.get_pos()
            return self._x < mouse_pos[0] < self._x + self._width and self._y < mouse_pos[1] < self._y + self._height


    def is_pressed(self):
        if self._on:
            mouse_click = pygame.mouse.get_pressed()
            if self.is_hovered_on():
                return mouse_click[0] == 1


    def erase_text(self):
        if self._on:
            self._text_erased = True
##            self.draw()


    def set_on(self):
        self._on = True


    def set_off(self):
        self._on = False
        cover_up(self._scr_background_type, self._x, self._y, self._width, self._height, self._scr_background_img, self._scr_background_color)
        self._x = self._init_x
        self._y = self._init_y
        self._width = self._init_width
        self._height = self._init_height
        self._color1 = self._init_color1
        self._color2 = self._init_color2
        self._text = self._init_text
        self._text_color = self._init_text_color
        self._text_config = self._init_text_config


    def is_on(self):
        return self._on


    def get_button_rect(self):
        if self._on:
            return (self._x, self._y, self._width, self._height)


    def get_name(self):
        if self._on:
            return self._name


    def get_colors(self):
        if self._on:
            return (self._color1, self._color2)


    def get_text_info(self):
        if self._on:
            return (self._text, self._text_config, self._text_color)


    def get_loc(self):
        if self._on:
            return (self._x, self._y)


    def get_width(self):
        if self._on:
            return self._width


    def get_height(self):
        if self._on:
            return self._height


    def get_scr_background_type(self):
        if self._on:
            return self._scr_background_type


    def get_scr_background_img(self):
        if self._on:
            return self._scr_background_img


    def get_scr_background_color(self):
        if self._on:
            return self._scr_background_color
            
                



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
        

    def draw_buttons(self, button, button_list = None):
        if self._on and self._background_type:
            if not button and button_list:
                for a_button in button_list:
                    if a_button.get_name() not in self._button_dict.keys():
                        self._button_dict[a_button.get_name()] = a_button.get_button_rect()
                    a_button.draw()


    def draw_image(self, img, img_name, x_coord, y_coord, img_width = None, img_height = None):
        if self._on:
            if img_width and img_height:
                image = pygame.transform.scale(img, (img_width, img_height))
                PROGRAM_DISPLAY.blit(image, (x_coord, y_coord))
            elif not img_width and not img_height:
                PROGRAM_DISPLAY.blit(img, (x_coord, y_coord))
                img_width, img_height = img.get_rect()[2], img.get_rect()[3]
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


    def get_background_img(self):
        return self._background_img


    def get_background_color(self):
        return self._background_color


    def is_running(self):
        return self._on

    

###########################################
INTRO_SCREEN = Screen()

def intro_screen_loop():
    INTRO_SCREEN.set_on()
    INTRO_SCREEN.set_background(WHITE)
    intro_b = Button("Intro", 50, 250, SCR1_MENU_W, SCR1_MENU_H, GREEN, LIGHT_GREEN, "Intro", BLACK, SCR1_MENU_TEXT, INTRO_SCREEN.get_background_type(),
                      INTRO_SCREEN.get_background_img(), INTRO_SCREEN.get_background_color())
    math_b = Button("Math", 300, 250, SCR1_MENU_W, SCR1_MENU_H, GREEN, LIGHT_GREEN, "Math", BLACK, SCR1_MENU_TEXT, INTRO_SCREEN.get_background_type(),
                          INTRO_SCREEN.get_background_img(), INTRO_SCREEN.get_background_color())
    reading_b = Button("Reading", 550, 250, SCR1_MENU_W, SCR1_MENU_H, GREEN, LIGHT_GREEN, "Reading", BLACK, SCR1_MENU_TEXT, INTRO_SCREEN.get_background_type(),
                          INTRO_SCREEN.get_background_img(), INTRO_SCREEN.get_background_color())
    writing_b = Button("Writing", 800, 250, SCR1_MENU_W, SCR1_MENU_H, GREEN, LIGHT_GREEN, "Writing", BLACK, SCR1_MENU_TEXT, INTRO_SCREEN.get_background_type(),
                          INTRO_SCREEN.get_background_img(), INTRO_SCREEN.get_background_color())
    random_b = Button("Random", 1050, 250, SCR1_MENU_W, SCR1_MENU_H, GREEN, LIGHT_GREEN, "Random", BLACK, SCR1_MENU_TEXT, INTRO_SCREEN.get_background_type(),
                          INTRO_SCREEN.get_background_img(), INTRO_SCREEN.get_background_color())

    math_reference_b = Button("Math- Reference", 325, 340, SCR1_SUBMENU_W, SCR1_SUBMENU_H, LIGHT_BLUE, AQUA, "Reference", BLACK, SCR1_SUBMENU_TEXT,
                              INTRO_SCREEN.get_background_type(), INTRO_SCREEN.get_background_img(), INTRO_SCREEN.get_background_color())
    reading_vocab_b = Button("Reading- Vocab", 575, 340, SCR1_SUBMENU_W, SCR1_SUBMENU_H, LIGHT_BLUE, AQUA, "Vocabulary", BLACK, SCR1_SUBMENU_TEXT,
                              INTRO_SCREEN.get_background_type(), INTRO_SCREEN.get_background_img(), INTRO_SCREEN.get_background_color())
    writing_grammar_b = Button("Writing- Grammar", 825, 340, SCR1_SUBMENU_W, SCR1_SUBMENU_H, LIGHT_BLUE, AQUA, "Grammar", BLACK, SCR1_SUBMENU_TEXT,
                              INTRO_SCREEN.get_background_type(), INTRO_SCREEN.get_background_img(), INTRO_SCREEN.get_background_color())
    math_practice_b = Button("Math- Practice", 325, 540, SCR1_SUBMENU_W, SCR1_SUBMENU_H, LIGHT_BLUE, AQUA, "Practice", BLACK, SCR1_SUBMENU_TEXT,
                              INTRO_SCREEN.get_background_type(), INTRO_SCREEN.get_background_img(), INTRO_SCREEN.get_background_color())

    INTRO_B_PRESS = {intro_b: [0, 100, move, "Down", 10, False],
                     math_b: [None, None, shrink_disappear, 5, False]}

    intro_b.set_on()
    math_b.set_on()
    reading_b.set_on()
    writing_b.set_on()
    random_b.set_on()

    math_reference_b.set_on()
    reading_vocab_b.set_on()
    writing_grammar_b.set_on()
    math_practice_b.set_on()

    while INTRO_SCREEN.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        INTRO_SCREEN.draw_text("SAT FUN PREP", "Title", BLACK, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.15, SCR1_TITLE_TEXT)
                
        INTRO_SCREEN.draw_buttons(None, [intro_b, math_b, reading_b, writing_b, random_b])
        INTRO_SCREEN.draw_buttons(None, [math_reference_b, reading_vocab_b, writing_grammar_b, math_practice_b])


        if intro_b.is_pressed():
            simult_animations(INTRO_B_PRESS)

        
        pygame.display.update()




intro_screen_loop()






            
