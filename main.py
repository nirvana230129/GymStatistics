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

    def add_workout(self, workout_date: datetime.date, exercise: str, weight: float = None, feeling_rating: int = None,
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
            ''', (workout_date, exercise_id, weight, feeling_rating, description))
        except sqlite3.IntegrityError:
            raise Exception(f'Workout with {exercise} on {workout_date} already exists')

    def add_exercise(self, exercise: str):
        try:
            self._cursor.execute('''
                INSERT INTO Exercises (name)
                VALUES (?);
            ''', (exercise,))
        except sqlite3.IntegrityError:
            raise Exception(f'Exercise {exercise} already exists')

    def find_exercise(self, exercise: str):
        self._cursor.execute('SELECT id FROM Exercises WHERE name = ?;', (exercise,))
        data = self._cursor.fetchone()
        return bool(data)

    def get_all_exercises(self):
        self._cursor.execute('SELECT name FROM Exercises;')
        data = self._cursor.fetchall()
        return [i[0] for i in data]

    def print_all(self):
        self._cursor.execute('SELECT * FROM Workouts W JOIN Exercises E ON W.exercise_id = E.id')
        data = self._cursor.fetchall()
        print(data)

    def plot_weights(self, machine):
        self._cursor.execute('''
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

for i in ['подтягивания узкие', 'подтягивания широкие', 'ноги снизу вверх (первые 2)', 'дельта', 'спина',
                 'ноги сверху вниз (правый)', 'соку бачи вира', 'висюля', 'от сердца к солнцу', 'дорожка', 'бицепс']:
    db.add_exercise(i)
db.commit()
db.add_workout(str(datetime.today().date()), 'бицепс', 35)
db.commit()
db.print_all()


def input_date():
    def _input_date():
        try:
            if user_input == 't':
                return datetime.now().date()
            if 2 <= len(user_input):
                for el in user_input:
                    if not el.isdigit():
                        sep = el
                        month, day = map(int, user_input.split(sep))
                        break
                else:
                    month, day = map(int, [user_input[0], user_input[1:]])
                current_year = datetime.now().year
                date = datetime(current_year, month, day)
                if date > datetime.now():
                    date = datetime(current_year - 1, month, day)
                return date.date()
        except ValueError:
            print("\tIncorrect date format. Please enter the date in mm-dd format.")

    res = None
    while res is None:
        user_input = input('\tEnter date (mm-dd) or "t" for today or "exit" to finish: ').strip().lower()
        if user_input == 'exit':
            break
        res = _input_date()
    return res

def input_exercise():
    def _input_exercise():
        try:
            if db.find_exercise(user_input):
                return user_input

            inp = ''
            while inp not in ['y', 'n']:
                inp = input(f'\tThere is no exercise "{user_input}" in the database. '
                            f'Do you want to add it? (y/n): ').strip().lower()
            if inp == 'y':
                db.add_exercise(user_input)
                return user_input
        except ValueError:
            print("\tIncorrect input. Please try again.")

    res = None
    while res is None:
        user_input = input(f'\tEnter exercise ({", ".join(db.get_all_exercises())}): ').strip().lower()
        if user_input == 'exit':
            break
        res = _input_exercise()
    return res

def input_num(field_name, dest_type: type):
    res = None
    while res is None:
        user_input = input(f'\tEnter {field_name}: ').strip().lower()
        if user_input == 'exit':
            break
        try:
            res = dest_type(user_input)
        except ValueError:
            print(f"\tIncorrect input for type {dest_type}. Please try again.")
    return res


inp = input('Enter command: ')
while inp != 'exit' or inp != '0':
    if inp.lower() in ['add workout day', '1']:
        date = input_date()
        if date is not None:
            print('-' * 60)

            exercise = input_exercise()
            if exercise is not None:
                print('-' * 60)

                weight = input_num('weight', float)
                if weight is not None:
                    print('-' * 60)

                    rating = input_num('rating', int)
                    if rating is not None:
                        print('-' * 60)

                        description = input('    Enter description: ')

                        db.add_workout(date, exercise, weight, rating, description)
                        # db.add_workout(str(datetime.today().date()), 'висюля', weight, rating, description)

    elif inp.lower() in ['Print all', '2']:
        db.print_all()

    inp = input('Enter command: ')
