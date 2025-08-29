from datetime import date
import re


def parse_input(dtype, msg:str = None):
    """
    Parse data from the user for a given dtype using a type-specific parser.

    :param dtype: 'date' | 'int' | 'float'
    :param msg: pre-print message
    :return: parsed value of requested type or None if user entered 'exit'
    """
    if msg is not None:
        msg = msg.strip()
        if not msg.startswith('\t'):
            msg = '\t' + msg
        if not msg.endswith(':'):
            msg = msg + ':'
        msg += ' '

    input_functions = {
        'date': input_date,
        'int': input_int,
        'float': input_float
    }

    prompts = {
        'date': '\tEnter date in format yyyy-mm-dd or mm-dd (using current or last year) or "t" for today or "exit" to finish: ',
        'int': '\tEnter integer number or "exit" to finish: ',
        'float': '\tEnter float number or "exit" to finish: '
    }

    res = None
    first_time = True
    while res is None:
        tip = msg if msg is not None and first_time else prompts[dtype]
        user_input = input(tip).strip().lower()
        first_time = False
        if user_input.lower() in ['exit', 'e']:
            break
        try:
            res = input_functions[dtype](user_input)
        except ValueError as e:
            print(f'There was an error during the entering: {e}. Please try again.')
    return res

def input_date(user_input) -> date:
    """
    Parse a date from string.

    Supported formats: yyyy-mm-dd and mm-dd (using current or previous year),
    and a special shortcut 't' for today.

    :param user_input: string with a date
    :return: date object
    :raises: ValueError if the date format is invalid
    """
    if user_input == 't':
        return date.today()
    
    numbers = re.findall(r'\d+', user_input)
    
    if len(numbers) == 2:  # mm-dd
        month, day = map(int, numbers)
        current_year = date.today().year
        res_date = date(current_year, month, day)
        
        if res_date > date.today():
            res_date = date(current_year - 1, month, day)
        return res_date
        
    elif len(numbers) == 3:  # yyyy-mm-dd
        year, month, day = map(int, numbers)
        return date(year, month, day)
        
    else:
        raise ValueError('Wrong date format')

def input_int(user_input) -> int:
    """
    Extract the first integer number from a string.

    A leading minus is allowed. A trailing minus is ignored.

    :param user_input: input string
    :return: integer number
    :raises: ValueError if no valid integer is found
    """
    numbers = re.findall(r'-?\d+', user_input)
    
    if numbers:
        number = numbers[0]
        if number.endswith('-'):
            number = number[:-1]
        return int(number)
    else:
        raise ValueError("No integer number found")

def input_float(user_input) -> float:
    """
    Extract the first floating-point number from a string.

    Supports decimal point and an optional leading minus sign.

    :param user_input: input string
    :return: floating-point number
    :raises: ValueError if no valid float is found
    """
    numbers = re.findall(r'-?\d+\.?\d*|-?\.\d+', user_input)
    
    if numbers:
        number = numbers[0]
        if number.endswith('-'):
            number = number[:-1]
        return float(number)
    else:
        raise ValueError("No floating-point number found")
