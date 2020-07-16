#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Word Game!\n
Contains main game interface
"""
from random import choices as random_choices
import engine

# constants
SET_LIVES = 3
SAVE_FILENAME = '.save_terminal'
MODES = ['Find Anagrams!', 'Construct Words!', 'Change Dictionary']

def select_dictionary():
    """Terminal dictionary selection"""
    while True:
        dictionary_fname = input('Enter dictionary filename: (or press enter for default) ')
        if not dictionary_fname:
            dictionary_fname = 'dictionary.txt'
        try:
            engine.set_dictionary(engine.open_dictionary(dictionary_fname))
        except FileNotFoundError:
            print('File not found!')
        else:
            break

def game1():
    """Game mode 1: Find Anagrams!: Find all anagrams of a random word\n
    before running out of lives or time. Score is computed by getting\n
    the number of correct anagrams found.
    """
    print('You chose {}'.format(MODES[0]))

    # constants
    # get base_anagram and its anagrams with at least two answers
    base_anagram, anagrams = engine.get_anagram_set(2)
    # get letter count of base_anagram since it will be used often in the loop
    base_letter_count = engine.count_letters(base_anagram)

    # variables
    lives = SET_LIVES
    score = 0
    right_ans = []

    print('Find the anagrams of:')
    # game main loop
    while lives and anagrams: # while there are remaining lives and answers
        print('==' + base_anagram + '==')
        answer = input()
        if engine.count_letters(answer) == base_letter_count: # checks if answer is valid
            if answer not in right_ans: # check if answer was already answered
                if answer in anagrams: # check if it is an anagram
                    right_ans.append(answer)
                    anagrams.remove(answer)
                    score += 1
                    print('Score {}'.format(score))
                elif answer == base_anagram:
                    print('This is the base word.')
                else:
                    lives -= 1
                    print('Not in dictionary! Lives: {}'.format(lives))
            else:
                print('Already answered!')
        else:
            print('Not a valid answer!')
    # game1 conclusion
    if anagrams: # check if there are remaining answers
        if score: # if player scored at least one, print other answers
            print('Other answers are: ', end='')
            for word in anagrams:
                if word not in right_ans:
                    print(word, end=' ')
        else:
            print('Answers are: ', end='')
            for word in anagrams:
                print(word, end=' ')
        print()
    return score

def game2():
    """Game mode 2: Construct Words!: Form words using letters generated\n
    by combining 2 random words before running out of lives or time.\n
    Score is computed by getting the scrabble points of each correct answer.
    """
    print('You chose {}'.format(MODES[1]))

    # constant
    # get characters that the user may use, created by combining 2 random words
    chars = engine.combine_words(random_choices(engine.DICTIONARY, k=2))

    # variables
    lives = SET_LIVES
    score = 0
    right_ans = []

    print('Enter words using these letters:')
    # game main loop
    while lives:
        print('==' + chars + '==')
        answer = input()
        # only accept at least 3 letter words and check if valid answer
        if engine.makeable(chars, answer) and len(answer) >= 3:
            if answer not in right_ans: # check if answer was already answered
                if answer in engine.DICTIONARY: # check if answer is correct
                    right_ans.append(answer)
                    score += engine.get_score(answer) # get scrabble points
                    print('Score: {}'.format(score))
                else:
                    lives -= 1
                    print('Not in dictionary! Lives: {}'.format(lives))
            else:
                print('Already answered!')
        else:
            print('Invalid answer!')
    return score

def run():
    """Main function that runs the game"""
    # get dictionary
    select_dictionary()

    # main loop
    running = True
    while running:
        # menu
        print('='*10)
        print('Enter game mode! High scores are:')
        print('Anagrams: {} with {} | Words: {} with {}'.format(\
              *(engine.get_highscore(0, SAVE_FILENAME)) +       \
                engine.get_highscore(1, SAVE_FILENAME)))
        for i, game_mode_name in enumerate(MODES, 1):
            print('{}. {}'.format(i, game_mode_name))
        print('0. Exit')

        mode = input()
        if mode in ('1', '2'):
            # game start
            if mode == '1':
                score = game1()
            elif mode == '2':
                score = game2()
            # game conclusion
            name, current_high_score = engine.get_highscore(int(mode)-1, SAVE_FILENAME)
            print('='*10)
            if score > current_high_score:
                print('New high score! You got {} points!'.format(score))
                name = input('Enter your name:')
                engine.set_highscore(name, score, int(mode)-1, SAVE_FILENAME)
            else:
                print('You got {} points!'.format(score))
                print('The high score is {} by {}'.format(current_high_score, name))
        elif mode == '3':
            select_dictionary()
        elif mode == '0':
            # end case
            running = False
        else:
            print('Invalid!')

if __name__ == '__main__':
    run()
