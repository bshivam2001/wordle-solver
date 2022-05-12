import sys
import os
import wordle

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = ''
import pygame

WIDTH, HEIGHT = 633, 900
ENABLE_STATS = True                     # Enables saving win and loss statistics

if ENABLE_STATS:
    import game_stats

COL_GREEN = "#549e4d"
COL_YELLOW = "#c7b150"
COL_GREY = "#787c7e"
COL_DARK_GREY = "#606060"
COL_OUTLINE = "#d3d6da"
COL_FILLED_OUTLINE = "#878a8c"
COL_WHITE = '#f0f0f0'
COL_ERROR = '#dc3545'

# Constants
suggestions = ['      ' for i in range(6)]
grid_states = [['' for i in range(5)] for i in range(6)]
is_running = True
guess_number = 0
error_occured = False
error_code = 0
show_help = True


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

def display_errors():
    error_text = [
        'Found the word!',
        'Could not find the word :(',
        'Invalid State'
    ]

    if error_occured == False:
        return
    
    text_col = COL_ERROR if error_code > 0 else COL_GREEN
    text_surface1 = ALT_FONT.render(error_text[error_code], True, text_col)
    text_rect1 = text_surface1.get_rect(center=(WIDTH//2, 700))
    text_surface2 = ALT_FONT.render('Press Esc to reset', True, text_col)
    text_rect2 = text_surface2.get_rect(center=(WIDTH//2, 780))
    SCREEN.blit(text_surface1, text_rect1)
    SCREEN.blit(text_surface2, text_rect2)


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


def draw_board():
    SCREEN.fill((0, 0, 0))
    x, y = 80, 50
    distx, disty = 100, 100
    size = 75
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

            text_surface = GAME_FONT.render(suggestions[j][i].upper(), True, COL_WHITE)
            text_rect = text_surface.get_rect(center=(x+(distx*i)+36, y+(disty*j)+36))
            SCREEN.blit(text_surface, text_rect)

    display_help()
    display_errors()   
    pygame.display.flip()



if __name__ == '__main__':
    pygame.init()
    if ENABLE_STATS:
        game_stats.read_stats()

    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    GAME_FONT = pygame.font.SysFont('Arial Black', 50)
    ALT_FONT = pygame.font.SysFont('Courier New', 40, bold=True)
    HELP_FONT = pygame.font.SysFont('Century Gothic', 24)
    pygame.display.set_caption('Wordle Solver!', 'Wordle Solver!')
    try:
        WINDOW_ICON = pygame.image.load('icon.jpg')
        pygame.display.set_icon(WINDOW_ICON)
    except:
        print('ERROR: Could not find game icon')

    reset_game()

    while(is_running):
        draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                pygame.quit()
                break 

            if event.type == pygame.KEYDOWN:
                show_help = False
                if event.key == pygame.K_RETURN:
                    if '' in grid_states[guess_number]:
                        continue
                    elif grid_states[guess_number].count('g') == 5:
                        error_occured = True #Found the word
                        continue
                    if guess_number <= 5:
                        wordle.updatePositions(suggestions[guess_number], grid_states[guess_number])
                        guess_number += 1
                        temp = wordle.getNextSuggestion()
                        if temp == '-1':
                            error_occured = True
                            error_code = 2
                            continue
                        print('Suggested:', temp)
                        suggestions[guess_number] = temp
                    else:
                        error_occured = True
                        error_code = 1
                
                elif event.key == pygame.K_n:
                    if error_occured:
                        continue
                    if '' in grid_states[guess_number]:
                        grid_states[guess_number][grid_states[guess_number].index('')] = 'n'

                elif event.key == pygame.K_y:
                    if error_occured:
                        continue
                    if '' in grid_states[guess_number]:
                        grid_states[guess_number][grid_states[guess_number].index('')] = 'y'

                elif event.key == pygame.K_g:
                    if error_occured:
                        continue
                    if '' in grid_states[guess_number]:
                        grid_states[guess_number][grid_states[guess_number].index('')] = 'g'

                elif event.key == pygame.K_BACKSPACE:
                    if error_occured:
                        continue
                    to_remove = 4
                    while to_remove >= 0 and grid_states[guess_number][to_remove] == '':
                        to_remove -= 1
                    if to_remove >= 0:
                        grid_states[guess_number][to_remove] = ''
                
                elif event.key == pygame.K_ESCAPE:
                    # Update stats before reset
                    if error_code == 0 and grid_states[guess_number].count('g') == 5:
                        game_stats.wordle_stats['SUCCESSES'] += 1
                        game_stats.wordle_stats[str(str(guess_number+1)+'TRY')] += 1
                    elif error_code == 1:
                        game_stats.wordle_stats['FAILURES'] += 1
                    elif error_code == 2:
                        game_stats.wordle_stats['ERRORS'] += 1
                    game_stats.update_stats()
        
                    reset_game()
    if ENABLE_STATS:
        game_stats.show_stats()

    sys.exit()
            