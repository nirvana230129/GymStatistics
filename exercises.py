import sqlite3

from table import Table


class ExercisesTable(Table):
    """
    This class is responsible for working with the Exercises table.
    """

    def __init__(self, connection: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
        """
        Connects to the database.
        :param connection: connection to the database.
        :param cursor: cursor to the database.
        """
        super().__init__('Exercises', connection, cursor)

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

    def get_exercise_id(self, exercise_name: str, may_be_alias: bool = False) -> int | None:
        """
        Finds an exercise with the given name.
        :param exercise_name: name of the exercise.
        :return: exercise ID or None if no exercise with the given name.
        """
        if may_be_alias:
            self._cursor.execute('SELECT id FROM Exercises WHERE name = ? OR alias = ?;', (exercise_name, exercise_name))
        else:
            self._cursor.execute('SELECT id FROM Exercises WHERE name = ?;', (exercise_name,))
        data = self._cursor.fetchone()
        return data[0] if data else None

    # def get_all_exercises(self) -> list[str]:
    #     """
    #     Gets all exercises.
    #     :return: list of all exercises.
    #     """
    #     self._cursor.execute('SELECT name FROM Exercises;')
    #     data = self._cursor.fetchall()
    #     return [i[0] for i in data]
