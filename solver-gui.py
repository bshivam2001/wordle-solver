import sys                              # for sys.exit()
import os                               # for os.environ()
import wordle

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''
import pygame

WIDTH, HEIGHT = 633, 900                # Window width and height
ENABLE_STATS = True                     # Enables saving win and loss statistics

if ENABLE_STATS:
    import game_stats

# COLOR CONSTANTS
COL_GREEN = "#549e4d"
COL_YELLOW = "#c7b150"
COL_GREY = "#787c7e"
COL_DARK_GREY = "#606060"
COL_WHITE = '#f0f0f0'
COL_ERROR = '#dc3545'

# Constants
suggestions = ['      ' for i in range(6)]                      # Stores all previous suggested words
grid_states = [['' for i in range(5)] for i in range(6)]        # Stores all previous grid states in the form (g/y/n)*5
is_running = True                                               # Main game loop variable
guess_number = 0                                                # Current guess number, game ends when this is equal to 5
error_occured = False                                           # Variable to check if any error has occurred
error_code = 0                                                  # Stores an error code when an error does occur
show_help = True                                                # Show help when game starts
x, y = 80, 50                                                   # Grid start position
distx, disty = 100, 100                                         # Distance between boxes in the grid
size = 75                                                       # Size of the boxes


# Function to reset all variables to their initial state 
def reset_game():
    global suggestions, grid_states, is_running, guess_number, error_occured, error_code
    suggestions = ['      ' for i in range(6)]
    grid_states = [['' for i in range(5)] for i in range(6)]
    is_running = True
    guess_number = 0
    error_occured = False
    error_code = 0
    wordle.reset()
    suggestions[0] = wordle.getNextSuggestion()
    print('Suggested:', suggestions[0])


