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

    def delete_schedule_by_date(self, workout_date: date) -> list[int]:
        """
        Deletes all schedule records for the given date.
        :param workout_date: date of the workout to delete.
        """
        self._cursor.execute("""
            SELECT id FROM Schedule
            WHERE date = ?;
        """, (workout_date,))
        deleted_ids = [row[0] for row in self._cursor.fetchall()]

        self._cursor.execute("""--sql
            DELETE FROM Schedule
            WHERE date = ?;
        """, (workout_date,))
        return deleted_ids

    def delete_schedule_by_exercise(self, exercise_id: int) -> None:
        """
        Deletes all schedule records for the given exercise.
        :param exercise_id: ID of the exercise to delete from schedule.
        """
        self._cursor.execute("""--sql
            DELETE FROM Schedule
            WHERE exercise_id = ?;
        """, (exercise_id,))
