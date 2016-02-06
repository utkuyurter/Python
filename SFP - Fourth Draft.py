"""
SFP- SAT Fun Prep
"""

import pygame, sys
import random, math
import screen_class
import image_button_class
import text_class

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
VIOLET = (250, 0, 250)

# Width and height of main buttons (like Intro, Math, etc.). SCR1 means screen no. 1
SCR1_MENU_W = 200
SCR1_MENU_H = 75

# Width and height of sub-buttons.
SCR1_SUBMENU_W = 175
SCR1_SUBMENU_H = 60

#Width and Height of mini-buttons.
SCR1_MINI_W = 140
SCR1_MINI_H = 50

# Text configurations. One for title, one for main buttons, one for sub-buttons
SCR1_TITLE_TEXT = pygame.font.Font("cour.ttf", 130)
SCR1_MENU_TEXT = pygame.font.Font("cour.ttf", 40)
SCR1_SUBMENU_TEXT = pygame.font.Font("cour.ttf", 20)
SCR1_MINI_TEXT = pygame.font.Font("cour.ttf", 15)

# Dictionary that maps button configurations to a tuple containing their data,
# so that they can be accessed individually not only as a whole Font object
TEXT_CONFIG_DICT = {SCR1_TITLE_TEXT: ("cour.ttf", 120),
                    SCR1_MENU_TEXT: ("cour.ttf", 40),
                    SCR1_SUBMENU_TEXT: ("cour.ttf", 20),
                    SCR1_MINI_TEXT: ("cour.ttf", 15)}




#########################################################################


# Helper functions

def cover_up(background_type, x_coord, y_coord, width, height, background_img = None, background_color = None):
    """
    Function that 'erases' a part of the display before a new button is drawn, or when a button is set off.
    """
    if background_type == "Image":
        PROGRAM_DISPLAY.blit(background_img, (x_coord, y_coord), (x_coord, y_coord, width, height))
    else:
        PROGRAM_DISPLAY.fill(background_color, (x_coord, y_coord, width, height))


def pythagorean(x, y):
    """
    Computes distance between the two given points.
    """
    return math.sqrt((x ** 2) + (y ** 2))



def distance_formula(x, y):
    """
    Computes distance between the two given points.
    """
    return math.sqrt((x ** 2) + (y ** 2))


def points_dist_formula(point1, point2):
    return math.sqrt(((point2[0] - point1[0]) ** 2) + ((point2[1] - point1[1]) ** 2))


def center_to_topleft(center, width, height):
    return (center[0] - (width / 2), center[1] - (height / 2))


def topleft_to_center(topleft, width, height):
    return (topleft[0] + (width / 2), topleft[1] + (height / 2))




#########################################################################


# Animation functions

def move(thing, type_speed, covered, target):
    """
    Moves an object one step, and doesn't draw or update anything other than positions. Can move the object up, down,
    right, left, or diagonally through the given slope.

    Returns the number of units covered at that moment. If it is done, returns True.
    """
    not_done = False
    if type(target) == int:
        not_done = covered < target
    else:
        not_done = thing.get_loc() != target
    if not_done:
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
            x_left = math.fabs(target[0] - thing.get_loc()[0])
            y_left = math.fabs(target[1] - thing.get_loc()[1])
            x_rate = float(x_left) / y_left
            if target[0] > thing.get_loc()[0]:
                x_direction = 1
            elif target[0] < thing.get_loc()[0]:
                x_direction = -1
            if target[1] > thing.get_loc()[1]:
                y_direction = 1
            elif target[1] < thing.get_loc()[1]:
                y_direction = -1
            x_change = x_rate * type_speed[0] * x_direction
            y_change = type_speed[0] * y_direction
            if x_direction == 1:
                if thing.get_loc()[0] + x_change <= target[0]:
                    thing.change_x(x_change)
                elif thing.get_loc()[0] < target[0]:
                    left = target[0] - thing.get_loc()[0]
                    thing.change_x(left)
            elif x_direction == -1:
                if thing.get_loc()[0] + x_change >= target[0]:
                    thing.change_x(x_change)
                elif thing.get_loc()[0] > target[0]:
                    left = target[0] - thing.get_loc()[0]
                    thing.change_x(left)
            if y_direction == 1:
                if thing.get_loc()[1] + y_change <= target[1]:
                    thing.change_y(y_change)
                elif thing.get_loc()[1] < target[1]:
                    left = target[1] - thing.get_loc()[1]
                    thing.change_y(left)
            elif y_direction == -1:
                if thing.get_loc()[1] + y_change >= target[1]:
                    thing.change_y(y_change)
                elif thing.get_loc()[1] > target[1]:
                    left = target[1] - thing.get_loc()[1]
                    thing.change_y(left)
            return thing.get_loc()
    return True



def shrink_disappear(thing, speed, done, target):
    """
    Makes an object disappear gradually by making it shrink at the given speed, one step at a time.
    Only updates positions; no drawing. Returns False if it's not done yet and True otherwise.
    """
    accomplished = False
    cover_up(thing.get_scr_background_type(), thing.get_loc()[0], thing.get_loc()[1], thing.get_width(), thing.get_height(), thing.get_scr_background_img(),
             thing.get_scr_background_color())
    thing.change_x(speed[0])
    thing.change_y(speed[0])
    thing.change_width(-2 * speed[0])
    thing.change_height(-2 * speed[0])
    if thing.get_width() < 2 or thing.get_height() < 2:
        thing.set_off()
        accomplished = True
    return accomplished



def enlarge_appear(thing, speed, done, target):
    accomplished = False
    if not thing.is_on():
        thing.set_on(thing.get_loc(), thing.get_width(), thing.get_height())    
    cover_up(thing.get_scr_background_type(), thing.get_loc()[0], thing.get_loc()[1], thing.get_width(), thing.get_height(), thing.get_scr_background_img(),
             thing.get_scr_background_color())
    if thing.get_width() + (2 * speed[0]) <= target[0]:
        thing.change_x(- speed[0])
        thing.change_width(2 * speed[0])
    elif thing.get_width() < target[0]:
        left = target[0] - thing.get_width()
        thing.change_x(- (left / 2))
        thing.change_width(left)
    if thing.get_height() + (2 * speed[0]) <= target[1]:
        thing.change_y(- speed[0])
        thing.change_height(2 * speed[0])
    elif thing.get_height() < target[1]:
        left = target[1] - thing.get_height()
        thing.change_y(- (left / 2))
        thing.change_height(left)
    if thing.get_width() == target[0] and thing.get_height() == target[1]:
        accomplished = True
    return accomplished


def text_enlarge(text, speed, done, target):
    accomplished = False
    if text.get_size() + speed[0] <= target:
        text.change_size(speed[0])
    elif text.get_size() < target:
        left = target - text.get_size()
        text.change_size(left)
    if text.get_size() == target:
        accomplished = True
    return accomplished



