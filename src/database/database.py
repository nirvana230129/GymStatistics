import sqlite3
from datetime import date
from .tables.exercises import ExercisesTable
from .tables.workout_sessions import Workout, WorkoutSessionsTable


class Database:
    """
    This class is responsible for working with the database.
    """

    def __init__(self, db_file: str) -> None:
        """
        Connects to the database.
        :param db_file: database file to connect to.
        """
        self._connection = sqlite3.connect(db_file)
        self._cursor = self._connection.cursor()
        self._exercises_table = ExercisesTable(self._connection, self._cursor)
        self._workout_sessions_table = WorkoutSessionsTable(self._connection, self._cursor)

    def clear(self) -> None:
        """
        Clears all tables of the database.
        """
        self._exercises_table.clear()
        self._workout_sessions_table.clear()
        self.commit()

    def create(self) -> None:
        """
        Creates 'WorkoutSessions' and 'Exercises' tables.
        """
        self._exercises_table.drop()
        self._workout_sessions_table.drop()
        self._exercises_table.create()
        self._workout_sessions_table.create()
        self.commit()

    def commit(self) -> None:
        """
        Commits the changes to the database.
        """
        self._connection.commit()

    def close(self) -> None:
        """
        Closes the database connection.
        """
        self._connection.close()

    def add_exercise(self, exercise_name: str, alias: str = None, target_muscle_group: str = None) -> None:
        """
        Adds a new exercise to the database.
        :param exercise_name: name of the exercise.
        :param alias: alias of the exercise.
        :param target_muscle_group: target muscle group of the exercise.
        """
        self._exercises_table.add_exercise(exercise_name, alias, target_muscle_group)
        self.commit()

    def add_workout(self,
                    workout_date: date, 
                    exercise_name: str, 
                    order_number: int, 
                    sets: int, 
                    weight: float | list[float] = None, 
                    repetitions: int | list[int] = None, 
                    time: int | list[int] = None, 
                    speed: float | list[float] = None, 
                    units: str = None,
                    feeling: int = None) -> None:
        """
        Adds a new workout_session to the database.
        :param workout_date: date of the workout.
        :param exercise_name: name of the exercise.
        :param order_number: order number of the exercise in the workout.
        :param sets: number of sets (for cardio exercises sets are parts with constant speed).
        :param weight: weight that was used during the workout (in machine or in equipment). If it is a list, it means that the weight 
        was different for each set.
        :param repetitions: number of repetitions. If it is a list, it means that the number of repetitions was different for each set.
        :param time: time in seconds. If it is a list, it means that the time was different for each set.
        :param speed: if it is a list, it means that the speed varied during the exercise.
        :param units: the units of weight on the machine, the weight of an equipment, or the speed (kg/lbs or kph/mph).
        :param feeling: feeling rating (from 1 to 5).
        """
        exercise_id = self._exercises_table.get_exercise_id(exercise_name, may_be_alias=True)
        if exercise_id is None:
            raise ValueError(f'There is no "{exercise_name}" exercise')

        workout = Workout(workout_date, exercise_id, order_number, sets, weight, repetitions, time, speed, units, feeling)
        self._workout_sessions_table.add_workout(workout)
        self.commit()

    def find_workout(self, workout_date: date, exercise_name: str) -> tuple | None:
        """
        Finds a workout with the given date and exercise.
        :param workout_date: date of the workout.
        :param exercise_name: name of the exercise.
        :return: workout or None if no workout with the given date and exercise.
        """
        exercise_id = self._exercises_table.get_exercise_id(exercise_name)
        if exercise_id is None:
            raise ValueError(f'There is no "{exercise_name}" exercise')

        self._cursor.execute("SELECT * FROM WorkoutSessions WHERE date = ? AND exercise_id = ?;", 
                             (workout_date, exercise_id))
        return self._cursor.fetchone()

    def get_all_exercises(self) -> list[str]:
        """
        Gets all exercises.
        :return: list of all exercises.
        """
        return self._exercises_table.get_all_data()
    
    def get_all_workout_sessions(self) -> list[str]:
        """
        Gets all exercises.
        :return: list of all exercises.
        """
        return self._workout_sessions_table.get_all_data()

    def get_all_data(self) -> None:
        """
        Prints all data in the database.
        """
        self._cursor.execute("SELECT * FROM WorkoutSessions WS JOIN Exercises E ON WS.exercise_id = E.id;")
        return self._cursor.fetchall()

    def plot_weights(self, exercise_name: str):
        """
        Plots the weight progression for the given exercise.
        :param exercise_name: name of the exercise.
        """
        pass
