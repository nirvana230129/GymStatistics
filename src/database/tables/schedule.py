import sqlite3
from datetime import date
from .table import Table


class ScheduleTable(Table):
    """
    This class is responsible for working with the Schedule table.
    """

    def __init__(self, cursor: sqlite3.Cursor) -> None:
        """
        Connects to the database.
        :param cursor: cursor to the database.
        """
        super().__init__('Schedule', cursor)

    def create(self) -> None:
        """
        Creates the table.
        """
        self._cursor.execute("""--sql
            CREATE TABLE IF NOT EXISTS Schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                exercise_id INTEGER NOT NULL,
                order_number INTEGER NOT NULL,
                UNIQUE(date, exercise_id),
                UNIQUE(date, order_number),
                FOREIGN KEY (exercise_id) REFERENCES Exercises(id)
            );
        """)

    def add_schedule_record(self, workout_date: date, exercise_id: str, order_number: int) -> None:
        """
        Adds a new schedule record.
        :param workout_date: date of the workout.
        :param exercise_id: ID of the exercise.
        :param order_number: order number of the exercise in the workout session.
        :return: ID of the inserted record.
        """
        self._cursor.execute("""--sql
            INSERT INTO Schedule (date, exercise_id, order_number)
            VALUES (?, ?, ?);
        """, (workout_date, exercise_id, order_number))
        return self._cursor.lastrowid

