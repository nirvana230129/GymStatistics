import pytest
from datetime import date
from src.input import input_date, input_int, input_float


class TestInput:
    def test_input_date(self):
        assert input_date('t') == date.today()
        for sep in ['-', ':', ' ', '=', '  ']:
            assert input_date(f"01{sep}01") == date(date.today().year, 1, 1)
            assert input_date(f"1{sep}1") == date(date.today().year, 1, 1)
            assert input_date(f"12{sep}31") == date(date.today().year - 1, 12, 31)
            assert input_date(f"2025{sep}12{sep}31") == date(2025, 12, 31)
        assert input_date("2025-05:05") == date(2025, 5, 5)
        with pytest.raises(ValueError):
            input_date("")
        with pytest.raises(ValueError):
            input_date("qqq")
        with pytest.raises(ValueError):
            input_date("05")
        with pytest.raises(ValueError):
            input_date("-05-")

    def test_input_int(self):
        """Тест функции input_int для чтения целых чисел."""
        assert input_int("123") == 123
        assert input_int("0") == 0
        assert input_int("-123") == -123  # Поддерживаем отрицательные числа
        
        assert input_int("123h") == 123
        assert input_int("abc123def") == 123
        assert input_int("12.34") == 12  # Берем только целую часть
        assert input_int("123abc456") == 123  # Берем первое число
        assert input_int("abc-123def") == -123  # Отрицательное число
        assert input_int("123-") == 123  # Минус в конце игнорируется
        
        assert input_int("123 456") == 123
        assert input_int("abc123def456ghi") == 123
        assert input_int("abc-123def456ghi") == -123  # Берем первое число (отрицательное)
        
        with pytest.raises(ValueError):
            input_int("")
        with pytest.raises(ValueError):
            input_int("abc")
        with pytest.raises(ValueError):
            input_int(".")

    def test_input_float(self):
        """Тест функции input_float для чтения дробных чисел."""
        assert input_float("123.45") == 123.45
        assert input_float("0.0") == 0.0
        assert input_float("123") == 123.0  # Целое число преобразуется в float
        assert input_float(".5") == 0.5  # Число начинается с точки
        assert input_float("-123.45") == -123.45  # Поддерживаем отрицательные числа
        assert input_float("-.5") == -0.5  # Отрицательное число с точкой
        
        assert input_float("123.45h") == 123.45
        assert input_float("abc123.45def") == 123.45
        assert input_float("12.34abc56.78") == 12.34  # Берем первое число
        assert input_float("abc-123.45def") == -123.45  # Отрицательное число
        assert input_float("123.45-") == 123.45  # Минус в конце игнорируется
        
        assert input_float("123.45 678.90") == 123.45
        assert input_float("abc123.45def678.90ghi") == 123.45
        assert input_float("abc-123.45def678.90ghi") == -123.45  # Берем первое число (отрицательное)
        
        assert input_float("123.") == 123.0  # Точка в конце
        assert input_float(".123") == 0.123  # Точка в начале
        assert input_float("-123.") == -123.0  # Отрицательное число с точкой в конце
        assert input_float("-.123") == -0.123  # Отрицательное число с точкой в начале
        
        with pytest.raises(ValueError):
            input_float("")
        with pytest.raises(ValueError):
            input_float("abc")
        with pytest.raises(ValueError):
            input_float("..")
        with pytest.raises(ValueError):
            input_float(".")
