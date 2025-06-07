import sqlite3

from table import Table


class ExercisesTable(Table):
    """
    This class is responsible for working with the exercises table.
    """

    def __init__(self, db_file: str) -> None:
        """
        Connects to the database.
        :param db_file: database file to connect to.
        """
        super().__init__(db_file, 'Exercises')

    def create(self) -> None:
        """
        Creates the table.
        """
        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS Exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                alias TEXT UNIQUE,
                target_muscle_group TEXT
            );
        ''')

    def add_exercise(self, exercise_name: str, alias: str = None, target_muscle_group: str = None) -> None:
        """
        Adds a new exercise.
        :param exercise_name: name of the exercise.
        :param alias: alias of the exercise.
        :param target_muscle_group: target muscle group of the exercise.
        """
        try:
            self._cursor.execute('''
                INSERT INTO Exercises (name, alias, target_muscle_group)
                VALUES (?, ?, ?);
            ''', (exercise_name, alias, target_muscle_group))
        except sqlite3.IntegrityError as e:
            print(e)

    # def get_exercise_id(self, exercise_name: str) -> int | None:
    #     """
    #     Finds an exercise with the given name.
    #     :param exercise_name: name of the exercise.
    #     :return: exercise ID or None if no exercise with the given name.
    #     """
    #     self._cursor.execute('SELECT id FROM Exercises WHERE name = ?;', (exercise_name,))
    #     data = self._cursor.fetchone()
    #     return data[0] if data else None

    # def get_all_exercises(self) -> list[str]:
    #     """
    #     Gets all exercises.
    #     :return: list of all exercises.
    #     """
    #     self._cursor.execute('SELECT name FROM Exercises;')
    #     data = self._cursor.fetchall()
    #     return [i[0] for i in data]
