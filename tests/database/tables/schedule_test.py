import pytest
import sqlite3
from src.database.tables.schedule import ScheduleTable
from src.database.tables.exercises import ExercisesTable


@pytest.fixture
def db_connection():
    connection = sqlite3.connect('../gym_tracker.db')
    yield connection
    connection.close()

@pytest.fixture
def db_cursor(db_connection):
    cursor = db_connection.cursor()
    yield cursor
    cursor.close()


class TestScheduleTable:
    def test_create(self, db_cursor):
        table = ScheduleTable(db_cursor)
        table.create()
        assert table
    
    def test_add_schedule_record(self, db_cursor):
        exercises = ExercisesTable(db_cursor)
        exercises.drop()
        exercises.create()
        id1 = exercises.add_exercise('A')
        id2 = exercises.add_exercise('B')
        id3 = exercises.add_exercise('C')

        table = ScheduleTable(db_cursor)
        table.drop()
        table.create()

        table.add_schedule_record('2024-01-01', id1, 1)
        table.add_schedule_record('2024-01-01', id2, 2)
        table.add_schedule_record('2024-01-02', id1, 1)

        for (date, id, order_num) in [
            ['2024-01-01', id3, 1],
            ['2024-01-01', id1, 3]
        ]:
            with pytest.raises(sqlite3.IntegrityError):
                table.add_schedule_record(date, id, order_num)
