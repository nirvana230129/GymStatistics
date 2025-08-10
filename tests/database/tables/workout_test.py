import pytest
import sqlite3
from src.database.tables.workout_sessions import Workout, WorkoutSessionsTable


class TestWorkout:
    weight_example = {
        'workout_date': '2025-03-27', 'exercise_id': 9999, 'order_number': 1, 'feeling': 3,
        'sets': 3, 'weight': 45, 'repetitions': 10, 'units': 'kg',
    }

    speed_example = {
        'workout_date': '2025-03-27', 'exercise_id': 9999, 'order_number': 1, 'feeling': 3,
        'sets': 3, 'time': 600, 'speed': 8.5, 'units': 'kph',
    }

    def test_feeling(self):
        for example in [self.weight_example, self.speed_example]:
            for i in range(-10, 10):
                if i < 1 or 5 < i:
                    example['feeling'] = i
                    with pytest.raises(ValueError):
                        Workout(**example)

            for i in range(1, 6):
                example['feeling'] = i
                assert Workout(**example)

            example['feeling'] = None
            assert Workout(**example)

    def test_units(self):
        example = self.weight_example
        
        for val in ['kg', 'lbs', None]:
            example['units'] = val
            assert Workout(**example)
        for val in ['kph', 'mph', '', 'ggg']:
            example['units'] = val
            with pytest.raises(ValueError):
                Workout(**example)
        
        example = self.speed_example
        
        for val in ['kph', 'mph', None]:
            example['units'] = val
            assert Workout(**example)
        for val in ['kg', 'lbs', '', 'ggg']:
            example['units'] = val
            with pytest.raises(ValueError):
                Workout(**example)

    def test_type_combinations_weight(self):
        assert Workout('2025-03-27', 9999, 1, 3, 45, 10)
        assert Workout('2025-03-27', 9999, 1, 3, 45, [5, 7, 9])
        assert Workout('2025-03-27', 9999, 1, 3, [41, 42, 43], 10)
        assert Workout('2025-03-27', 9999, 1, 3, [41, 42, 43], [5, 7, 9])
        with pytest.raises(ValueError):
            Workout('2025-03-27', 9999, 1, 3, 45, [5, 7])
        with pytest.raises(ValueError):
            Workout('2025-03-27', 9999, 1, 3, [41, 42], 10)
        with pytest.raises(ValueError):
            Workout('2025-03-27', 9999, 1, 3, [41, 42], [5, 7])
        with pytest.raises(ValueError):
            Workout('2025-03-27', 9999, 1, 3, [41, 42], [5, 7, 9])
        with pytest.raises(ValueError):
            Workout('2025-03-27', 9999, 1, 3, [41, 42, 43], [5, 7])

    def test_type_combinations_speed(self):
        assert Workout('2025-03-27', 9999, 1, 3, None, None, 600, 8.5)
        assert Workout('2025-03-27', 9999, 1, 3, None, None, [100, 200, 300], [5, 6.5, 5])
        with pytest.raises(ValueError):
            Workout('2025-03-27', 9999, 1, 3, None, None, 600, [5, 6.5, 5])
        with pytest.raises(ValueError):
            Workout('2025-03-27', 9999, 1, 3, None, None, [100, 200, 300], 8.5)
        with pytest.raises(ValueError):
            Workout('2025-03-27', 9999, 1, 3, None, None, 600, [5, 6.5])
        with pytest.raises(ValueError):
            Workout('2025-03-27', 9999, 1, 3, None, None, [100, 200, 300], [5, 6.5])
        with pytest.raises(ValueError):
            Workout('2025-03-27', 9999, 1, 3, None, None, [100, 200], 8.5)
        with pytest.raises(ValueError):
            Workout('2025-03-27', 9999, 1, 3, None, None, [100, 200], [5, 6.5, 5])
        with pytest.raises(ValueError):
            Workout('2025-03-27', 9999, 1, 3, None, None, [100, 200], [5, 6.5])
    
    def test_type_combinations_mixed(self):
        assert Workout('2025-03-27', 9999, 1, 3, 45, 10, 600, 8.5)
        assert Workout('2025-03-27', 9999, 1, 3, [41, 42, 43], [5, 7, 9], [100, 200, 300], [5, 6.5, 5])


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


class TestWorkoutSessions:
    weight1 = Workout(
        workout_date='2025-03-27', exercise_id=9999, order_number=1, feeling=3,
        sets=3, weight=45, repetitions=10, units='kg',
    )
    weight2 = Workout(
        workout_date='2025-03-27', exercise_id=9999, order_number=2, feeling=3,
        sets=3, weight=45, repetitions=10, units='kg',
    )
    speed1 = Workout(
        workout_date='2025-03-27', exercise_id=9999, order_number=1, feeling=3,
        sets=3, time=600, speed=8.5, units='kph',
    )

    def test_create(self, db_connection, db_cursor):
        table = WorkoutSessionsTable(db_connection, db_cursor)
        table.create()
        assert table
    
    def test_add_workout(self, db_connection, db_cursor):
        table = WorkoutSessionsTable(db_connection, db_cursor)
        table.drop()
        table.create()

        table.add_workout(self.speed1)
        table.add_workout(self.weight2)

        with pytest.raises(sqlite3.IntegrityError):
            table.add_workout(self.weight1)
    
    def test_add_workout_session(self, db_connection, db_cursor):
        table = WorkoutSessionsTable(db_connection, db_cursor)
        table.drop()
        table.create()

        table.add_workout_session([self.speed1, self.weight2])

        with pytest.raises(sqlite3.IntegrityError):
            table.add_workout_session([self.speed1, self.weight1])
