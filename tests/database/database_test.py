import pytest
import sqlite3
from src.database.database import Database


class TestDatabase:
    file = '../gym_tracker.db'
    def test_create(self):
        db = Database(self.file)
        db.create()
        assert db
    
    def test_add_exercise(self):
        db = Database(self.file)
        db.drop()
        db.create()

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