def pixel_fade_disappear(thing, speed, done, target):
    pass
    
    
def fade_disappear():
    pass

    
def pixel_fade_appear():
    pass


def fade_appear(thing, speed, done, target):
    pass
    
    


def simult_animations(things_and_animations):
    """
    Takes a dictionary as input and uses it to animate different buttons with different types of animations simultaneously.
    """
    copy_dict = dict((key, list(val)) for key, val in things_and_animations.items())
    while copy_dict:
        for thing in copy_dict.keys():
            data = copy_dict[thing]
            covered = data[2](thing, [param for param in data[3 : -1]], data[0], data[1])
            thing.draw()
            if type(covered) == int or type(covered) == float:
                copy_dict[thing][0] = covered

            elif type(covered) == bool:
                if covered:
                    copy_dict[thing][-1] = True
        for thing in copy_dict.keys():
            if copy_dict[thing][-1]:
                copy_dict.pop(thing)
        pygame.display.update()
        CLOCK.tick(20)
 


          

###################################

        
INTRO_SCREEN = screen_class.Screen()
INTRO_B_SCREEN = screen_class.Screen()
MATH_B_SCREEN = screen_class.Screen()
READING_B_SCREEN = screen_class.Screen()
WRITING_B_SCREEN = screen_class.Screen()
RANDOM_B_SCREEN = screen_class.Screen()
INFO_SCREEN = screen_class.Screen()
OPENING_SCREEN = screen_class.Screen()
CLOSING_SCREEN = screen_class.Screen()
MATH_REF_RULES_B_SCREEN_1 = screen_class.Screen()
MATH_REF_RULES_B_SCREEN_2 = screen_class.Screen()


info1 = pygame.image.load('info.png')
info2 = pygame.image.load('info2.png')
back1 = pygame.image.load('back6.png')
back2 = pygame.image.load('back3.png')
forward1 = pygame.image.load('forward1.png')
forward2 = pygame.image.load('forward2.png')
        

#MAIN IMAGES
intro_b_1 = pygame.image.load('intro_b_1.png')
intro_b_2 = pygame.image.load('intro_b_2.png')
math_b_1 = pygame.image.load('math_b_1.png')
math_b_2 = pygame.image.load('math_b_2.png')
reading_b_1 = pygame.image.load('reading_b_1.png')
reading_b_2 = pygame.image.load('reading_b_2.png')
writing_b_1 = pygame.image.load('writing_b_1.png')
writing_b_2 = pygame.image.load('writing_b_2.png')
random_b_1 = pygame.image.load('random_b_1.png')
random_b_2 = pygame.image.load('random_b_2.png')

#SUB IMAGES
vocab_b_1 = pygame.image.load('vocab1.png')
vocab_b_2 = pygame.image.load('vocab2.png')
essay_b_1 = pygame.image.load('essay1.png')
essay_b_2 = pygame.image.load('essay2.png')
comprehension_b_1 = pygame.image.load('comprehension1.png')
comprehension_b_2 = pygame.image.load('comprehension2.png')
grammar_b_1 = pygame.image.load('grammar1.png')
grammar_b_2 = pygame.image.load('grammar2.png')
practice_b_1 = pygame.image.load('practice1.png')
practice_b_2 = pygame.image.load('practice2.png')
road_b_1 = pygame.image.load('road1.png')
road_b_2 = pygame.image.load('road2.png')
reference_b_1 = pygame.image.load('reference1.png')
reference_b_2 = pygame.image.load('reference2.png')
road_b_1 = pygame.image.load('road1.png')
road_b_2 = pygame.image.load('road2.png')

#MINI IMAGES
math_rules_b_1 = pygame.image.load('math_rules_1.png')
math_rules_b_2 = pygame.image.load('math_rules_2.png')
math_sample_b_1 = pygame.image.load('math_sample_1.png')
math_sample_b_2 = pygame.image.load('math_sample_2.png')
math_ref_res_b_1 = pygame.image.load('math_ref_res_1.png')
math_ref_res_b_2 = pygame.image.load('math_ref_res_2.png')
math_mini_b_1 =  pygame.image.load('math_mini_1.png')
math_mini_b_2 =  pygame.image.load('math_mini_2.png')
math_timed_b_1 = pygame.image.load('math_timed_1.png')
math_timed_b_2 = pygame.image.load('math_timed_2.png')
math_practice_res_b_1 = pygame.image.load('math_practice_res_1.png')
math_practice_res_b_2 = pygame.image.load('math_practice_res_2.png')

reading_vocab_mini_b_1 = pygame.image.load('reading_vocab_mini_1.png')
reading_vocab_mini_b_2 = pygame.image.load('reading_vocab_mini_2.png')
reading_vocab_practice_b_1 = pygame.image.load('reading_vocab_practice_1.png')
reading_vocab_practice_b_2 = pygame.image.load('reading_vocab_practice_2.png')
reading_comprehension_stories_b_1 = pygame.image.load('reading_comprehension_stories_1.png')
reading_comprehension_stories_b_2 = pygame.image.load('reading_comprehension_stories_2.png')
reading_comprehension_practice_b_1 = pygame.image.load('reading_comprehension_practice_1.png')
reading_comprehension_practice_b_2 = pygame.image.load('reading_comprehension_practice_2.png')
reading_road_recommendations_b_1 = pygame.image.load('reading_road_recommendations_1.png')
reading_road_recommendations_b_2 = pygame.image.load('reading_road_recommendations_2.png')
reading_road_progress_b_1 = pygame.image.load('reading_road_progress_1.png')
reading_road_progress_b_2 = pygame.image.load('reading_road_progress_2.png')

writing_grammar_rhymes_1 = pygame.image.load('grammar_rhymes_1.png')
writing_grammar_rhymes_2 = pygame.image.load('grammar_rhymes_2.png')
writing_grammar_mini_games_1 = pygame.image.load('grammar_mini_1.png')
writing_grammar_mini_games_2 = pygame.image.load('grammar_mini_2.png')
writing_essay_tips_1 = pygame.image.load('essay_tips_1.png')
writing_essay_tips_2 = pygame.image.load('essay_tips_2.png')
writing_essay_templates_1 = pygame.image.load('essay_templates_1.png')
writing_essay_templates_2 = pygame.image.load('essay_templates_2.png')


#TITLES
SFP_TITLE = pygame.image.load('SFP_TITLE2.png')
MATH_TITLE = pygame.image.load('MATH_TITLE_1.png')
READING_TITLE = pygame.image.load('READING_TITLE_1.png')
WRITING_TITLE = pygame.image.load('WRITING_TITLE_1.png')
RANDOM_TITLE = pygame.image.load('RANDOM_TITLE_1.png')
INFO_TITLE = pygame.image.load('INFO_TITLE_1.png')
INTRO_TITLE = pygame.image.load('INTRO_TITLE_1.png')

