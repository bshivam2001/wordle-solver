__STATS_FILE__ = 'stats.txt'

# STAT DICT
wordle_stats = {
    'SUCCESSES': 0,
    'FAILURES': 0,
    'ERRORS': 0,
    '1TRY': 0,
    '2TRY': 0,
    '3TRY': 0,
    '4TRY': 0,
    '5TRY': 0,
    '6TRY': 0
}

#Function to read the stats file
def read_stats():
    global wordle_stats
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
                
                if line[0] in wordle_stats.keys():
                    wordle_stats[line[0]] = int(line[1])
                 
    except FileNotFoundError:
        print('Creating stats file...')
        file = open(__STATS_FILE__, 'w')
        file.close()
    except ValueError:
        print('Error parsing stats file')


# Function to update the current stats in the file
def update_stats():
    global wordle_stats
    with open(__STATS_FILE__, 'w') as file:
        for key, value in wordle_stats.items():
            file.write(str(key + '=' + str(value) + '\n'))


def show_stats():
    total_games = wordle_stats['SUCCESSES'] + wordle_stats['FAILURES']
    total_games = 1 if total_games == 0 else total_games # Avoid division by zero
    success_rate = (wordle_stats['SUCCESSES'] / total_games) * 100
    print('Success Rate: %.2f %%' % (success_rate))