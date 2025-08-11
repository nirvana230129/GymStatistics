import pytest
import sqlite3
from src.database.database import Database


class TestDatabase:
    file = '../gym_tracker.db'

    ws1 = {
        'workout_date': '2025-03-27', 'exercise_name': 'A', 'order_number': 1, 'feeling': 3,
        'sets': 3, 'weight': 45, 'repetitions': 10, 'units': 'kg',
    }
    ws2 = {
        'workout_date': '2025-03-27', 'exercise_name': 'B', 'order_number': 2, 'feeling': 3,
        'sets': 3, 'weight': 45, 'repetitions': 10, 'units': 'kg',
    }

    def test_create(self):
        db = Database(self.file)
        db.create()
        assert db
        db.close()
    
    def test_add_exercise(self):
        db = Database(self.file)
        db.create()
        db.clear()

        exercise1 = {'exercise_name': 'A', 'alias': 'a', 'target_muscle_group': 'z'}
        exercise2 = {'exercise_name': 'B', 'alias': 'b'}
        exercise3 = {'exercise_name': 'C'}
        exercise4 = {'exercise_name': 'A', 'alias': 'c', 'target_muscle_group': 'z'}
        exercise5 = {'exercise_name': 'C', 'alias': 'a'}
        exercise6 = {'exercise_name': 'C'}

        for x in [exercise1, exercise2, exercise3]:
            db.add_exercise(**x)

        for exercise in [exercise4, exercise5, exercise6]:
            with pytest.raises(sqlite3.IntegrityError):
                db.add_exercise(**exercise)
        db.close()

    def test_add_workout(self):
        db = Database(self.file)
        db.create()
        db.clear()

        db.add_exercise(self.ws1['exercise_name'])
        db.add_workout(**self.ws1)

        with pytest.raises(ValueError):
            db.add_workout(**self.ws2)
        db.close()

    def test_find_workout(self):
        db = Database(self.file)
        db.create()
        db.clear()

        db.add_exercise(self.ws1['exercise_name'])
        db.add_exercise('B')
        db.add_workout(**self.ws1)

        assert db.find_workout(self.ws1['workout_date'], self.ws1['exercise_name']) == [(1, '2025-03-27', 1, 1, 1, 3, -1, 3, 45.0, 10, None, None, 'kg')]
        assert db.find_workout('2000-01-01', 'B') == []
        assert db.find_workout(self.ws1['workout_date'], 'B') == []
        
        with pytest.raises(ValueError):
            db.find_workout(self.ws1['workout_date'], 'C')
        db.close()

    def test_plot_weights(self):
        pass
