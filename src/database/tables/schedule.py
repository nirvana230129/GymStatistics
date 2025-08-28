import sqlite3
from datetime import date
from .table import Table


class ScheduleTable(Table):
    """
    `Schedule` table: workout plan/ordering for a given date.
    """

    def __init__(self, cursor: sqlite3.Cursor) -> None:
        """
        Initialize the `Schedule` table wrapper.

        :param cursor: SQLite cursor
        """
        super().__init__('Schedule', cursor)

    def create(self) -> None:
        """
        Create `Schedule` table.
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
        Add a schedule record.

        :param workout_date: workout date
        :param exercise_id: exercise id
        :param order_number: sequence number within the workout day
        :return: inserted row id
        """
        self._cursor.execute("""--sql
            INSERT INTO Schedule (date, exercise_id, order_number)
            VALUES (?, ?, ?);
        """, (workout_date, exercise_id, order_number))
        return self._cursor.lastrowid

    def delete_schedule_by_date(self, workout_date: date) -> list[int]:
        """
        Delete all schedule records for the given date.

        :param workout_date: date to delete records for
        :return: list of deleted schedule ids
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
        Delete all schedule records for the given exercise.
        """
        self._cursor.execute("""--sql
            DELETE FROM Schedule
            WHERE exercise_id = ?;
        """, (exercise_id,))
