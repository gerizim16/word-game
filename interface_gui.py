#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Word Game!\n
Contains main game with GUI
"""
# built-ins
from string import ascii_letters, digits, punctuation
from random import choices as random_choices
from textwrap import wrap as wrap_text
# third-party
import pygame
# own module
import engine

# constants
WIDTH = 1024
HEIGHT = 768-60
TIME_LIMIT_SET = 60 # seconds
ACCEPTED = ascii_letters+digits+punctuation+" " # accepted user input
COLOR_BACKGROUND = (167, 65, 74) # maroon
COLOR_FONT_BG = (19, 34, 38) # near black
COLOR_ACCENT = (49, 172, 171) # light green-blue
COLOR_FONT = (242, 234, 237) # near white
LIVES = 3
SAVE_FILENAME = '.save_gui'

# initialize pygame
pygame.init()
pygame.display.set_caption('Word Game!')
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
SCREEN.fill(COLOR_BACKGROUND)
FONT_SIZE = 36
FONT_1 = pygame.font.SysFont('Helvetica', FONT_SIZE)
FONT_1_HEIGHT = FONT_1.size('')[1]

def clear_game_area(bgcolor=COLOR_BACKGROUND):
    """clears game area"""
    pygame.draw.rect(SCREEN, bgcolor,\
        (15, 30+FONT_1_HEIGHT, WIDTH-30, HEIGHT-(60+2*FONT_1_HEIGHT)))

def showstatus(phrase, mode=0):
    """str(phrase), int(mode) --> showstatus(phrase, mode=0)
    Shows phrase on GUI header(mode=0)[default] or footer(mode=1)
    """
    phrase = str(phrase)
    textdisp = FONT_1.render(phrase, True, COLOR_FONT)
    # position based on mode
    if mode == 0:
        position = (15, 15)
    elif mode == 1:
        position = (15, HEIGHT-(FONT_1_HEIGHT+15))
    # draw to screen
    pygame.draw.rect(SCREEN, COLOR_FONT_BG, position + (WIDTH-30, FONT_1_HEIGHT))
    SCREEN.blit(textdisp, (position[0]+6, position[1]))

def show_line(phrase, height):
    """Shows a line in screen in height specified"""
    display_text = FONT_1.render(phrase, True, COLOR_FONT)
    text_size = FONT_1.size(phrase)
    position = ((WIDTH-text_size[0])//2, height)
    pygame.draw.rect(SCREEN, COLOR_FONT_BG,\
                     (15, position[1]) + (WIDTH-30, text_size[1]))
    SCREEN.blit(display_text, position)

def show_answers(answer_list):
    """Shows answers in the GUI"""
    answers = ' | '.join(answer_list)
    answers = wrap_text(answers, 81)
    answer_font = pygame.font.SysFont('Helvetica', FONT_SIZE-4)
    answer_font_height = answer_font.size('')[1]
    height = 15 + 66 + 3*FONT_1_HEIGHT
    for answer in answers:
        display_text = answer_font.render(answer, True, COLOR_FONT)
        text_size = answer_font.size(answer)
        position = (30, height)
        pygame.draw.rect(SCREEN, COLOR_FONT_BG, position + text_size)
        SCREEN.blit(display_text, position)
        height += answer_font_height + 6

def update_lives(lives):
    """Updates lives GUI"""
    font = pygame.font.SysFont('Helvetica', FONT_SIZE + 34)
    lives = lives*chr(9829)
    display_text = font.render(lives, True, COLOR_BACKGROUND)
    text_size = font.size(lives + chr(9829))
    position = (30, FONT_1_HEIGHT + 48)
    pygame.draw.rect(SCREEN, COLOR_ACCENT, (position[0]-6, \
                     position[1]-6) + (text_size[0] + 12, text_size[1]+12))
    SCREEN.blit(display_text, (position[0], position[1]-25))

def update_time(msec):
    """Updates time GUI"""
    msec = 'Time left: ' + str(msec) + ' s'
    display_text = FONT_1.render(msec, True, COLOR_FONT_BG)
    text_size = FONT_1.size(msec)
    position = ((WIDTH-text_size[0])//2, FONT_1_HEIGHT + 48)
    pygame.draw.rect(SCREEN, COLOR_ACCENT, (position[0]-6, \
                     position[1]-6) + (text_size[0] + 12, text_size[1]+12))
    SCREEN.blit(display_text, position)

def update_score(score):
    """Updates score GUI"""
    score = 'Score: ' + str(score)
    display_text = FONT_1.render(score, True, COLOR_FONT_BG)
    text_size = FONT_1.size(score)
    position = (WIDTH - text_size[0] - 30, FONT_1_HEIGHT + 48)
    pygame.draw.rect(SCREEN, COLOR_ACCENT, (position[0]-6, \
                     position[1]-6) + (text_size[0] + 12, text_size[1]+12))
    SCREEN.blit(display_text, position)

def get_strinput(max_chars=-1):
    """Gets long user input and returns it as string"""
    holder = []
    # main loop
    getting_strinput = True
    while getting_strinput:
        # get keypresses
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    # done case: clear bottom status then return string
                    showstatus('', 1)
                    pygame.display.flip()
                    return ''.join(holder)
                elif event.key == pygame.K_BACKSPACE:
                    if holder:
                        holder = holder[:-1]
                # append as long as in accepted input
                elif event.unicode in ACCEPTED and len(holder) != max_chars:
                    holder.append(event.unicode)
                elif event.type == pygame.QUIT or \
                     (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return None # quit game

                # update/show input at bottom.
                showstatus(''.join(holder), 1)
                pygame.display.flip()

def select_dictionary():
    """GUI dictionary selection"""
    showstatus('Enter dictionary filename! (or press enter to use default)')
    showstatus('', 1)
    pygame.display.flip()
    while True:
        user_input = get_strinput()
        if user_input == '':
            user_input = 'dictionary.txt'
        elif user_input is None:
            pygame.quit()
            return
        try:
            engine.set_dictionary(tuple(engine.open_dictionary(user_input)))
        except FileNotFoundError:
            showstatus('File not found!')
            pygame.display.flip()
        except TypeError:
            return
        else:
            break

def menu(*menu_names):
    """Creates 2D menu screen accepting menu names with format\n
    menu((main_menu,), (sub_menu, sub_menu,...), (main_menu,)...)\n
    note that a main menu must still be a tuple by itself.\n
    returns selected menu into a [main menu index, sub menu index]\n
    sub menu index is 0 when there is no sub menu as by example in first choice in example menu\n
    """
    # constants
    rows = len(menu_names)
    gap = 15
    button_height = FONT_1_HEIGHT + 6
    menu_heigth = (button_height + gap)*rows
    menu_width = 350
    height_list = [i for i in range(0, rows*(button_height+gap), button_height+gap)]

    # initialize draw
    menu_surface = pygame.Surface((menu_width, menu_heigth))
    # keying color
    menu_surface.fill((1, 1, 1))
    menu_surface.set_colorkey((1, 1, 1))
    # initial draw for buttons and button names
    for row_index, row_names in enumerate(menu_names):
        for col_index, button_name in enumerate(row_names):
            # button_width of a row is dependent on amount of buttons in a row
            button_width = menu_width if len(row_names) == 1 else\
                           (menu_width - gap*(len(row_names)-1))//len(row_names)
            dimensions = ((button_width+gap)*col_index, height_list[row_index], \
                          button_width, button_height)
            menu_button(button_name, True if row_index == 0 and col_index == 0 else False, \
                        dimensions, menu_surface)
    SCREEN.blit(menu_surface, ((WIDTH-menu_width)/2, (HEIGHT-menu_heigth)/2))
    pygame.display.flip()

    # menu loop
    selected = [0, 0]
    new_selected = [0, 0]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    new_selected[0] = (selected[0] - 1) % rows
                    new_selected[1] = 0
                elif event.key == pygame.K_DOWN:
                    new_selected[0] = (selected[0] + 1) % rows
                    new_selected[1] = 0
                elif event.key == pygame.K_LEFT:
                    new_selected[1] = (selected[1] - 1) % (len(menu_names[selected[0]]))
                elif event.key == pygame.K_RIGHT:
                    new_selected[1] = (selected[1] + 1) % (len(menu_names[selected[0]]))
                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return selected
                elif event.type == pygame.QUIT or \
                     (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    return [-1, -1]
                # if a new menu button is selected,
                if selected != new_selected:
                    # redraw past selected button to normal state
                    cols = menu_names[selected[0]]
                    button_width = menu_width if len(cols) == 1\
                                   else (menu_width - gap*(len(cols)-1))//len(cols)
                    dimensions = ((button_width+gap)*selected[1], height_list[selected[0]], \
                                  button_width, button_height)
                    menu_button(cols[selected[1]], False,\
                                dimensions, menu_surface)
                    # redraw new selected button to selected state
                    cols = menu_names[new_selected[0]]
                    button_width = menu_width if len(cols) == 1\
                                   else (menu_width - gap*(len(cols)-1))//len(cols)
                    dimensions = ((button_width+gap)*new_selected[1], height_list[new_selected[0]],\
                                  button_width, button_height)
                    menu_button(cols[new_selected[1]], True,\
                                dimensions, menu_surface)
                    SCREEN.blit(menu_surface, ((WIDTH-menu_width)//2, (HEIGHT-menu_heigth)//2))
                    selected = new_selected.copy()
                pygame.display.flip()

def menu_button(name, mode, rect, msurface):
    """Not used by itself, helper function for menu function
    name = button name
    mode = highlighted if True, normal if False (default)
    rect = button position and dimensions
    msurface = surface where the button will be drawn
    """
    pygame.draw.rect(msurface, COLOR_FONT if mode else COLOR_FONT_BG, rect)
    text = FONT_1.render(name, True, COLOR_FONT if not mode else COLOR_FONT_BG)
    size = FONT_1.size(name)
    msurface.blit(text, (rect[0] + (rect[2]-size[0])//2, rect[1] + (rect[3]-size[1])//2))

def game1(time_limit):
    """"Anagram game: Find all anagrams of a random word\n
    before running out of lives or time. Score is computed by getting\n
    the number of correct anagrams found.
    """
    showstatus('Find all the possible anagrams!')
    # variables
    lives = LIVES
    score = 0
    base_anagram, anagrams = engine.get_anagram_set(2) # get given and answers
    total_score = len(anagrams) # get highest score attainable
    answers = [] # list of correct answers found
    letter_bank = [str(letter) for letter in base_anagram] # available letters to be used
    holder = [] # letters used
    typing = True
    # initial draw
    update_score(score)
    update_lives(lives)
    show_line(' '.join(letter_bank), 66 + 2*FONT_1_HEIGHT) # draws given
    show_line('', HEIGHT - (2*FONT_1_HEIGHT + 45)) # draws currently typing answer
    # initialize timer event
    sec = time_limit
    if time_limit > 0:
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        update_time(sec)
    pygame.display.flip()
    # main game loop
    while lives and score != total_score and sec != 0:
        if typing:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT: # clock tick
                    sec -= 1
                    update_time(sec)
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if letter_bank:
                            showstatus('Use all the letters!')
                        else: # exit from typing
                            typing = False
                    elif event.key == pygame.K_BACKSPACE:
                        if holder:
                            letter_bank.append(holder[-1])
                            holder = holder[:-1]
                    elif event.unicode.lower() in letter_bank:
                        letter = event.unicode.lower()
                        holder.append(letter)
                        letter_bank.remove(letter)
                    elif event.type == pygame.QUIT or \
                         (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        lives = 0

                    show_line(' '.join(letter_bank), 66 + 2*FONT_1_HEIGHT) # draws given
                    # draws currently typing answer
                    show_line(' '.join(holder), HEIGHT - (2*FONT_1_HEIGHT + 45))
        else: # if not typing
            answer = ''.join(holder)
            if answer in anagrams: # if correct
                score += 1
                anagrams.remove(answer)
                answers.append(answer)
                show_answers(answers)
                update_score(score)
                showstatus('Correct!')
            elif answer == base_anagram: # if answered the given word
                showstatus("That's the original word!")
            elif answer in answers:
                showstatus("Already answered!")
            else: # if wrong
                lives -= 1
                update_lives(lives)
                showstatus('Not in dictionary!')
            # reinitialize
            typing = True
            holder = []
            letter_bank = [str(letter) for letter in base_anagram]
            show_line(' '.join(letter_bank), 66 + 2*FONT_1_HEIGHT)
            show_line('', HEIGHT - (2*FONT_1_HEIGHT + 45))
        pygame.display.flip()
    # game conclusion
    show_answers(answers + ['-='*40+'-', 'Other answers:'] + anagrams) # show answers/other answers
    pygame.time.set_timer(pygame.USEREVENT, 0) # stops timer event
    # high score handling
    hname, hscore = engine.get_highscore(1 if time_limit == -1 else 0, SAVE_FILENAME)
    if score > hscore:
        showstatus('You got {} points!'.format(score))
        showstatus('Enter your name: ', 1)
        pygame.display.flip()
        name = get_strinput(9)
        showstatus('New highscore is {} points!'.format(score), 1)
        engine.set_highscore(name, score, 1 if time_limit == -1 else 0, SAVE_FILENAME)
    else:
        showstatus('The highscore is {} by {}'.format(hscore, hname), 1)
    # wait for enter before exit
    showstatus('You got {} points! (press enter to continue)'.format(score))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return

def game2(time_limit):
    """Construct words: Form words using letters generated by combining 2 random words\n
    before running out of lives or time. Score is computed by getting\n
    the scrabble points of each correct answer.
    """
    showstatus('Form words using these letters!')
    # variables
    lives = LIVES
    score = 0
    base_chars = engine.combine_words(random_choices(engine.DICTIONARY, k=2)) # given
    at_least = 3 # minimum letters to be considered a word
    answers = [] # correct answers made
    letter_bank = [str(letter) for letter in base_chars] # letters available to be used
    holder = [] # letters used
    typing = True
    # initial draw
    update_score(score)
    update_lives(lives)
    show_line(' '.join(letter_bank), 66 + 2*FONT_1_HEIGHT) # draws given
    show_line('', HEIGHT - (2*FONT_1_HEIGHT + 45)) # draws currently typing answer
    # initialize timer event
    sec = time_limit
    if time_limit > 0:
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        update_time(sec)
    pygame.display.flip()
    # main game loop
    while lives and sec != 0:
        if typing:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT: # clock tick
                    sec -= 1
                    update_time(sec)
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if len(holder) >= at_least: # exit from typing
                            typing = False
                        else:
                            showstatus('Enter at least {} letters!'.format(at_least))
                    elif event.key == pygame.K_BACKSPACE:
                        if holder:
                            letter_bank.append(holder[-1])
                            holder = holder[:-1]
                    elif event.unicode.lower() in letter_bank:
                        letter = event.unicode.lower()
                        holder.append(letter)
                        letter_bank.remove(letter)
                    elif event.type == pygame.QUIT or \
                         (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                        lives = 0

                    show_line(' '.join(letter_bank), 66 + 2*FONT_1_HEIGHT) # draws given
                    # draws currently typing answer
                    show_line(' '.join(holder), HEIGHT - (2*FONT_1_HEIGHT + 45))
        else: # if not typing
            answer = ''.join(holder)
            if answer in engine.DICTIONARY: # if correct
                if answer not in answers: # if not yet answered before
                    score += engine.get_score(answer)
                    answers.append(answer)
                    show_answers(answers)
                    update_score(score)
                    showstatus('Correct!')
                else: # if already answered
                    showstatus('Already answered!')
            else: # if not in dictionary
                lives -= 1
                update_lives(lives)
                showstatus('Not in dictionary!')
            # reinitialize
            typing = True
            holder = []
            letter_bank = [str(letter) for letter in base_chars]
            show_line(' '.join(letter_bank), 66 + 2*FONT_1_HEIGHT)
            show_line(' '.join(holder), HEIGHT - (2*FONT_1_HEIGHT + 45))
        pygame.display.flip()
    # game conclusion
    pygame.time.set_timer(pygame.USEREVENT, 0) # stops timer event
    # high score handling
    hname, hscore = engine.get_highscore(3 if time_limit == -1 else 2, SAVE_FILENAME)
    if score > hscore:
        showstatus('You got {} points!'.format(score))
        showstatus('Enter your name: ', 1)
        pygame.display.flip()
        name = get_strinput(9)
        showstatus('New highscore is {} points!'.format(score), 1)
        engine.set_highscore(name, score, 3 if time_limit == -1 else 2, SAVE_FILENAME)
    else:
        showstatus('The highscore is {} by {}'.format(hscore, hname), 1)
    # wait for enter before exit
    showstatus('You got {} points! (press enter to continue)'.format(score))
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    return

def run():
    """Main function to run the game\n
    Shows the structure of the whole game
    """
    # initialize constant
    time_limit = TIME_LIMIT_SET

    # select dictionary
    select_dictionary()

    # main loop
    while True:
        clear_game_area()
        showstatus('Menu: Select a game mode.')
        # show highscore of game mode (timed or untimed)
        if time_limit != -1:
            scores = engine.get_highscore(0, SAVE_FILENAME) + engine.get_highscore(2, SAVE_FILENAME)
            time_mode = 'Timed'
        else:
            scores = engine.get_highscore(1, SAVE_FILENAME) + engine.get_highscore(3, SAVE_FILENAME)
            time_mode = 'Untimed'
        showstatus('{0} | Anagrams: {1} with {2} {5} - Words: {3} with {4} {6}'.format(\
                   time_mode, *scores, 'pts' if scores[1] > 1 else 'pt',               \
                   'pts' if scores[3] > 1 else 'pt'), 1)
        pygame.display.flip()

        # get user input from menu
        main_menu, sub_menu =                                                          \
            menu(('Find Anagrams!',), ('Construct Words!',), ('Timer On', 'Timer Off'),\
                 ('Change Dictionary',), ('Exit',))

        # checks user option
        if main_menu == 4 or main_menu == -1:
            break # exit case
        elif main_menu == 0:
            clear_game_area(COLOR_ACCENT)
            game1(time_limit) # anagram game
        elif main_menu == 1:
            clear_game_area(COLOR_ACCENT)
            game2(time_limit) # words game
        elif main_menu == 2:
            # time limit setting
            if sub_menu == 0:
                time_limit = TIME_LIMIT_SET
            elif sub_menu == 1:
                time_limit = -1
        elif main_menu == 3:
            select_dictionary()

    # free resources
    pygame.quit()

if __name__ == '__main__':
    run()
