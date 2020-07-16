#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Word Game! game logic\n
Contains game logic and the dictionary variable that the functions are dependent to
"""
from random import choice as random_choice

SCRABBLE = {'e':1, 'a':1, 'i':1, 'o':1, 'n':1, 'r':1, 't':1, 'l':1, 's':1, 'u':1,
            'd':2, 'g':2,
            'b':3, 'c':3, 'm':3, 'p':3,
            'f':4, 'h':4, 'v':4, 'w':4, 'y':4,
            'k':5,
            'j':8, 'x':8,
            'q':10, 'z':10}
DICTIONARY = ()

def set_dictionary(buffer):
    """Sets the global DICTIONARY variable"""
    global DICTIONARY
    DICTIONARY = tuple(buffer)

def open_dictionary(filename):
    """Accepts a filename, Returns a tuple of words"""
    with open(filename, 'r') as textfile:
        buffer = tuple(textfile.read().splitlines())
    return buffer

def get_score(word):
    """word -> get_score(word) -> integer scrabble score"""
    word = word.lower()
    sums = 0
    for letter in word:
        sums += SCRABBLE[letter]
    return sums

def count_letters(word):
    """word -> count_letters(word) -> dict of letter: letter_count\n
    Note: letters are all treated as lowercase and returns in lowercase
    """
    word = word.lower()
    letters_counts = {} # letter: count
    for letter in word:
        if letter in letters_counts:
            letters_counts[letter] += 1
        else:
            letters_counts[letter] = 1
    return letters_counts

def makeable(chars, word):
    """characters, word -> makeable(characters, word)\n
    Returns True if word is makeable using letters in chars else False
    Note: letters are all treated as lowercase and returns in lowercase
    """
    chars, word = chars.lower(), word.lower()
    letter_intersect = set(chars) & set(word)
    if len(letter_intersect) == len(set(word)):
        chars_letter_count = count_letters(chars)
        word_letter_count = count_letters(word)
        for letter in letter_intersect:
            if word_letter_count[letter] > chars_letter_count[letter]:
                return False
        return True
    return False

def combine_words(words):
    """Accepts list of words and returns a single string where all words can be made\n
    String letters are arranged in alphabetical order
    Note: letters are all treated as lowercase and returns in lowercase
    """
    letters_max = count_letters(words[0])
    for word in words[1:]:
        letters_candidate = count_letters(word)
        letters_max = {key:max(letters_max.get(key, 0), letters_candidate.get(key, 0)) for\
                       key in set(letters_max.keys()) | set(letters_candidate.keys())}
    return ''.join(''.join(key for _ in range(value)) for \
                    key, value in sorted(tuple(letters_max.items()), key=lambda item: item[0]))

def possible_words(chars):
    """Accepts a string and returns all words that may be made by that string in a list"""
    words = []
    for word in DICTIONARY:
        if makeable(chars, word):
            words.append(word)
    return words

def find_anagrams(base_word):
    """Accepts a word and returns all of its anagrams in a list"""
    words = []
    for word in DICTIONARY:
        if len(base_word) == len(word):
            if count_letters(base_word) == count_letters(word):
                words.append(word)
    words.remove(base_word)
    return words

def get_anagram_set(at_least=1):
    """Special function that returns a random base word and all of its anagrams\n
    Returns with syntax (base_word, anagrams)\n
    Base word is not included in anagrams
    """
    while True:
        base_word = random_choice(DICTIONARY)
        anagrams = find_anagrams(base_word)
        if len(anagrams) >= at_least:
            break
    return base_word, anagrams

def get_highscore(mode, filename):
    """mode, filename -> get_highscore(mode, filename)\n
    Returns high score from game mode tuple(name, score)
    """
    try:
        with open(filename, 'r') as save:
            contents = save.read().split('\n')
    except FileNotFoundError:
        contents = ['0' if i % 2 else 'None' for i in range(mode*2+2)]
    try:
        name, score = contents[2*mode], contents[2*mode+1]
    except IndexError:
        name, score = None, 0
    return name, int(score)

def set_highscore(name, score, row, filename):
    """name, score, row, filename -> set_highscore(name, score, row, filename)\n
    Sets high score with name in the first sub row in the specified main row and\n
    score on the second sub row in the specified main row
    """
    try:
        with open(filename, 'r') as save:
            contents = save.read().split('\n')
    except FileNotFoundError:
        contents = ['0' if i % 2 else 'None' for i in range(row*2+2)]

    while True:
        try:
            contents[2*row], contents[2*row+1] = name, str(score)
        except IndexError:
            contents.extend([None, 0])
        else:
            break

    contents = '\n'.join(contents)
    with open(filename, 'w') as save:
        save.write(contents)

def main():
    print("This is a module used by 'Word Game!' game.")
    print('It contains all of its game logic')
    input('Press anything to continue...')

if __name__ == '__main__':
    main()
