import sqlite3
from datetime import date, datetime
from .tables.exercises import ExercisesTable
from .tables.workouts import Workout, WorkoutsTable
from .tables.schedule import ScheduleTable
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter

class Database:
    """
    SQLite wrapper to work with exercises, schedule and workouts tables.
    Provides CRUD operations and helper queries.
    """

    def __init__(self, db_file: str) -> None:
        """
        Connect to the database and initialize table objects.

        :param db_file: path to SQLite database file
        """
        self._connection = sqlite3.connect(db_file)
        self._cursor = self._connection.cursor()
        self._exercises_table = ExercisesTable(self._cursor)
        self._workouts_table = WorkoutsTable(self._cursor)
        self._schedule_table = ScheduleTable(self._cursor)

    def clear(self) -> None:
        """
        Clear all tables completely.
        """
        self._exercises_table.clear()
        self._workouts_table.clear()
        self._schedule_table.clear()
        self.commit()

    def create(self) -> None:
        """
        Re-create tables `Exercises`, `Workouts`, `Schedule`.
        """
        self._exercises_table.drop()
        self._workouts_table.drop()
        self._schedule_table.drop()
        self._exercises_table.create()
        self._workouts_table.create()
        self._schedule_table.create()
        self.commit()

    def commit(self) -> None:
        """
        Commit current transaction.
        """
        self._connection.commit()

    def close(self) -> None:
        """
        Close the database connection.
        """
        self._connection.close()

    def get_columns(self) -> list[str]:
        """
        Return column names of the last executed query.

        :return: list of column names
        """
        if hasattr(self._cursor, 'description'):
            return [desc[0] for desc in self._cursor.description]
        return []

    def add_exercise(self, exercise_name: str, alias: str = None, target_muscle_group: str = None) -> None:
        """
        Add an exercise.

        :param exercise_name: exercise name
        :param alias: alias
        :param target_muscle_group: target muscle group
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
        Add a workout session.

        :param workout_date: date
        :param exercise_name: exercise name (or alias)
        :param order_number: exercise order in the day
        :param sets: number of sets (for cardio: parts with constant speed)
        :param weight: weight(s)
        :param repetitions: repetitions
        :param time: time(s)
        :param speed: speed(s)
        :param units: measurement units ('kg'/'lbs' or 'kph'/'mph')
        :param feeling: feeling score (1..5)
        """
        exercise_id = self._exercises_table.get_exercise_id(exercise_name, may_be_alias=True)
        if exercise_id is None:
            raise ValueError(f'There is no "{exercise_name}" exercise')
        
        schedule_id = self._schedule_table.add_schedule_record(workout_date, exercise_id, order_number)
        workout = Workout(schedule_id, sets, weight, repetitions, time, speed, units, feeling)
        self._workouts_table.add_workout(workout)
        self.commit()

    def find_workout(self, workout_date: date, exercise_name: str) -> tuple | None:
        """
        Find records by date and exercise.

        :return: list of rows or empty list
        """
        exercise_id = self._exercises_table.get_exercise_id(exercise_name)
        if exercise_id is None:
            raise ValueError(f'There is no "{exercise_name}" exercise')

        self._cursor.execute("""--sql
            SELECT S.id, S.date, S.exercise_id, S.order_number, W.id, W.feeling, W.local_order, W.sets, W.weight, W.repetitions, W.time, W.speed, W.units
            FROM Schedule S
            JOIN Workouts W ON S.id = W.schedule_id
            WHERE S.date = ? AND S.exercise_id = ?;
        """, (workout_date, exercise_id))
        return self._cursor.fetchall()

    def get_all_exercises(self) -> list[list[str]]:
        """
        Return all rows from `Exercises`.

        :return: list of tuples
        """
        return self._exercises_table.get_all_data()
    
    def get_all_schedule(self) -> list[list[str]]:
        """
        Return all rows from `Schedule`.
        """
        return self._schedule_table.get_all_data()

    def get_all_workouts(self) -> list[list[str]]:
        """
        Return all rows from `Workouts`.
        """
        return self._workouts_table.get_all_data()

    def print_all_data(self) -> None:
        """
        Print contents of all tables with separators.
        """
        border = '=' * 80
        sep = '-' * 60
        for i in (
            border,
            self.get_all_exercises(),
            self.get_columns(),
            sep,
            self.get_all_schedule(),
            self.get_columns(),
            sep,
            self.get_all_workouts(),
            self.get_columns(),
            border,
        ):
            print(i)

    def plot_weights(self, exercise_name: str):
        """
        Plot average weight by date for the given exercise.
        """
        self._cursor.execute("""--sql
            SELECT S.date, W.weight
            FROM Workouts W
            JOIN Schedule S ON W.schedule_id = S.id
            JOIN Exercises E ON S.exercise_id = E.id
            WHERE E.name = ?
        """, (exercise_name,))

        date_weight = {}
        for d, w in self._cursor.fetchall():
            if d not in date_weight:
                date_weight[d] = []
            date_weight[d].append(w)

        dates = []
        weights = []
        for date in date_weight:
            dates.append(datetime.strptime(date, '%Y-%m-%d'))
            w = date_weight[date]
            weights.append(sum(w) / len(w))

        plt.figure(figsize=(8, 5))
        plt.plot(dates, weights, marker='o')

        plt.gca().xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
        plt.xticks(dates)

        plt.xlabel('Date')
        plt.ylabel('Weight')
        plt.title(f'{exercise_name} weight progression')

        plt.grid(True)
        plt.show()

    def delete_exercise(self, exercise_name: str) -> None:
        """
        Delete an exercise and all related schedule/workout records.
        """
        exercise_id = self._exercises_table.get_exercise_id(exercise_name, may_be_alias=True)
        if exercise_id is None:
            raise ValueError(f'There is no "{exercise_name}" exercise')
        
        # Delete related workouts first
        for schedule_id in self._get_schedule_ids_by_exercise(exercise_id):
            self._workouts_table.delete_workouts_by_schedule(schedule_id)
        
        # Delete schedule records
        self._schedule_table.delete_schedule_by_exercise(exercise_id)
        
        # Delete the exercise
        self._exercises_table.delete_by_id(exercise_id)
        self.commit()

    def delete_workout(self, workout_date: date, exercise_name: str) -> None:
        """
        Delete workouts for the given date and exercise.
        """
        exercise_id = self._exercises_table.get_exercise_id(exercise_name, may_be_alias=True)
        if exercise_id is None:
            raise ValueError(f'There is no "{exercise_name}" exercise')
        
        # Find schedule record
        self._cursor.execute("""--sql
            SELECT id FROM Schedule
            WHERE date = ? AND exercise_id = ?;
        """, (workout_date, exercise_id))
        
        schedule_record = self._cursor.fetchone()
        if schedule_record is None:
            raise ValueError(f'No workout found for {exercise_name} on {workout_date}')
        
        schedule_id = schedule_record[0]
        
        # Delete workouts
        self._workouts_table.delete_workouts_by_schedule(schedule_id)
        
        # Delete schedule record
        self._schedule_table.delete_by_id(schedule_id)
        self.commit()

    def delete_workout_by_date(self, workout_date: date) -> None:
        """
        Delete all workouts for the given date.
        """        
        # Delete schedule records
        schedule_ids_to_delete = self._schedule_table.delete_schedule_by_date(workout_date)
        
        # Delete workouts first
        for schedule_id in schedule_ids_to_delete:
            self._workouts_table.delete_workouts_by_schedule(schedule_id)

        self.commit()

    def _get_schedule_ids_by_exercise(self, exercise_id: int) -> list[int]:
        """
        Return all schedule IDs for the exercise.
        """
        self._cursor.execute("""--sql
            SELECT id FROM Schedule
            WHERE exercise_id = ?;
        """, (exercise_id,))
        return [row[0] for row in self._cursor.fetchall()]
    
    def get_exercise_id(self, exercise_name: str, may_be_alias: bool = True) -> int | None:
        """
        Gets exercise ID by name.
        :param exercise_name: name of the exercise.
        :param may_be_alias: whether to search in aliases too.
        :return: exercise ID or None if not found.
        """
        return self._exercises_table.get_exercise_id(exercise_name, may_be_alias)

    def get_workouts_by_date(self, workout_date: date) -> list[tuple]:
        """
        Gets all workouts for the given date.
        :param workout_date: date of the workout.
        :return: list of workout records.
        """
        self._cursor.execute("""--sql
            SELECT S.id, E.name, S.order_number, W.id, W.sets, W.weight, W.repetitions, W.time, W.speed, W.units, W.feeling
            FROM Schedule S
            JOIN Exercises E ON S.exercise_id = E.id
            LEFT JOIN Workouts W ON S.id = W.schedule_id
            WHERE S.date = ?
            ORDER BY S.order_number;
        """, (workout_date,))
        return self._cursor.fetchall()

    def get_all_dates(self) -> list[date]:
        """
        Gets all dates with workouts.
        :return: list of dates.
        """
        self._cursor.execute("""--sql
            SELECT DISTINCT date
            FROM Schedule
            ORDER BY date;
        """)
        return [datetime.strptime(row[0], '%Y-%m-%d').date() for row in self._cursor.fetchall()]
