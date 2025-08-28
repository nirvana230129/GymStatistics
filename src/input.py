from datetime import date
import re


def parse_input(dtype):
    """
    Parse data from the user for a given dtype using a type-specific parser.

    :param dtype: 'date' | 'int' | 'float'
    :return: parsed value of requested type or None if user entered 'exit'
    """
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
    while res is None:
        user_input = input(prompts[dtype]).strip().lower()
        if user_input.lower() in ['exit', 'e']:
            break
        res = input_functions[dtype](user_input)
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
        raise ValueError

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
    # Extract numbers with a decimal point and an optional leading minus sign
    # Pattern: optional minus + digits + optional dot + optional digits OR optional minus + dot + digits
    numbers = re.findall(r'-?\d+\.?\d*|-?\.\d+', user_input)
    
    if numbers:
        # Take the first found number
        number = numbers[0]
        # Strip a trailing minus if present
        if number.endswith('-'):
            number = number[:-1]
        return float(number)
    else:
        raise ValueError("No floating-point number found")
