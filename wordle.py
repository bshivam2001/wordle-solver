'''
Usage:  1. Run the function getNextSuggestion() to get a word suggestion based on
            the current state of the game
        2. Run updatePositions(word, correctness_input) after each call to getNextSuggestion()
            This updates the positions lists to suggest better words in the next call to getNextSuggestion()
'''

import random
from queue import PriorityQueue

# Input wordlist file
__WORDLIST_FILE__ = 'possible.txt'

# Enter a word to start with, random word is selected if this is empty
__INITIAL_SUGGESTION__ = ''

# Variables
suggestion = __INITIAL_SUGGESTION__             # Holds the current suggestion
wordlist = []                                   # Holds all possible 5 letter words
included = set()                                # Holds letters that are yellow
positions = {}                                  # Holds letters that are green along with their positions
pos_not = [[] for i in range(5)]                # Holds letters that CANNOT be at ith position
tried = []                                      # Holds words that have already been tried
excluded = set()                                # Holds letters that are NOT part of the solution word

# Function to check if a given word is possible or not and gives it a score
def getScore(word):
    score = 0

    if word in tried:
        return -1

    for i in included:
        if i not in word:
            return -1

    for i in range(5):
        if i in positions.keys() and word[i] != positions[i]:
            return -1
        elif word[i] in excluded:
            return -1
        elif word[i] in pos_not[i]:
            return -1
        elif word[i] in included:
            score += 1
        
    # Reduce score if newly guessed letters are being repeated
    # in order to attempt to try maximum number of different letters with every guess
    known = len(included) + len(positions.keys())   # Number of letters that are known
    if len(set(word))-known < 5-known:
        score = max(0, score-1)
    return score
        

# Function to reset game state
def reset():
    global suggestion, included, positions, pos_not, tried, excluded
    suggestion = ''
    included = set()
    positions = {}
    pos_not = [[] for i in range(5)]
    tried = []
    excluded = set()  


'''
Function to update the positions lists given the word and the correctness
Args:   word: the word you tried
        correctness_input: input for whether each letter was
              green, yellow or grey in the wordle game
'''
def updatePositions(word, correctness_input):
    for i in range(len(correctness_input)):
        if correctness_input[i] == 'g':
            positions[i] = word[i]
            if correctness_input[i] in included:
                included.remove(correctness_input[i])
        elif correctness_input[i] == 'y':
            included.add(word[i])
            pos_not[i].append(word[i])
        elif correctness_input[i] == 'n':
            pos_not[i].append(word[i])
            if word[i] not in included and word[i] not in positions.values():
                excluded.add(word[i])


# Function to get the next word suggestion
def getNextSuggestion():
    global suggestion
    # Special case if the first word is being suggested, for maximum success it must:
    # 1. Have all unique letters
    # 2. Not include rarely used letters
    if suggestion == '':
        # These letters occur less than 50 times in over 2000 words
        exclude_letters = ['q', 'x', 'j', 'z']
        while len(set(suggestion)) < 5 or any(x in suggestion for x in exclude_letters):
            suggestion = random.choice(wordlist)
            
        return suggestion

    possible = PriorityQueue()
    for word in wordlist:
        word_score = getScore(word)

        if len(included) == 0:
            word_set = set(list(word))
            if len(word_set) < 5:
                continue

        if word_score >= 0 and word_score < 5:
            possible.put((5-word_score, word))
    if possible.empty():
        '''
        #DEBUG - print statements
        print(positions)
        print(included)
        print(excluded)
        print(pos_not)
        '''
        return '-1'  #Error: invalid state
        
    suggestion = possible.get()[1]
    tried.append(suggestion)
    return suggestion

try:
    with open(__WORDLIST_FILE__) as file:
        wordlist = file.read().splitlines()
except FileNotFoundError:
    print(f'FATAL ERROR: Could not find file \'{__WORDLIST_FILE__}\'')

# Command line version: Run this file directly to skip the UI
if __name__ == '__main__':
    # Initialize number of guesses
    guesses = 6
    # Loop 6 times
    while guesses > 0:
        # Get a suggestion from the wordlist
        suggestion = getNextSuggestion()
        '''
        If getNextSuggestion() returns -1, the game is in an invalid state
        either because the word is not present in the wordlist
        or because the user made an error while entering the correctness
        '''
        if suggestion == '-1':
            print('FATAL ERROR: Invalid State')
            break

        # Print the suggestion and get the correctness from the user
        print('\nTry:', suggestion.upper())
        correctness = ''
        while len(correctness) < 5:
            print('Enter correctness of each letter:')
            correctness = input('[(g)reen, (y)ellow, (n)one]: ')
            correctness = correctness.replace(' ', '')
        
        # Analyze the positions of letters in the word to make a better guess next time
        updatePositions(suggestion, correctness)
        
        # If all letters are 'g' then the game has ended
        if correctness.count('g') == 5:
            print('\nFound the word:', suggestion)
            break

        # Reduce the number of available guesses
        guesses -= 1