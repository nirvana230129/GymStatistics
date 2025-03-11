import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime


class Database:
    def __init__(self, db_file):
        self._connection = sqlite3.connect(db_file)
        self._cursor = self._connection.cursor()

    def drop(self):
        self._cursor.execute('DROP TABLE IF EXISTS Workouts;')
        self._cursor.execute('DROP TABLE IF EXISTS Exercises;')

    def create(self):
        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS Workouts (
                date DATE NOT NULL,
                exercise_id INT NOT NULL,
                weight REAL,
                rating INTEGER,
                description TEXT,
                PRIMARY KEY (date, exercise_id),
                FOREIGN KEY (exercise_id) REFERENCES Exercises(id)
            );
        ''')
        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS Exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            );
        ''')

    def commit(self):
        self._connection.commit()

    def add_workout(self, date: datetime.date, exercise: str, weight: float = None, rating: int = None,
                    description: str = None):
        self._cursor.execute('SELECT id FROM Exercises WHERE name = ?;', (exercise,))
        data = self._cursor.fetchone()
        if data is None:
            raise ValueError(f'There is no "{exercise}" exercise')
        exercise_id = data[0]

        try:
            self._cursor.execute(f'''
                INSERT INTO Workouts (date, exercise_id, weight, rating, description)
                VALUES (?, ?, ?, ?, ?);
            ''', (date, exercise_id, weight, rating, description))
        except sqlite3.IntegrityError:
            raise Exception(f'Workout with {exercise} on {date} already exists')

    def add_exercise(self, exercise: str):
        try:
            self._cursor.execute('''
                INSERT INTO Exercises (name)
                VALUES (?);
            ''', (exercise,))
        except sqlite3.IntegrityError:
            raise Exception(f'Exercise {exercise} already exists')

    def plot_weights(self, machine):
        self._cursor.execute(f'''
            SELECT date, weight 
            FROM Workouts 
            WHERE machine = ?
        ''', (machine,))
        data = self._cursor.fetchall()
        print(data)
        dates = [row[0] for row in data]
        weights = [row[1] for row in data]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, weights, marker='o')
        plt.title(f'Weight Progression for {machine}')
        plt.xlabel('Date')
        plt.ylabel('Weight')
        plt.grid(True)
        plt.show()


db = Database('gym_tracker.db')

db.drop()
db.create()
db.commit()

for exercise in ['подтягивания узкие', 'подтягивания широкие', 'ноги снизу вверх (первые 2)', 'дельта', 'спина',
                 'ноги сверху вниз (правый)', 'соку бачи вира', 'висюля', 'от сердца к солнцу', 'дорожка', 'бицепс']:
    db.add_exercise(exercise)
db.commit()

db.add_workout(str(datetime.today().date()), 'бицепс', 35)
# db.add_workout(datetime(2025, 3, 1).date(), 'Bench Press', 60, 5)
# db.add_workout(datetime(2025, 3, 2).date(), 'Bench Press', 62.5, 4)
# db.add_workout(datetime(2025, 3, 3).date(), 'Bench Press', 65, 4)
# db.add_workout(datetime(2025, 3, 4).date(), 'Bench Press', 70, 2)
db.commit()
