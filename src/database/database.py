import sqlite3
from datetime import date

from tables.exercises import ExercisesTable
from tables.workout_sessions import Workout, WorkoutSessionsTable


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
        self._workouts_table = WorkoutSessionsTable(self._connection, self._cursor)

    def drop(self) -> None:
        """
        Clears the database.
        """
        self._exercises_table.drop()
        self._workouts_table.drop()

    def create(self) -> None:
        """
        Creates 'Workouts' and 'Exercises' tables.
        """
        self._exercises_table.create()
        self._workouts_table.create()

    def commit(self) -> None:
        """
        Commits the changes to the database.
        """
        self._connection.commit()

    def add_exercise(self, exercise_name: str, alias: str = None, target_muscle_group: str = None) -> None:
        """
        Adds a new exercise to the database.
        :param exercise_name: name of the exercise.
        :param alias: alias of the exercise.
        :param target_muscle_group: target muscle group of the exercise.
        """
        self._exercises_table.add_exercise(exercise_name, alias, target_muscle_group)

    def add_workout(self,
                    workout_date: date, 
                    exercise_name: str, 
                    order_number: int, 
                    weight: float | list[float] = None, 
                    weight_unit: str = None, 
                    repetitions: int = None, 
                    sets: int = None, 
                    time_in_seconds: int | list[int] = None, 
                    distance_in_meters: int | list[int] = None, 
                    feeling: int = None) -> None:
        """
        Adds a new workout_session to the database.
        :param workout_date: date of the workout.
        :param exercise_name: name of the exercise.
        :param order_number: order number of the exercise in the workout.
        :param weight: weight that was used during the workout. If it is a list, it means that the weight was different for each set.
        :param weight_unit: unit of the weight (kg or lbs).
        :param repetitions: number of repetitions.
        :param sets: number of sets.
        :param time_in_seconds: time in seconds. If it is a list, it means that the time was different for each set.
        :param distance_in_meters: distance in meters. If it is a list, it means that the distance was different for each set.
        :param feeling: feeling rating (from 1 to 5).
        """
        exercise_id = self._exercises_table.get_exercise_id(exercise_name, may_be_alias=True)
        if exercise_id is None:
            raise ValueError(f'There is no "{exercise_name}" exercise')

        workout = Workout(workout_date, exercise_id, order_number, weight, weight_unit, repetitions, sets, time_in_seconds, distance_in_meters, feeling)
        self._workouts_table.add_workout(workout)

    def find_workout(self, workout_date: date, exercise_name: str) -> tuple | None:
        """
        Finds a workout with the given date and exercise ID.
        :param workout_date: date of the workout.
        :param exercise_name: name of the exercise.
        :return: workout or None if no workout with the given date and exercise ID.
        """
        exercise_id = self.get_exercise_id(exercise_name)
        if exercise_id is not None:
            self._cursor.execute('SELECT * FROM Workouts WHERE date = ? AND exercise_id = ?;',
                                 (workout_date, exercise_id))
            data = self._cursor.fetchone()
            return data or None

    def get_all_exercises(self) -> list[str]:
        """
        Gets all exercises.
        :return: list of all exercises.
        """
        return self._exercises_table.get_all_data()

    def print_all_data(self) -> None:
        """
        Prints all data in the database.
        """
        self._cursor.execute('SELECT * FROM WorkoutSessions WS JOIN Exercises E ON WS.exercise_id = E.id;')
        data = self._cursor.fetchall()
        print(*data, sep='\n', end='\n\n')

    def print_all_data_old(self) -> None:
        """
        Prints all data in the database.
        """
        self._cursor.execute('SELECT * FROM Workouts W JOIN Exercises E ON W.exercise_id = E.id;')
        data = self._cursor.fetchall()
        print(*data, sep='\n', end='\n\n')

    def plot_weights(self, exercise_name: str):
        """
        Plots the weight progression for the given exercise.
        :param exercise_name: name of the exercise.
        """
        pass