#BACKGROUNDS
background_main = pygame.image.load('main.jpg')
background_math = pygame.image.load('math2.jpg')
background_writing = pygame.image.load('writing.jpg')
background_reading = pygame.image.load('reading.jpg')
background_info = pygame.image.load('background3.jpg')
background_random = pygame.image.load('random.jpg')
background_intro = pygame.image.load('background4.jpg')
background_opening = pygame.image.load('opening.jpg')
background_closing = pygame.image.load('closing.jpg')


screen = 1

####SCREEN LOOPS


def intro_screen_loop():
    INTRO_SCREEN.set_on()
    INTRO_SCREEN.set_background(background_main)
    
    
    info = image_button_class.Image_Button('info' , info1, info2, 1210, 620, 70 , 70, INTRO_SCREEN.get_background_type(), INTRO_SCREEN.get_background_img(), INTRO_SCREEN.get_background_color())
    intro_b = image_button_class.Image_Button('intro' , intro_b_1, intro_b_2, 50, 250, SCR1_MENU_W, SCR1_MENU_H , INTRO_SCREEN.get_background_type(), INTRO_SCREEN.get_background_img(), INTRO_SCREEN.get_background_color())
    math_b = image_button_class.Image_Button('math' , math_b_1, math_b_2, 300, 250, SCR1_MENU_W , SCR1_MENU_H  , INTRO_SCREEN.get_background_type(), INTRO_SCREEN.get_background_img(), INTRO_SCREEN.get_background_color())
    reading_b = image_button_class.Image_Button('reading' , reading_b_1, reading_b_2, 550, 250, SCR1_MENU_W , SCR1_MENU_H  , INTRO_SCREEN.get_background_type(), INTRO_SCREEN.get_background_img(), INTRO_SCREEN.get_background_color())
    writing_b = image_button_class.Image_Button('writing' , writing_b_1, writing_b_2, 800, 250, SCR1_MENU_W, SCR1_MENU_H  , INTRO_SCREEN.get_background_type(), INTRO_SCREEN.get_background_img(), INTRO_SCREEN.get_background_color())
    random_b = image_button_class.Image_Button('random' , random_b_1, random_b_2, 1050, 250, SCR1_MENU_W, SCR1_MENU_H , INTRO_SCREEN.get_background_type(), INTRO_SCREEN.get_background_img(), INTRO_SCREEN.get_background_color())


    MATH_B_PRESS = {intro_b: [None, None, shrink_disappear, 5, False],
                      reading_b: [None, None, shrink_disappear, 5, False],
                      writing_b: [None, None, shrink_disappear, 5, False],
                      random_b: [None, None, shrink_disappear, 5, False]}


    READING_B_PRESS = {intro_b: [None, None, shrink_disappear, 5, False],
                      math_b: [None, None, shrink_disappear, 5, False],
                      writing_b: [None, None, shrink_disappear, 5, False],
                      random_b: [None, None, shrink_disappear, 5, False]}


    WRITING_B_PRESS = {intro_b: [None, None, shrink_disappear, 5, False],
                      math_b: [None, None, shrink_disappear, 5, False],
                      reading_b: [None, None, shrink_disappear, 5 ,False],
                      random_b: [None, None, shrink_disappear, 5, False]}


    RANDOM_B_PRESS = {intro_b: [None, None, shrink_disappear, 5, False],
                      math_b: [None, None, shrink_disappear, 5, False],
                      reading_b: [None, None, shrink_disappear, 5 ,False],
                      writing_b: [None, None, shrink_disappear, 5, False]}

    INTRO_B_PRESS = {writing_b: [None, None, shrink_disappear, 5, False],
                     math_b: [None, None, shrink_disappear, 5, False],
                     reading_b: [None, None, shrink_disappear, 5 ,False],
                     random_b: [None, None, shrink_disappear, 5, False]}

                         
    intro_b.set_on()
    math_b.set_on()
    reading_b.set_on()
    writing_b.set_on()
    random_b.set_on()
    info.set_on()
    

    while INTRO_SCREEN.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closing()
                pygame.quit()
                sys.exit()

                
        

        INTRO_SCREEN.draw_image(SFP_TITLE, "SAT FUN PREP",  DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.15, 550, 120)
        
        INTRO_SCREEN.draw_text("SFPver0.1.10", "Ver", BLACK, 70, 670 , SCR1_MINI_TEXT)
        
        INTRO_SCREEN.draw_img_buttons(None, [info, intro_b, math_b, reading_b, writing_b, random_b])

        if math_b.is_pressed():
            simult_animations(MATH_B_PRESS)
            math_button_press_loop()

        elif reading_b.is_pressed():
            simult_animations(READING_B_PRESS)
            reading_button_press_loop()
            
        elif intro_b.is_pressed():
            simult_animations(INTRO_B_PRESS)
            intro_button_screen_loop() 
            
        elif random_b.is_pressed():
            simult_animations(RANDOM_B_PRESS)
            random_button_press_loop()

        elif info.is_pressed():
            info_button_press_loop()

        elif writing_b.is_pressed():
            simult_animations(WRITING_B_PRESS)
            writing_button_press_loop()
       
        pygame.display.update()

############################
#MAIN SCREENS

def intro_button_screen_loop():
    INTRO_B_SCREEN.set_on()
    INTRO_B_SCREEN.set_background(background_intro)
    

    back = image_button_class.Image_Button('back_b' , back1, back2 , 100, 600, 50 , 50, INTRO_B_SCREEN.get_background_type(), INTRO_B_SCREEN.get_background_img(), INTRO_B_SCREEN.get_background_color())
    back.set_on()

    intro_b = image_button_class.Image_Button('intro' , intro_b_1, intro_b_2, 50, 250, SCR1_MENU_W, SCR1_MENU_H , INTRO_B_SCREEN.get_background_type(), INTRO_B_SCREEN.get_background_img(), INTRO_B_SCREEN.get_background_color())
    

    INTRO_B_MOVE = {intro_b: [0, center_to_topleft((DISPLAY_WIDTH / 2, 100), intro_b.get_width(), intro_b.get_height()), move, 10, False]}

    intro_b.set_on()
    simult_animations(INTRO_B_MOVE)
    intro_b.set_off()
    INTRO_SCREEN.draw_image(INTRO_TITLE, "INTRO_TITLE",  DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.15, 550, 120)
    
    while INTRO_B_SCREEN.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closing()
                pygame.quit()
                sys.exit()

        
        
        INTRO_B_SCREEN.draw_img_buttons(None, [back, intro_b])

        if back.is_pressed():
            intro_screen_loop()

        pygame.display.update()




        