# Function to display errors; Win and Loss are also treated as errors
def display_errors():
    # If an error hasn't occurred, return
    if error_occured == False:
        return
    # Store all error messages
    error_text = [
        'Found the word!',
        'Could not find the word :(',
        'Invalid State'
    ]
    # Set text color according to error message
    text_col = COL_ERROR if error_code > 0 else COL_GREEN
    # Display the error text
    text_surface1 = ALT_FONT.render(error_text[error_code], True, text_col)
    text_rect1 = text_surface1.get_rect(center=(WIDTH//2, 700))
    text_surface2 = ALT_FONT.render('Press Esc to reset', True, text_col)
    text_rect2 = text_surface2.get_rect(center=(WIDTH//2, 780))
    SCREEN.blit(text_surface1, text_rect1)
    SCREEN.blit(text_surface2, text_rect2)


# Function to display help messages at the start of the game
def display_help():
    if not show_help:
        return
    text_surface = HELP_FONT.render('Try the displayed word in wordle', True, COL_WHITE)
    text_rect = text_surface.get_rect(center=(WIDTH//2, 300))
    SCREEN.blit(text_surface, text_rect)
    text_surface = HELP_FONT.render('Press \'g\' if a letter matches its place', True, COL_GREEN)
    text_rect = text_surface.get_rect(center=(WIDTH//2, 380))
    SCREEN.blit(text_surface, text_rect)
    text_surface = HELP_FONT.render('Press \'y\' if the letter is present', True, COL_YELLOW)
    text_rect = text_surface.get_rect(center=(WIDTH//2, 420))
    SCREEN.blit(text_surface, text_rect)
    text_surface = HELP_FONT.render('at the wrong place', True, COL_YELLOW)
    text_rect = text_surface.get_rect(center=(WIDTH//2, 445))
    SCREEN.blit(text_surface, text_rect)
    text_surface = HELP_FONT.render('Press \'n\' if the letter is not present', True, COL_ERROR)
    text_rect = text_surface.get_rect(center=(WIDTH//2, 485))
    SCREEN.blit(text_surface, text_rect)
    text_surface = HELP_FONT.render('at all in the word', True, COL_ERROR)
    text_rect = text_surface.get_rect(center=(WIDTH//2, 510))
    SCREEN.blit(text_surface, text_rect)
    text_surface = HELP_FONT.render('Press the Enter key to finish entering', True, COL_GREY)
    text_rect = text_surface.get_rect(center=(WIDTH//2, 550))
    SCREEN.blit(text_surface, text_rect)
    text_surface = HELP_FONT.render('Press the backspace key to go back a letter', True, COL_GREY)
    text_rect = text_surface.get_rect(center=(WIDTH//2, 590))
    SCREEN.blit(text_surface, text_rect)
    text_surface = HELP_FONT.render('Press the espace key to reset', True, COL_GREY)
    text_rect = text_surface.get_rect(center=(WIDTH//2, 630))
    SCREEN.blit(text_surface, text_rect)


# Function to draw the game
def draw_board():
    SCREEN.fill((0, 0, 0))
    global x, y, distx, disty, size
    # Draw the grid
    for j in range(guess_number+1):
        for i in range(5):
            if grid_states[j][i] == '':
                pygame.draw.rect(SCREEN, COL_GREY, (x+(distx*i), y+(disty*j), size, size), width = 1)
            elif grid_states[j][i] == 'n':
                pygame.draw.rect(SCREEN, COL_DARK_GREY, (x+(distx*i), y+(disty*j), size, size))
            elif grid_states[j][i] == 'y':
                pygame.draw.rect(SCREEN, COL_YELLOW, (x+(distx*i), y+(disty*j), size, size))
            elif grid_states[j][i] == 'g':
                pygame.draw.rect(SCREEN, COL_GREEN, (x+(distx*i), y+(disty*j), size, size))
            # Draw respective letters in each box
            text_surface = GAME_FONT.render(suggestions[j][i].upper(), True, COL_WHITE)
            text_rect = text_surface.get_rect(center=(x+(distx*i)+36, y+(disty*j)+36))
            SCREEN.blit(text_surface, text_rect)
    # Display help and error messages
    display_help()
    display_errors()   
    # Update the screen
    pygame.display.flip()



if __name__ == '__main__':
    pygame.init()
    # Enable reading and writing statistics in the stats file
    if ENABLE_STATS:
        game_stats.read_stats()

    # Initialize main screen
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    # Load font for wordle letters
    GAME_FONT = pygame.font.SysFont('Arial Black', 50)
    # Load font for error messages
    ALT_FONT = pygame.font.SysFont('Courier New', 40, bold=True)
    # Load font for help messages
    HELP_FONT = pygame.font.SysFont('Century Gothic', 24)
    pygame.display.set_caption('Wordle Solver!', 'Wordle Solver!')
    try:
        WINDOW_ICON = pygame.image.load('icon.jpg')
        pygame.display.set_icon(WINDOW_ICON)
    except:
        print('ERROR: Could not find game icon')

    # Initialize the game
    reset_game()

    # Main game loop
    while(is_running):
        # Draw the board and revelant help and error messages
        draw_board()
        # Handle Events
        for event in pygame.event.get():
            # Game quit event, generated when you press the X button in the title bar
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                break 
            # Keydown event
            if event.type == pygame.KEYDOWN:
                # If any key is pressed, stop displaying help
                show_help = False
                # Return key
                if event.key == pygame.K_RETURN:
                    # If all boxes in current guess do not have a correctness value, do nothing
                    if '' in grid_states[guess_number]:
                        continue
                    # If all boxes are green, end the game
                    elif grid_states[guess_number].count('g') == 5:
                        error_occured = True # Found the word
                        continue
                    # If less than 6 guesses have been made, store the current grid state
                    if guess_number < 5:
                        # Update positions in the wordle lists
                        wordle.updatePositions(suggestions[guess_number], grid_states[guess_number])
                        # Increment the number of guesses that have been made
                        guess_number += 1
                        temp = wordle.getNextSuggestion()
                        if temp == '-1':
                            error_occured = True    # Invalid game state; either due to user input error, or word not in dictionary
                            error_code = 2
                            continue
                        # Print and display the suggestion
                        print('Suggested:', temp)
                        suggestions[guess_number] = temp
                    else:
                        error_occured = True    # Game over, could not find word in 6 guessess
                        error_code = 1
                # 'N' key
                elif event.key == pygame.K_n:
                    # Do nothing in error state
                    if error_occured:
                        continue
                    # Update the current box to be a grey 'n' value
                    if '' in grid_states[guess_number]:
                        grid_states[guess_number][grid_states[guess_number].index('')] = 'n'
                # 'Y' key
                elif event.key == pygame.K_y:
                    # Do nothing in error state
                    if error_occured:
                        continue
                    # Update the current box to be a yellow 'y' value
                    if '' in grid_states[guess_number]:
                        grid_states[guess_number][grid_states[guess_number].index('')] = 'y'
                # 'G' key
                elif event.key == pygame.K_g:
                    # Do nothing in error state
                    if error_occured:
                        continue
                    # Update the current box to be a green 'g' value
                    if '' in grid_states[guess_number]:
                        grid_states[guess_number][grid_states[guess_number].index('')] = 'g'
                # Backspace
                elif event.key == pygame.K_BACKSPACE:
                    # Do nothing in error state
                    if error_occured:
                        continue
                    # Find which letter's state needs to be reset
                    to_remove = 4
                    while to_remove >= 0 and grid_states[guess_number][to_remove] == '':
                        to_remove -= 1
                    # If there is a box that is not empty state, reset it
                    if to_remove >= 0:
                        grid_states[guess_number][to_remove] = ''
                # Escape key
                elif event.key == pygame.K_ESCAPE:
                    # Update stats before reset
                    if error_code == 0 and grid_states[guess_number].count('g') == 5:
                        game_stats.increment_stat('SUCCESSES')
                        game_stats.increment_stat(str(str(guess_number+1)+'TRY'))
                    elif error_code == 1:
                        game_stats.increment_stat('FAILURES')
                    elif error_code == 2:
                        game_stats.increment_stat('ERRORS')
                    game_stats.update_stats()
                    # Reset the game
                    reset_game()
    # Show stats before exit
    if ENABLE_STATS:
        game_stats.show_stats()
    sys.exit()
