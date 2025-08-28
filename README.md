# GymStatistics

Проект для отслеживания статистики тренировок в тренажерном зале.

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd GymStatistics
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # На macOS/Linux
# или
.venv\Scripts\activate  # На Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running tests

Run all tests:
```bash
python -m pytest tests -v
```

Run a particular test:
```bash
python -m pytest tests/input_test.py -v
```

## Project structure

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
│   └── menu.py
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

## Dependencies

- pytest — run tests
- pytest-mock — mocking in tests
- matplotlib — plotting

## Run application

Create venv, install deps (see above) and run:
```bash
python src/main.py
```

The app will open an interactive menu to manage the database.