def random_button_press_loop():
    RANDOM_B_SCREEN.set_on()
    RANDOM_B_SCREEN.set_background(background_random)
    

    back = image_button_class.Image_Button('back_b' , back1, back2 , 100, 600, 50 , 50, RANDOM_B_SCREEN.get_background_type(), RANDOM_B_SCREEN.get_background_img(), RANDOM_B_SCREEN.get_background_color())
    back.set_on()


    random_b = image_button_class.Image_Button('random' , random_b_1, random_b_2, 1050, 250, SCR1_MENU_W, SCR1_MENU_H , RANDOM_B_SCREEN.get_background_type(), RANDOM_B_SCREEN.get_background_img(), RANDOM_B_SCREEN.get_background_color())

    

    RANDOM_B_MOVE = {random_b: [0, center_to_topleft((DISPLAY_WIDTH / 2, 100), random_b.get_width(), random_b.get_height()), move, 10, False]}

    random_b.set_on()
    simult_animations(RANDOM_B_MOVE)
    random_b.set_off()
    INTRO_SCREEN.draw_image(RANDOM_TITLE, "RANDOM_TITLE",  DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.15, 550, 120)
    
    while RANDOM_B_SCREEN.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closing()
                pygame.quit()
                sys.exit()

       
        RANDOM_B_SCREEN.draw_img_buttons(None, [back, random_b])

        if back.is_pressed():
            intro_screen_loop()

            
        pygame.display.update()






def info_button_press_loop():
    INFO_SCREEN.set_on()
    INFO_SCREEN.set_background(background_info)
    
    
    back = image_button_class.Image_Button('back_b' , back1, back2 , 100, 600, 50 , 50, INFO_SCREEN.get_background_type(), INFO_SCREEN.get_background_img(), INFO_SCREEN.get_background_color())
    back.set_on()
   
    
    while INFO_SCREEN.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closing()
                pygame.quit()
                sys.exit()


        INFO_SCREEN.draw_img_buttons(None, [back])
        INTRO_SCREEN.draw_image(INFO_TITLE, "INFO_TITLE",  DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.15, 550, 120)
        
        if back.is_pressed():
            intro_screen_loop()


        pygame.display.update()



def math_button_press_loop():
    MATH_B_SCREEN.set_on()
    MATH_B_SCREEN.set_background(background_math)
    
    back = image_button_class.Image_Button('back_b' , back1, back2 , 100, 600, 50 , 50, MATH_B_SCREEN.get_background_type(), MATH_B_SCREEN.get_background_img(), MATH_B_SCREEN.get_background_color())
    back.set_on()
    

    math_b = image_button_class.Image_Button('math' , math_b_1, math_b_2, 300, 250, SCR1_MENU_W , SCR1_MENU_H  , MATH_B_SCREEN.get_background_type(), MATH_B_SCREEN.get_background_img(), MATH_B_SCREEN.get_background_color())

    math_reference_b = image_button_class.Image_Button("Math- Reference", reference_b_1, reference_b_2, 347, 170, SCR1_SUBMENU_W, SCR1_SUBMENU_H,  MATH_B_SCREEN.get_background_type(), MATH_B_SCREEN.get_background_img(), MATH_B_SCREEN.get_background_color())
    
    math_practice_b = image_button_class.Image_Button("Math- Practice", practice_b_1, practice_b_2, 680, 170, SCR1_SUBMENU_W, SCR1_SUBMENU_H, MATH_B_SCREEN.get_background_type(), MATH_B_SCREEN.get_background_img(), MATH_B_SCREEN.get_background_color())
    

    math_rules_b = image_button_class.Image_Button("Math-Rules_and_Formulas",math_rules_b_1, math_rules_b_2, 370, 250, SCR1_MINI_W, SCR1_MINI_H, MATH_B_SCREEN.get_background_type(), MATH_B_SCREEN.get_background_img(), MATH_B_SCREEN.get_background_color())

    math_sample_b = image_button_class.Image_Button("Math-Sample-Questions",math_sample_b_1, math_sample_b_2, 370, 320, SCR1_MINI_W, SCR1_MINI_H, MATH_B_SCREEN.get_background_type(), MATH_B_SCREEN.get_background_img(), MATH_B_SCREEN.get_background_color())

    math_reference_resources_b = image_button_class.Image_Button("Math-Reference_Resources",math_ref_res_b_1, math_ref_res_b_2, 370, 339, SCR1_MINI_W, SCR1_MINI_H, MATH_B_SCREEN.get_background_type(), MATH_B_SCREEN.get_background_img(), MATH_B_SCREEN.get_background_color())

    math_mini_b = image_button_class.Image_Button("Math-Mini-Games",math_mini_b_1, math_mini_b_2, 703, 250, SCR1_MINI_W, SCR1_MINI_H, MATH_B_SCREEN.get_background_type(), MATH_B_SCREEN.get_background_img(), MATH_B_SCREEN.get_background_color())

    math_timed_questions_b = image_button_class.Image_Button("Math-Mini-Games",math_timed_b_1, math_timed_b_2, 703, 320, SCR1_MINI_W, SCR1_MINI_H, MATH_B_SCREEN.get_background_type(), MATH_B_SCREEN.get_background_img(), MATH_B_SCREEN.get_background_color())

    math_practice_resources_b = image_button_class.Image_Button("Math-Mini-Games",math_practice_res_b_1, math_practice_res_b_2, 703, 339, SCR1_MINI_W, SCR1_MINI_H, MATH_B_SCREEN.get_background_type(), MATH_B_SCREEN.get_background_img(), MATH_B_SCREEN.get_background_color())



    
    MATH_B_MOVE = {math_b: [0, center_to_topleft((DISPLAY_WIDTH / 2, 100), math_b.get_width(), math_b.get_height()), move, 10, False]}
    

    SUB_ANIM = {math_reference_b: [None, (math_reference_b.get_init_vals()['init width'], math_reference_b.get_init_vals()['init height']), enlarge_appear, 10, False],
                math_practice_b: [None, (math_practice_b.get_init_vals()['init width'], math_practice_b.get_init_vals()['init height']), enlarge_appear, 10, False]}
    

    REF_B_PRESS = {math_rules_b: [None, (math_rules_b.get_init_vals()['init width'], math_rules_b.get_init_vals()['init height']), enlarge_appear, 5, False],
                   math_sample_b: [None, (math_sample_b.get_init_vals()['init width'], math_sample_b.get_init_vals()['init height']), enlarge_appear, 5, False],
                   math_reference_resources_b: [None, (math_reference_resources_b.get_init_vals()['init width'], math_reference_resources_b.get_init_vals()['init height']), enlarge_appear, 5, False]}
    

    PRACTICE_B_PRESS = {math_mini_b: [None, (math_mini_b.get_init_vals()['init width'], math_mini_b.get_init_vals()['init height']), enlarge_appear, 5, False],
                        math_timed_questions_b: [None, (math_timed_questions_b.get_init_vals()['init width'], math_timed_questions_b.get_init_vals()['init height']), enlarge_appear, 5, False],
                        math_practice_resources_b: [None, (math_practice_resources_b.get_init_vals()['init width'], math_practice_resources_b.get_init_vals()['init height']), enlarge_appear, 5, False]}


        
    
    math_b.set_on()
    math_reference_b.set_on()
    math_practice_b.set_on()

    math_rules_b.set_on()
    math_sample_b.set_on()    
    math_reference_resources_b.set_on()
    math_mini_b.set_on()
    math_timed_questions_b.set_on()
    math_practice_resources_b.set_on()

    math_reference_b.change_x(SCR1_SUBMENU_W / 2)
    math_reference_b.change_y(SCR1_SUBMENU_H / 2)
    math_reference_b.change_width(- SCR1_SUBMENU_W / 2)
    math_reference_b.change_height(- SCR1_SUBMENU_H / 2)
    math_practice_b.change_x(SCR1_SUBMENU_W / 2)
    math_practice_b.change_y(SCR1_SUBMENU_H / 2)
    math_practice_b.change_width(- SCR1_SUBMENU_W / 2)
    math_practice_b.change_height(- SCR1_SUBMENU_H / 2)


    math_rules_b.change_x(SCR1_MINI_W / 2)
    math_rules_b.change_y(SCR1_MINI_H / 2)
    math_rules_b.change_width(- SCR1_MINI_W / 2)
    math_rules_b.change_height(- SCR1_MINI_H / 2)
    math_sample_b.change_x(SCR1_MINI_W / 2)
    math_sample_b.change_y(SCR1_MINI_H / 2)
    math_sample_b.change_width(- SCR1_MINI_W / 2)
    math_sample_b.change_height(- SCR1_MINI_H / 2)
    math_reference_resources_b.change_x(SCR1_MINI_W / 2)
    math_reference_resources_b.change_y(SCR1_MINI_W / 2)
    math_reference_resources_b.change_width(- SCR1_MINI_W / 2)
    math_reference_resources_b.change_height(- SCR1_MINI_H / 2)

    math_mini_b.change_x(SCR1_MINI_W / 2)
    math_mini_b.change_y(SCR1_MINI_H / 2)
    math_mini_b.change_width(- SCR1_MINI_W / 2)
    math_mini_b.change_height(- SCR1_MINI_H / 2)
    math_timed_questions_b.change_x(SCR1_MINI_W / 2)
    math_timed_questions_b.change_y(SCR1_MINI_H / 2)
    math_timed_questions_b.change_width(- SCR1_MINI_W / 2)
    math_timed_questions_b.change_height(- SCR1_MINI_H / 2)
    math_practice_resources_b.change_x(SCR1_MINI_W / 2)
    math_practice_resources_b.change_y(SCR1_MINI_W / 2)
    math_practice_resources_b.change_width(- SCR1_MINI_W / 2)
    math_practice_resources_b.change_height(- SCR1_MINI_H / 2)
    

    simult_animations(MATH_B_MOVE)
    math_b.set_off()
    MATH_B_SCREEN.draw_image(MATH_TITLE, "MATH TITLE",  DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.15, 550, 120)
    
    simult_animations(SUB_ANIM)

    math_rules_b.set_off()
    math_sample_b.set_off()
    math_reference_resources_b.set_off()
    math_mini_b.set_off()
    math_timed_questions_b.set_off()
    math_practice_resources_b.set_off()
    
    
    
    while MATH_B_SCREEN.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closing()
                pygame.quit()
                sys.exit()


        MATH_B_SCREEN.draw_img_buttons(None, [back, math_b, math_reference_b, math_practice_b, math_rules_b, math_sample_b, math_reference_resources_b, math_mini_b, math_timed_questions_b, math_practice_resources_b])
    
 
        
        if back.is_pressed():
            intro_screen_loop()
            
            
        if math_reference_b.is_pressed() and not math_rules_b.is_on():
            simult_animations(REF_B_PRESS)
            math_reference_b.unanimated()
            
        elif math_practice_b.is_pressed() and not math_mini_b.is_on():
            simult_animations(PRACTICE_B_PRESS)
            math_practice_b.unanimated()
            
        elif math_rules_b.is_pressed():
           math_ref_rules_scr1()
            
            
        
        pygame.display.update()


