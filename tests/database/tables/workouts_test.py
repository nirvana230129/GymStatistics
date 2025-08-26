import pytest
import sqlite3
from src.database.tables.workouts import Workout, WorkoutsTable


class TestWorkout:
    weight_example = {'schedule_id': 9999, 'sets': 3, 'weight': 45, 'repetitions': 10, 'units': 'kg', 'feeling': 3}
    speed_example = {'schedule_id': 9999, 'sets': 1, 'time': 600, 'speed': 8.5, 'units': 'kph', 'feeling': 3}

    def test_feeling(self):
        for example in [self.weight_example, self.speed_example]:
            for i in range(-10, 10):
                example['feeling'] = i
                if 1 <= i <= 5:
                    assert Workout(**example)
                else:
                    with pytest.raises(ValueError):
                        Workout(**example)
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
        for weight, repetitions in [
            [1, 1], 
            [1, [1, 1]], 
            [[1, 1], 1], 
            [[1, 1], [1, 1]]
        ]:
            assert Workout(schedule_id=9999, sets=2, weight=weight, repetitions=repetitions)

        for weight, repetitions in [
            [1, [1, 1, 1]], 
            [[1, 1, 1], 1], 
            [[1, 1, 1], [1, 1]], 
            [[1, 1], [1, 1, 1]],
            [[1, 1, 1], [1, 1, 1]],
        ]:
            with pytest.raises(ValueError):
                Workout(schedule_id=9999, sets=2, weight=weight, repetitions=repetitions)

    def test_type_combinations_speed(self):
        assert Workout(schedule_id=9999, sets=1, time=1,      speed=1)
        assert Workout(schedule_id=9999, sets=2, time=[1, 1], speed=[1, 1])

        for time, speed in [
            [1, 1], 
            [1, [1, 1]], 
            [[1, 1], 1], 
            [[1, 1], [1, 1, 1]],
            [[1, 1, 1], [1, 1, 1]],
        ]:
            with pytest.raises(ValueError):
                Workout(schedule_id=9999, sets=2, time=time, speed=speed)
    
    def test_type_combinations_mixed(self):
        assert Workout(schedule_id=9999, sets=1, time=1,      speed=1,      weight=1,      repetitions=1)
        assert Workout(schedule_id=9999, sets=2, time=[1, 1], speed=[1, 1], weight=[1, 1], repetitions=[1, 1])


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


class TestWorkouts:
    weight1 = Workout(schedule_id=1, feeling=3, sets=3, weight=1, repetitions=1, units='kg')
    weight2 = Workout(schedule_id=1, feeling=3, sets=3, weight=1, repetitions=1, units='kg')
    speed1 = Workout(schedule_id=2, feeling=3, sets=1, time=1, speed=1, units='kph')

    def test_create(self, db_cursor):
        table = WorkoutsTable(db_cursor)
        table.create()
        assert table
    
    def test_add_workout(self, db_cursor):
        table = WorkoutsTable(db_cursor)
        table.drop()
        table.create()

        table.add_workout(self.speed1)
        table.add_workout(self.weight2)

        with pytest.raises(sqlite3.IntegrityError):
            table.add_workout(self.weight1)
    
    def test_delete_workout(self, db_cursor):
        table = WorkoutsTable(db_cursor)
        table.drop()
        table.create()

        table.add_workout(self.speed1)
        table.add_workout(self.weight2)

        assert table.get_all_data() == [(1, 2, 3, -1, 1, None, None, 1, 1.0, 'kph'), (2, 1, 3, -1, 3, 1.0, 1, None, None, 'kg')]

        table.delete_by_id(1)
        assert table.get_all_data() == [(2, 1, 3, -1, 3, 1.0, 1, None, None, 'kg')]

        table.delete_by_id(1)
        assert table.get_all_data() == [(2, 1, 3, -1, 3, 1.0, 1, None, None, 'kg')]

    def test_delete_workouts_by_schedule(self, db_cursor):
        table = WorkoutsTable(db_cursor)
        table.drop()
        table.create()

        table.add_workout(self.speed1)
        table.add_workout(self.weight2)

        assert table.get_all_data() == [(1, 2, 3, -1, 1, None, None, 1, 1.0, 'kph'), (2, 1, 3, -1, 3, 1.0, 1, None, None, 'kg')]

        table.delete_workouts_by_schedule(2)
        assert table.get_all_data() == [(2, 1, 3, -1, 3, 1.0, 1, None, None, 'kg')]

        table.delete_workouts_by_schedule(2)
        assert table.get_all_data() == [(2, 1, 3, -1, 3, 1.0, 1, None, None, 'kg')]

    def test_delete_workouts_by_date(self, db_cursor):
        table = WorkoutsTable(db_cursor)
        table.drop()
        table.create()

        table.add_workout(self.speed1)
        table.add_workout(self.weight2)

        assert table.get_all_data() == [(1, 2, 3, -1, 1, None, None, 1, 1.0, 'kph'), (2, 1, 3, -1, 3, 1.0, 1, None, None, 'kg')]

        table.delete_workouts_by_schedule(2)
        assert table.get_all_data() == [(2, 1, 3, -1, 3, 1.0, 1, None, None, 'kg')]

        table.delete_workouts_by_schedule(2)
        assert table.get_all_data() == [(2, 1, 3, -1, 3, 1.0, 1, None, None, 'kg')]
