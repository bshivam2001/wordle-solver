__STATS_FILE__ = 'stats.txt'

# Store all different types of stats you'd like to save
available_stats = ['SUCCESSES', 'FAILURES', 'ERRORS', '1TRY', '2TRY', '3TRY', '4TRY', '5TRY', '6TRY']

# Dictionary to store stat values
game_stats = {}
# Initialize dictionary
for stat in available_stats:
    game_stats[stat] = 0


#Function to read the stats file
def read_stats():
    global game_stats
    try:
        with open('stats.txt') as file:
            lines = file.readlines()
            for line in lines:
                # Read one line at a time
                line = line.replace(' ','').split('=')
                if not line:
                    break
                elif len(line) > 2:
                    continue
                
                if line[0] in game_stats.keys():
                    game_stats[line[0]] = int(line[1])
                 
    except FileNotFoundError:
        print('Creating stats file...')
        file = open(__STATS_FILE__, 'w')
        file.close()
    except ValueError:
        print('Error parsing stats file')


# Function to increment the value of the given stat
def increment_stat(stat):
    if stat in game_stats.keys():
        game_stats[stat] += 1
    else:
        print('ERROR: Statistic value {stat} not available')


# Function to update the current stats in the file
def update_stats():
    global game_stats
    with open(__STATS_FILE__, 'w') as file:
        for key, value in game_stats.items():
            file.write(str(key + '=' + str(value) + '\n'))


def show_stats():
    # Show success rate if available
    try:
        total_games = game_stats['SUCCESSES'] + game_stats['FAILURES']
        total_games = 1 if total_games == 0 else total_games # Avoid division by zero
        success_rate = (game_stats['SUCCESSES'] / total_games) * 100
        print('\nSuccesses: %s' % (game_stats['SUCCESSES']))
        print('Failures: %s' % (game_stats['FAILURES']))
        print('Success Rate: %.2f %%' % (success_rate))
    except KeyError:
        pass