def reading_button_press_loop():
    READING_B_SCREEN.set_on()
    READING_B_SCREEN.set_background(background_reading)
   
    
    back = image_button_class.Image_Button('back_b' , back1, back2 , 100, 600, 50 , 50, READING_B_SCREEN.get_background_type(), READING_B_SCREEN.get_background_img(), READING_B_SCREEN.get_background_color())
    back.set_on()
       
   
    reading_b = image_button_class.Image_Button('reading' , reading_b_1, reading_b_2, 550, 250, SCR1_MENU_W , SCR1_MENU_H  , READING_B_SCREEN.get_background_type(), READING_B_SCREEN.get_background_img(), READING_B_SCREEN.get_background_color())
       

    reading_vocab_b = image_button_class.Image_Button('reading-vocab' , vocab_b_1, vocab_b_2, 530, 175, SCR1_SUBMENU_W , SCR1_SUBMENU_H  , READING_B_SCREEN.get_background_type(), READING_B_SCREEN.get_background_img(), READING_B_SCREEN.get_background_color())
       
    reading_comprehension_b = image_button_class.Image_Button('reading-comprehension' , comprehension_b_1, comprehension_b_2, 155, 175, SCR1_SUBMENU_W , SCR1_SUBMENU_H  , READING_B_SCREEN.get_background_type(), READING_B_SCREEN.get_background_img(), READING_B_SCREEN.get_background_color())
       
    reading_road_b = image_button_class.Image_Button('reading-road' , road_b_1, road_b_2, 905, 175, SCR1_SUBMENU_W , SCR1_SUBMENU_H  , READING_B_SCREEN.get_background_type(), READING_B_SCREEN.get_background_img(), READING_B_SCREEN.get_background_color())


       
    reading_vocab_mini_games_b = image_button_class.Image_Button('reading-vocab_mini_games' , reading_vocab_mini_b_1, reading_vocab_mini_b_2, 552, 260, SCR1_MINI_W , SCR1_MINI_H  , READING_B_SCREEN.get_background_type(), READING_B_SCREEN.get_background_img(), READING_B_SCREEN.get_background_color())
       
    reading_vocab_practice_b = image_button_class.Image_Button('reading-vocab_practice' , reading_vocab_practice_b_1, reading_vocab_practice_b_2, 552, 330, SCR1_MINI_W , SCR1_MINI_H  , READING_B_SCREEN.get_background_type(), READING_B_SCREEN.get_background_img(), READING_B_SCREEN.get_background_color())
       
    reading_comprehension_stories_b = image_button_class.Image_Button('reading-comprehension_stories' , reading_comprehension_stories_b_1, reading_comprehension_stories_b_2, 177, 260, SCR1_MINI_W , SCR1_MINI_H  , READING_B_SCREEN.get_background_type(), READING_B_SCREEN.get_background_img(), READING_B_SCREEN.get_background_color())
       
    reading_comprehension_practice_b = image_button_class.Image_Button('reading-comrehension_practice' , reading_comprehension_practice_b_1, reading_comprehension_practice_b_2, 177, 330, SCR1_MINI_W , SCR1_MINI_H  , READING_B_SCREEN.get_background_type(), READING_B_SCREEN.get_background_img(), READING_B_SCREEN.get_background_color())
    
    reading_road_recommendations_b = image_button_class.Image_Button('reading-road_recommendations' , reading_road_recommendations_b_1, reading_road_recommendations_b_2, 927, 260, SCR1_MINI_W , SCR1_MINI_H  , READING_B_SCREEN.get_background_type(), READING_B_SCREEN.get_background_img(), READING_B_SCREEN.get_background_color())
       
    reading_road_progress_b = image_button_class.Image_Button('reading-road_progress' , reading_road_progress_b_1, reading_road_progress_b_2, 927, 330, SCR1_MINI_W , SCR1_MINI_H  , READING_B_SCREEN.get_background_type(), READING_B_SCREEN.get_background_img(), READING_B_SCREEN.get_background_color())
       



    READING_B_MOVE = {reading_b: [0, 150, move, 'Up', -10, 25, False]}

    

    SUB_ANIM = {reading_vocab_b: [None, (reading_vocab_b.get_init_vals()['init width'], reading_vocab_b.get_init_vals()['init height']), enlarge_appear, 10, False],
             reading_comprehension_b: [None, (reading_comprehension_b.get_init_vals()['init width'], reading_comprehension_b.get_init_vals()['init height']), enlarge_appear, 10, False],
             reading_road_b: [None, (reading_road_b.get_init_vals()['init width'], reading_road_b.get_init_vals()['init height']), enlarge_appear, 10, False]}


    VOCAB_B_PRESS = {reading_vocab_mini_games_b: [None, (reading_vocab_mini_games_b.get_init_vals()['init width'], reading_vocab_mini_games_b.get_init_vals()['init height']), enlarge_appear, 5, False],
                     reading_vocab_practice_b: [None, (reading_vocab_practice_b.get_init_vals()['init width'], reading_vocab_practice_b.get_init_vals()['init height']), enlarge_appear, 5, False]}


    COMPREHENSION_B_PRESS = {reading_comprehension_stories_b: [None, (reading_comprehension_stories_b.get_init_vals()['init width'], reading_comprehension_stories_b.get_init_vals()['init height']), enlarge_appear, 5, False],
                             reading_comprehension_practice_b: [None, (reading_comprehension_practice_b.get_init_vals()['init width'], reading_comprehension_practice_b.get_init_vals()['init height']), enlarge_appear, 5, False]}

    

    ROAD_B_PRESS = {reading_road_recommendations_b: [None, (reading_road_recommendations_b.get_init_vals()['init width'], reading_road_recommendations_b.get_init_vals()['init height']), enlarge_appear, 5, False],
                    reading_road_progress_b: [None, (reading_road_progress_b.get_init_vals()['init width'], reading_road_progress_b.get_init_vals()['init height']), enlarge_appear, 5, False]}
    
 
    
    reading_b.set_on()
    reading_vocab_b.set_on()
    reading_comprehension_b.set_on()
    reading_road_b.set_on()
    reading_vocab_mini_games_b.set_on()
    reading_vocab_practice_b.set_on()
    reading_comprehension_stories_b.set_on()
    reading_comprehension_practice_b.set_on()
    reading_road_recommendations_b.set_on()
    reading_road_progress_b.set_on()
    
   

    reading_vocab_b.change_x(SCR1_SUBMENU_W / 2)
    reading_vocab_b.change_y(SCR1_SUBMENU_H / 2)
    reading_vocab_b.change_width(-SCR1_SUBMENU_W / 2)
    reading_vocab_b.change_height(-SCR1_SUBMENU_H / 2)
    
    reading_comprehension_b.change_x(SCR1_SUBMENU_W / 2)
    reading_comprehension_b.change_y(SCR1_SUBMENU_H / 2)
    reading_comprehension_b.change_width(-SCR1_SUBMENU_W / 2)
    reading_comprehension_b.change_height(-SCR1_SUBMENU_H / 2)
    
    reading_road_b.change_x(SCR1_SUBMENU_W / 2)
    reading_road_b.change_y(SCR1_SUBMENU_H / 2)
    reading_road_b.change_width(-SCR1_SUBMENU_W / 2)
    reading_road_b.change_height(-SCR1_SUBMENU_H / 2)

    


    reading_vocab_mini_games_b.change_x(SCR1_MINI_W / 2)
    reading_vocab_mini_games_b.change_y(SCR1_MINI_H / 2)
    reading_vocab_mini_games_b.change_width(-SCR1_MINI_W / 2)
    reading_vocab_mini_games_b.change_height(-SCR1_MINI_H / 2)
    reading_vocab_practice_b.change_x(SCR1_MINI_W / 2)
    reading_vocab_practice_b.change_y(SCR1_MINI_H / 2)
    reading_vocab_practice_b.change_width(-SCR1_MINI_W / 2)
    reading_vocab_practice_b.change_height(-SCR1_MINI_H / 2)
    
    reading_comprehension_stories_b.change_x(SCR1_MINI_W / 2)
    reading_comprehension_stories_b.change_y(SCR1_MINI_H / 2)
    reading_comprehension_stories_b.change_width(-SCR1_MINI_W / 2)
    reading_comprehension_stories_b.change_height(-SCR1_MINI_H / 2)
    reading_comprehension_practice_b.change_x(SCR1_MINI_W / 2)
    reading_comprehension_practice_b.change_y(SCR1_MINI_H / 2)
    reading_comprehension_practice_b.change_width(-SCR1_MINI_W / 2)
    reading_comprehension_practice_b.change_height(-SCR1_MINI_H / 2)
    
    reading_road_recommendations_b.change_x(SCR1_MINI_W / 2)
    reading_road_recommendations_b.change_y(SCR1_MINI_H / 2)
    reading_road_recommendations_b.change_width(-SCR1_MINI_W / 2)
    reading_road_recommendations_b.change_height(-SCR1_MINI_H / 2)
    reading_road_progress_b.change_x(SCR1_MINI_W / 2)
    reading_road_progress_b.change_y(SCR1_MINI_H / 2)
    reading_road_progress_b.change_width(-SCR1_MINI_W / 2)
    reading_road_progress_b.change_height(-SCR1_MINI_H / 2)
    
    simult_animations(READING_B_MOVE)
    reading_b.set_off()
    INTRO_SCREEN.draw_image(READING_TITLE, "READING_TITLE",  DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.15, 550, 120)
    
    simult_animations(SUB_ANIM)

    reading_vocab_mini_games_b.set_off()
    reading_vocab_practice_b.set_off()
    reading_comprehension_stories_b.set_off()
    reading_comprehension_practice_b.set_off()
    reading_road_recommendations_b.set_off()
    reading_road_progress_b.set_off()
    
    
    while READING_B_SCREEN.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closing()
                pygame.quit()
                sys.exit()

        
        READING_B_SCREEN.draw_img_buttons(None, [back, reading_b, reading_vocab_b, reading_comprehension_b, reading_road_b, reading_vocab_mini_games_b, reading_vocab_practice_b, reading_comprehension_stories_b, reading_comprehension_practice_b, reading_road_recommendations_b, reading_road_progress_b])
        
        if back.is_pressed():
            intro_screen_loop()
            
        
        elif reading_vocab_b.is_pressed() and not reading_vocab_mini_games_b.is_on():
            simult_animations(VOCAB_B_PRESS)
            reading_vocab_b.unanimated()

        elif reading_comprehension_b.is_pressed() and not reading_comprehension_stories_b.is_on():
            simult_animations(COMPREHENSION_B_PRESS)
            reading_comprehension_b.unanimated()
        
        elif reading_road_b.is_pressed() and not reading_road_progress_b.is_on():
            simult_animations(ROAD_B_PRESS)   
            reading_road_b.unanimated()
            
            
        pygame.display.update()






