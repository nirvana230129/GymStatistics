from datetime import date
import re


def parse_input(dtype):
    """
    Parse data from the user.
    :return: correct data of dtype type or None if data is invalid.
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
    Inputs a date from the user in format yyyy-mm-dd or mm-dd (using current or last year).
    :return: date
    :raises: ValueError if date format is invalid
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
    Inputs an integer from the user, removing any non-digit characters except minus sign.
    :return: integer
    :raises: ValueError if no valid integer found
    """
    # Извлекаем числа с опциональным знаком минус в начале
    # Игнорируем минус в конце числа
    numbers = re.findall(r'-?\d+', user_input)
    
    if numbers:
        # Берем первое найденное число
        number = numbers[0]
        # Убираем минус в конце, если он есть
        if number.endswith('-'):
            number = number[:-1]
        return int(number)
    else:
        raise ValueError("Не найдено целое число")

def input_float(user_input) -> float:
    """
    Inputs a float from the user, removing any non-numeric characters except decimal point and minus sign.
    :return: float
    :raises: ValueError if no valid float found
    """
    # Извлекаем числа с десятичной точкой и опциональным знаком минус в начале
    # Паттерн: опциональный минус + цифры + опциональная точка + опциональные цифры
    numbers = re.findall(r'-?\d+\.?\d*|-?\.\d+', user_input)
    
    if numbers:
        # Берем первое найденное число
        number = numbers[0]
        # Убираем минус в конце, если он есть
        if number.endswith('-'):
            number = number[:-1]
        return float(number)
    else:
        raise ValueError("Не найдено дробное число")
