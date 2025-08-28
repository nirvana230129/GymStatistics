import sqlite3
from .table import Table


class ExercisesTable(Table):
    """
    `Exercises` table: exercises and their attributes (alias, muscle group).
    """

    def __init__(self, cursor: sqlite3.Cursor) -> None:
        """
        Initialize the `Exercises` table wrapper.

        :param cursor: SQLite cursor
        """
        super().__init__('Exercises', cursor)

    def create(self) -> None:
        """
        Create `Exercises` table.
        """
        self._cursor.execute("""--sql
            CREATE TABLE IF NOT EXISTS Exercises (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                alias TEXT UNIQUE,
                target_muscle_group TEXT
            );
        """)

    def add_exercise(self, exercise_name: str, alias: str = None, target_muscle_group: str = None) -> None:
        """
        Add an exercise to the table.

        :param exercise_name: name
        :param alias: alias
        :param target_muscle_group: target muscle group
        """
        self._cursor.execute("""--sql
            INSERT INTO Exercises (name, alias, target_muscle_group)
            VALUES (?, ?, ?);
        """, (exercise_name, alias, target_muscle_group))
        return self._cursor.lastrowid
    
    def get_exercise_id(self, exercise_name: str, may_be_alias: bool = False) -> int | None:
        """
        Return exercise id by name (or by alias if may_be_alias is True).
        """
        if may_be_alias:
            self._cursor.execute("SELECT id FROM Exercises WHERE name = ? OR alias = ?;", (exercise_name, exercise_name))
        else:
            self._cursor.execute("SELECT id FROM Exercises WHERE name = ?;", (exercise_name,))
        data = self._cursor.fetchone()
        return data[0] if data else None