def writing_button_press_loop():
    WRITING_B_SCREEN.set_on()
    WRITING_B_SCREEN.set_background(background_writing)
    
    
    back = image_button_class.Image_Button('back_b' , back1, back2 , 100, 600, 50 , 50, WRITING_B_SCREEN.get_background_type(), WRITING_B_SCREEN.get_background_img(), WRITING_B_SCREEN.get_background_color())
    back.set_on()
    

   
        
    writing_b = image_button_class.Image_Button('writing' , writing_b_1, writing_b_2, 800, 250, SCR1_MENU_W, SCR1_MENU_H  , WRITING_B_SCREEN.get_background_type(), WRITING_B_SCREEN.get_background_img(), WRITING_B_SCREEN.get_background_color())

    
    writing_grammar_b = image_button_class.Image_Button('writing-Grammar' , grammar_b_1, grammar_b_2, 335, 175, SCR1_SUBMENU_W, SCR1_SUBMENU_H  , WRITING_B_SCREEN.get_background_type(), WRITING_B_SCREEN.get_background_img(), WRITING_B_SCREEN.get_background_color())


    writing_essay_b = image_button_class.Image_Button('writing-Essay' , essay_b_1, essay_b_2, 700, 175, SCR1_SUBMENU_W, SCR1_SUBMENU_H  , WRITING_B_SCREEN.get_background_type(), WRITING_B_SCREEN.get_background_img(), WRITING_B_SCREEN.get_background_color())


    writing_grammar_mini_games_b = image_button_class.Image_Button('writing-Grammar_MINI_GAMES' , writing_grammar_mini_games_1, writing_grammar_mini_games_2, 363, 260, SCR1_MINI_W, SCR1_MINI_H  , WRITING_B_SCREEN.get_background_type(), WRITING_B_SCREEN.get_background_img(), WRITING_B_SCREEN.get_background_color())

    writing_grammar_rhymes_b = image_button_class.Image_Button('writing-Grammar_RHYMES' , writing_grammar_rhymes_1, writing_grammar_rhymes_2, 363, 330, SCR1_MINI_W, SCR1_MINI_H  , WRITING_B_SCREEN.get_background_type(), WRITING_B_SCREEN.get_background_img(), WRITING_B_SCREEN.get_background_color())

    writing_essay_templates_b = image_button_class.Image_Button('writing-Essay_Templates' , writing_essay_templates_1, writing_essay_templates_2, 728, 260, SCR1_MINI_W, SCR1_MINI_H  , WRITING_B_SCREEN.get_background_type(), WRITING_B_SCREEN.get_background_img(), WRITING_B_SCREEN.get_background_color())

    writing_essay_tips_b = image_button_class.Image_Button('writing-Essay_Tips' , writing_essay_tips_1, writing_essay_tips_2, 728, 330, SCR1_MINI_W, SCR1_MINI_H  , WRITING_B_SCREEN.get_background_type(), WRITING_B_SCREEN.get_background_img(), WRITING_B_SCREEN.get_background_color())
    
  


    WRITING_B_MOVE = {writing_b: [0, center_to_topleft((DISPLAY_WIDTH / 2, 100), writing_b.get_width(), writing_b.get_height()), move, 10, False]}
    
    

    SUB_ANIM = {writing_grammar_b: [0, (writing_grammar_b.get_init_vals()['init width'], writing_grammar_b.get_init_vals()['init height']), enlarge_appear, 10, False],
             writing_essay_b: [0, (writing_essay_b.get_init_vals()['init width'], writing_essay_b.get_init_vals()['init height']), enlarge_appear, 10, False]}
   

    ESSAY_B_PRESS = {writing_essay_tips_b: [None, (writing_essay_tips_b.get_init_vals()['init width'], writing_essay_tips_b.get_init_vals()['init height']), enlarge_appear, 5, False],
                     writing_essay_templates_b: [None, (writing_essay_templates_b.get_init_vals()['init width'], writing_essay_templates_b.get_init_vals()['init height']), enlarge_appear, 5, False]}
    

    GRAMMAR_B_PRESS = {writing_grammar_mini_games_b: [None, (writing_grammar_mini_games_b.get_init_vals()['init width'], writing_grammar_mini_games_b.get_init_vals()['init height']), enlarge_appear, 5, False],
                     writing_grammar_rhymes_b: [None, (writing_grammar_rhymes_b.get_init_vals()['init width'], writing_grammar_rhymes_b.get_init_vals()['init height']), enlarge_appear, 5, False]}


  
    
    writing_b.set_on()
    writing_grammar_b.set_on()
    writing_essay_b.set_on()
    writing_grammar_mini_games_b.set_on()
    writing_grammar_rhymes_b.set_on()
    writing_essay_templates_b.set_on()
    writing_essay_tips_b.set_on()




    writing_grammar_b.change_x(SCR1_SUBMENU_W / 2)
    writing_grammar_b.change_y(SCR1_SUBMENU_H / 2)
    writing_grammar_b.change_width(-SCR1_SUBMENU_W / 2)
    writing_grammar_b.change_height(-SCR1_SUBMENU_H / 2)
    
    writing_essay_b.change_x(SCR1_SUBMENU_W / 2)
    writing_essay_b.change_y(SCR1_SUBMENU_H / 2)
    writing_essay_b.change_width(-SCR1_SUBMENU_W / 2)
    writing_essay_b.change_height(-SCR1_SUBMENU_H / 2)


    
    writing_grammar_mini_games_b.change_x(SCR1_MINI_W / 2)
    writing_grammar_mini_games_b.change_y(SCR1_MINI_H / 2)
    writing_grammar_mini_games_b.change_width(-SCR1_MINI_W / 2)
    writing_grammar_mini_games_b.change_height(-SCR1_MINI_H / 2)
    writing_grammar_rhymes_b.change_x(SCR1_MINI_W / 2)
    writing_grammar_rhymes_b.change_y(SCR1_MINI_H / 2)
    writing_grammar_rhymes_b.change_width(-SCR1_MINI_W / 2)
    writing_grammar_rhymes_b.change_height(-SCR1_MINI_H / 2)
    
    writing_essay_templates_b.change_x(SCR1_MINI_W / 2)
    writing_essay_templates_b.change_y(SCR1_MINI_H / 2)
    writing_essay_templates_b.change_width(-SCR1_MINI_W / 2)
    writing_essay_templates_b.change_height(-SCR1_MINI_H / 2)
    writing_essay_tips_b.change_x(SCR1_MINI_W / 2)
    writing_essay_tips_b.change_y(SCR1_MINI_H / 2)
    writing_essay_tips_b.change_width(-SCR1_MINI_W / 2)
    writing_essay_tips_b.change_height(-SCR1_MINI_H / 2)


    simult_animations(WRITING_B_MOVE)
    writing_b.set_off()
    INTRO_SCREEN.draw_image(WRITING_TITLE, "WRITING_TITLE",  DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.15, 550, 120)

    simult_animations(SUB_ANIM)


    writing_grammar_mini_games_b.set_off()
    writing_grammar_rhymes_b.set_off()
    writing_essay_templates_b.set_off()
    writing_essay_tips_b.set_off()
    
    
  
    
    while WRITING_B_SCREEN.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closing()
                pygame.quit()
                sys.exit()

        WRITING_B_SCREEN.draw_img_buttons(None, [back, writing_b, writing_grammar_b, writing_essay_b, writing_grammar_mini_games_b, writing_grammar_rhymes_b, writing_essay_templates_b, writing_essay_tips_b])
      

        
    
        if back.is_pressed():              
            intro_screen_loop()


        elif writing_grammar_b.is_pressed() and not writing_grammar_rhymes_b.is_on():
            simult_animations(GRAMMAR_B_PRESS)
            writing_grammar_b.unanimated()

        elif writing_essay_b.is_pressed() and not writing_essay_tips_b.is_on():
            simult_animations(ESSAY_B_PRESS)
            writing_essay_b.unanimated()                     
                                  
       
            
            
            
        pygame.display.update()
        
