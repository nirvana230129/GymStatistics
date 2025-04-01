import sqlite3
import matplotlib.pyplot as plt
from datetime import date


class Database:
    """
    This class is responsible for working with the database.
    """

    def __init__(self, db_file: str) -> None:
        """
        Connects to the database.
        :param db_file: database file to connect to.
        """
        self._connection = sqlite3.connect(db_file)
        self._cursor = self._connection.cursor()

    def drop(self) -> None:
        """
        Clears the database.
        """
        self._cursor.execute('DROP TABLE IF EXISTS Workouts;')
        self._cursor.execute('DROP TABLE IF EXISTS Exercises;')

    def create(self) -> None:
        """
        Creates 'Workouts' and 'Exercises' tables.
        """
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

    def commit(self) -> None:
        """
        Commits the changes to the database.
        """
        self._connection.commit()

    def add_workout(
            self,
            workout_date: date,
            exercise: str,
            weight: float = None,
            feeling_rating: int = None,
            description: str = None
    ) -> None:
        """
        Adds a new workout to the database.
        :param workout_date: date of the workout.
        :param exercise: name of the exercise.
        :param weight: weight that was used during the workout.
        :param feeling_rating: feeling rating (from 1 to 5).
        :param description: additional information about the workout.
        """
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

    def find_workout(self, workout_date: date, exercise_id: int) -> tuple | None:
        """
        Finds a workout with the given date and exercise ID.
        :param workout_date: date of the workout.
        :param exercise_id: id of the exercise.
        :return: workout or None if no workout with the given date and exercise ID.
        """
        self._cursor.execute('SELECT * FROM Workouts WHERE date = ? AND exercise_id = ?;',
                             (workout_date, exercise_id))
        data = self._cursor.fetchone()
        return data or None

    def add_exercise(self, exercise_name: str) -> None:
        """
        Adds a new exercise to the database.
        :param exercise_name: name of the exercise.
        """
        try:
            self._cursor.execute('''
                INSERT INTO Exercises (name)
                VALUES (?);
            ''', (exercise_name,))
        except sqlite3.IntegrityError:
            raise Exception(f'Exercise {exercise_name} already exists')

    def get_exercise_id(self, exercise_name: str) -> int | None:
        """
        Finds an exercise with the given name.
        :param exercise_name:
        :return: exercise ID or None if no exercise with the given name.
        """
        self._cursor.execute('SELECT id FROM Exercises WHERE name = ?;', (exercise_name,))
        data = self._cursor.fetchone()
        return data[0] if data else None

    def get_all_exercises(self) -> list[str]:
        """
        Gets all exercises.
        :return: list of all exercises.
        """
        self._cursor.execute('SELECT name FROM Exercises;')
        data = self._cursor.fetchall()
        return [i[0] for i in data]

    def print_all(self) -> None:
        """
        Prints all data in the database.
        """
        self._cursor.execute('SELECT * FROM Workouts W JOIN Exercises E ON W.exercise_id = E.id')
        data = self._cursor.fetchall()
        print(data)

    # def plot_weights(self, machine):
    #     self._cursor.execute('''
    #         SELECT date, weight
    #         FROM Workouts
    #         WHERE machine = ?
    #     ''', (machine,))
    #     data = self._cursor.fetchall()
    #     print(data)
    #     dates = [row[0] for row in data]
    #     weights = [row[1] for row in data]
    #
    #     plt.figure(figsize=(10, 5))
    #     plt.plot(dates, weights, marker='o')
    #     plt.title(f'Weight Progression for {machine}')
    #     plt.xlabel('Date')
    #     plt.ylabel('Weight')
    #     plt.grid(True)
    #     plt.show()


