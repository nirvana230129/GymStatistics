import pytest
import sqlite3
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


class TestExercises:
    exercise1 = {'exercise_name': 'A', 'alias': 'a', 'target_muscle_group': 'z'}
    exercise2 = {'exercise_name': 'B', 'alias': 'b', 'target_muscle_group': ''}
    exercise3 = {'exercise_name': 'A', 'alias': 'c', 'target_muscle_group': 'z'}
    exercise4 = {'exercise_name': 'C', 'alias': 'a', 'target_muscle_group': ''}

    def test_create(self, db_connection, db_cursor):
        table = ExercisesTable(db_connection, db_cursor)
        table.create()
        assert table
    
    def test_add_exercise(self, db_connection, db_cursor):
        table = ExercisesTable(db_connection, db_cursor)
        table.drop()
        table.create()

        table.add_exercise(**self.exercise1)
        table.add_exercise(**self.exercise2)

        for exercise in [self.exercise3, self.exercise4]:
            with pytest.raises(sqlite3.IntegrityError):
                table.add_exercise(**exercise)
    
    def test_get_exercise_id(self, db_connection, db_cursor):
        table = ExercisesTable(db_connection, db_cursor)
        table.drop()
        table.create()

        table.add_exercise(**self.exercise1)
        table.add_exercise(**self.exercise2)

        assert table.get_exercise_id('A') == 1
        assert table.get_exercise_id('B') == 2

        assert table.get_exercise_id('a', may_be_alias=True) == 1
        assert table.get_exercise_id('b', may_be_alias=True) == 2

        assert table.get_exercise_id('C') is None
        assert table.get_exercise_id('c', may_be_alias=True) is None