###############################
#SUB SCREENS

def math_ref_rules_scr1():
    MATH_REF_RULES_B_SCREEN_1.set_on()
    MATH_REF_RULES_B_SCREEN_1.set_background(background_math)
   
    
    back = image_button_class.Image_Button('back_b' , back1, back2 , 100, 600, 50 , 50, MATH_REF_RULES_B_SCREEN_1.get_background_type(), MATH_REF_RULES_B_SCREEN_1.get_background_img(), MATH_REF_RULES_B_SCREEN_1.get_background_color())
    back.set_on()

    forward = image_button_class.Image_Button('forward_b' , forward1, forward2 , 1150, 600, 50 , 50, MATH_REF_RULES_B_SCREEN_1.get_background_type(), MATH_REF_RULES_B_SCREEN_1.get_background_img(), MATH_REF_RULES_B_SCREEN_1.get_background_color())
    forward.set_on()


    while MATH_REF_RULES_B_SCREEN_1.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closing()
                pygame.quit()
                sys.exit()


        MATH_REF_RULES_B_SCREEN_1.draw_img_buttons(None, [back, forward])
        MATH_REF_RULES_B_SCREEN_1.draw_text("RULES&FORMULAS", "Title", BLACK, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.15, SCR1_TITLE_TEXT)       
        
        if back.is_pressed():
            math_button_press_loop()

        elif forward.is_pressed():
            math_ref_rules_scr2()
            
            
        
        pygame.display.update()

