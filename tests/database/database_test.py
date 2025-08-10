import pytest
import sqlite3
from src.database.database import Database


class TestDatabase:
    file = '../gym_tracker.db'

    ws1 = {
        'workout_date': '2025-03-27', 
        'exercise_name': 'A', 
        'order_number': 1, 
        'sets': 3, 
        'weight': 45, 
        'repetitions': 10, 
        'time': None, 
        'speed': None, 
        'units': 'kg',
        'feeling': 3,
    }
    ws2 = {
        'workout_date': '2025-03-27', 
        'exercise_name': 'B', 
        'order_number': 2, 
        'sets': 3, 
        'weight': 45, 
        'repetitions': 10, 
        'time': None, 
        'speed': None, 
        'units': 'kg',
        'feeling': 3,
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
        exercise2 = {'exercise_name': 'B', 'alias': 'b', 'target_muscle_group': ''}
        exercise3 = {'exercise_name': 'A', 'alias': 'c', 'target_muscle_group': 'z'}
        exercise4 = {'exercise_name': 'C', 'alias': 'a', 'target_muscle_group': ''}

        db.add_exercise(**exercise1)
        db.add_exercise(**exercise2)
        assert db

        for exercise in [exercise3, exercise4]:
            with pytest.raises(sqlite3.IntegrityError):
                db.add_exercise(**exercise)
        db.close()

    def test_add_workout(self):
        db = Database(self.file)
        db.create()
        db.clear()

        db.add_exercise(self.ws1['exercise_name'])
        db.add_workout(**self.ws1)
        assert db

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

        assert db.find_workout(self.ws1['workout_date'], self.ws1['exercise_name']) == \
            (1, '2025-03-27', 1, 1, 3, 45.0, 10, None, None, 'kg', 3, 0)
        assert db.find_workout('2000-01-01', 'B') == None
        assert db.find_workout(self.ws1['workout_date'], 'B') == None
        
        with pytest.raises(ValueError):
            db.find_workout(self.ws1['workout_date'], 'C')
        db.close()

    def test_plot_weights(self):
        pass
