# GymStatistics

Проект для отслеживания статистики тренировок в тренажерном зале.

## Установка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd GymStatistics
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python -m venv .venv
source .venv/bin/activate  # На macOS/Linux
# или
.venv\Scripts\activate  # На Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Запуск тестов

Для запуска всех тестов:
```bash
python -m pytest tests -v
```

Для запуска конкретного теста:
```bash
python -m pytest tests/input_test.py -v
```

## Структура проекта

```
GymStatistics/
├── src/
│   ├── database/
│   │   ├── database.py
│   │   └── tables/
│   │       ├── exercises.py
│   │       ├── schedule.py
│   │       ├── table.py
│   │       └── workouts.py
│   ├── input.py
│   └── main.py
├── tests/
│   ├── database/
│   │   ├── database_test.py
│   │   └── tables/
│   │       ├── exercises_test.py
│   │       ├── schedule_test.py
│   │       └── workouts_test.py
│   └── input_test.py
├── requirements.txt
└── README.md
```

## Зависимости

- pytest - для запуска тестов
- pytest-mock - для мокирования в тестах
- matplotlib - для построения графиков
