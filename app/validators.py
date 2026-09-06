VALID_COMMANDS = {'1', '2', '3', '4', '5', '6'}
VALID_PRIORITYS = {'1', '2', '3', '4', '5'}

def validate_command(command):
    ''' получает str; возвращает bool; побочных эффектов не имеет '''
    cleaned = command.strip()
    return cleaned in VALID_COMMANDS

def normalize_title(title):
    ''' получает str; возвращает str; побочных эффектов не имеет '''
    return title.strip()

def is_normalized_priority(priority):
    ''' получает int; возвращет bool; побочных эффектов не имеет '''
    return priority in VALID_PRIORITYS