class Interface:
    """
    This class is responsible for interacting with the database.
    """

    def __init__(self, db_file: str, clear: bool = False) -> None:
        """
        Connects to the database.
        :param db_file: database file to connect to.
        :param clear: if True, clears the database.
        """
        self.db = Database(db_file)
        if clear:
            self.db.drop()
            self.db.create()
            self.db.commit()

    def fill_rubbish(self) -> None:
        """
        Fills the database with a rubbish.
        """
        for i in ['подтягивания узкие', 'подтягивания широкие', 'ноги снизу вверх (первые 2)', 'дельта', 'спина',
                  'ноги сверху вниз (правый)', 'соку бачи вира', 'висюля', 'от сердца к солнцу', 'дорожка', 'бицепс']:
            self.db.add_exercise(i)
        self.db.commit()
        self.db.add_workout(date.today(), 'бицепс', 35)
        self.db.commit()

    @staticmethod
    def _input_date() -> date | None:
        """
        Inputs a date from the user.
        :return: date or None if date is invalid or user wants to exit.
        """
        def _parse_date_input() -> date | None:
            """
            Parse date from the user.
            :return: date or None if date is invalid.
            """
            try:
                if user_input == 't':
                    return date.today()
                if 2 <= len(user_input):
                    for el in user_input:
                        if not el.isdigit():
                            sep = el
                            month, day = map(int, user_input.split(sep))
                            break
                    else:
                        month, day = map(int, [user_input[0], user_input[1:]])
                    current_year = date.today().year
                    res_date = date(current_year, month, day)
                    if res_date > date.today():
                        res_date = date(current_year - 1, month, day)
                    return res_date
            except ValueError:
                print("\tIncorrect date format. Please enter the date in mm-dd format.")

        res = None
        while res is None:
            user_input = input('\tEnter date (mm-dd) or "t" for today or "exit" to finish: ').strip().lower()
            if user_input == 'exit':
                break
            res = _parse_date_input()
        return res

    @staticmethod
    def _input_num(field_name: str, dest_type: type) -> int | float | None:
        """
        Inputs a number from the user.
        :param field_name: name of the field (used in prints).
        :param dest_type: type of the field (int or float).
        :return: number or None if field is invalid or user wants to exit.
        """
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

    def _input_exercise(self) -> str | None:
        """
        Inputs an exercise from the user.
        :return: exercise or None if exercise is invalid or user wants to exit.
        """
        def _parse_input_exercise() -> str | None:
            """
            Parse input from the user.
            :return: exercise or None if exercise is invalid.
            """
            try:
                if self.db.get_exercise_id(user_input):
                    return user_input

                y_n_inp = ''
                while y_n_inp != 'n':
                    y_n_inp = input(f'\tThere is no exercise "{user_input}" in the database. '
                                f'Do you want to add it? (y/n): ').strip().lower()
                    if y_n_inp == 'y':
                        self.db.add_exercise(user_input)
                        return user_input
            except ValueError:
                print("\tIncorrect input. Please try again.")

        res = None
        while res is None:
            user_input = input(f'\tEnter an exercise ({", ".join(self.db.get_all_exercises())}): ').strip().lower()
            if user_input == 'exit':
                break
            res = _parse_input_exercise()
        return res

    def add_workout(self) -> tuple | None:
        """
        Adds a workout to the database.
        :return: added workout or None if something went wrong.
        """
        exercise_date = self._input_date()
        if exercise_date is None:
            return None
        print('-' * 60)

        exercise_name = self._input_exercise()
        if exercise_name is None:
            return None
        print('-' * 60)

        weight = self._input_num('weight', float)
        if weight is None:
            return None
        print('-' * 60)

        rating = self._input_num('rating', int)
        if rating is None:
            return None
        print('-' * 60)

        description = input('    Enter description: ')

        self.db.add_workout(exercise_date, exercise_name, weight, rating, description)
        self.db.commit()
        return self.db.find_workout(exercise_date, self.db.get_exercise_id(exercise_name))

    def print_all(self) -> None:
        """
        Prints all data in the database.
        """
        self.db.print_all()



interface = Interface(db_file='gym_tracker.db', clear=True)
interface.fill_rubbish()

tip = '0.Exit, 1.Add workout day, 2.Print all'
inp = input(f'Enter command ({tip}): ')
while inp != 'exit' and inp != '0':
    if inp.lower() in ['add workout day', '1']:
        print(interface.add_workout(), end='\n\n')

    elif inp.lower() in ['Print all', '2']:
        interface.print_all()

    elif inp.lower() in ['Print all', '3']:
        print(interface.db.get_all_exercises())

    inp = input(f'Enter command ({tip}): ')

