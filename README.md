# Wordle Solver
Suggest words to solve the popular word game 'Wordle'

- Suggests words based on previous guesses
- Can run in GUI based mode or command line
- Update win-loss statistics after every run to update success rates

## Requirements
- Python 3.xx

## Usage
1. Run the program in python
    - Run `solver-gui.py` for the GUI version, or
    - Run `wordle.py` for the command line version
2. Enter the *correctness* input after each suggestion
    - Enter *'g'* for green, *'y'* for yellow or *'n'* for none, corresponding to the feedback the Wordle app gives
    - Press enter after giving inputs for all five letters to get a new suggession based on your inputs
3. Press `Esc` key to reset the game state in the GUI version

- To disable statistics, set the `ENABLE_STATS` variable to `False` in `solver-gui.py`
- If you would like the program to start from a particular word, set the `__INITIAL_SUGGESTION__` variable to a 5 letter word in `wordle.py`

## Screenshots
![Game Start State](./images/game_start.png "Game Start State")
![Game Win State](./images/game_end.png "Game Win State")

## Notes
### Initial Suggestion
- If you want to start with a particular word, set the `__INITIAL_SUGGESTION__` variable in `wordle.py` to your preferred word
- Starting with words like *ARISE*, *ADIEU*, *ATONE*, *IRATE*, or *ALONE* increase your chances of finding at least one correct letter as each of them has 3 vowels and use the most common letters from the English language
### Similar words
- The code generally will find the correct word within 6 tries with a very high success rate  
- However it is likely to fail when the correct answer is very similar to other words  
  (words having 4 letters same, eg m**atch**, c**atch**, h**atch**, p**atch**, w**atch**, etc.)
- In such a scenario, the program will continue to suggest one of these words in alphabetical order, but it will also display all of these very similar words.  
  You can choose to use any of these similar words instead of the one suggested, should you feel that that word is more likely to be the answer.