def math_ref_rules_scr2():
    MATH_REF_RULES_B_SCREEN_2.set_on()
    MATH_REF_RULES_B_SCREEN_2.set_background(background_math)
   
    
    
    back = image_button_class.Image_Button('back_b' , back1, back2 , 100, 600, 50 , 50, MATH_REF_RULES_B_SCREEN_2.get_background_type(), MATH_REF_RULES_B_SCREEN_2.get_background_img(), MATH_REF_RULES_B_SCREEN_2.get_background_color())
    back.set_on()

    forward = image_button_class.Image_Button('forward_b' , forward1, forward2 , 1150, 600, 50 , 50, MATH_REF_RULES_B_SCREEN_2.get_background_type(), MATH_REF_RULES_B_SCREEN_2.get_background_img(), MATH_REF_RULES_B_SCREEN_2.get_background_color())
    forward.set_on()


    while MATH_REF_RULES_B_SCREEN_2.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                closing()
                pygame.quit()
                sys.exit()


        MATH_REF_RULES_B_SCREEN_2.draw_img_buttons(None, [back, forward])
        #MATH_B_SCREEN.draw_text("RULES&FORMULAS", "Title", BLACK, DISPLAY_WIDTH / 2, DISPLAY_HEIGHT * 0.15, SCR1_TITLE_TEXT)       
        
        if back.is_pressed():
            math_ref_rules_scr1()
            
            
        
        pygame.display.update()

    
    
#def math_ref_sample_questions_scr1():

#def math_ref_resources_scr1():

#def math_practice_mini_games_scr1():

#def math_practice_timed_questions_scr1():

#def math_practice_resources_scr1():


##############

#def reading_vocab_mini_games_scr1():

#def reading_vocab_practice_scr1():

#def reading_comprehension_stories_scr1():

#def reading_comprehension_practice_scr1():

#def reading_road_recommendations_scr1():

#def reading_road_progress_scr1():

################

#def writing_grammar_mini_games_scr1():

#def writing_grammar_rhymes_scr1():

#def writing_essay_templates_scr1():

#def writing_essay_tips_scr1():


    





















        

###########################################
#Opening and Closing Transitions
def opening():
    OPENING_SCREEN.set_on()
    OPENING_SCREEN.set_background(background_opening)

    while OPENING_SCREEN.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
        pygame.display.update()
        CLOCK.tick(0.5)
        OPENING_SCREEN.set_off()



def closing():
    CLOSING_SCREEN.set_on()
    CLOSING_SCREEN.set_background(background_closing)

    while CLOSING_SCREEN.is_running():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
        pygame.display.update()
        CLOCK.tick(0.3)
        CLOSING_SCREEN.set_off()
    
       
    
opening()
intro_screen_loop()






            
