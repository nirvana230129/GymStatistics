import sqlite3
from datetime import date

from table import Table


class Workout:
    """
    This class describes a workout session.
    """

    def __init__(self, 
                 workout_date: date, 
                 exercise_id: str, 
                 order_number: int, 
                 weight: float | list[float] = None, 
                 weight_unit: str = None, 
                 repetitions: int = None, 
                 sets: int = None, 
                 time_in_seconds: int | list[int] = None, 
                 distance_in_meters: int | list[int] = None, 
                 feeling: int = None,
                 local_order: int = 0) -> None:
        """
        Initializes a workout session.
        :param workout_date: date of the workout.
        :param exercise_id: ID of the exercise.
        :param order_number: order number of the exercise in the workout.
        :param weight: weight that was used during the workout. If it is a list, it means that the weight was different for each set.
        :param weight_unit: unit of the weight (kg or lbs).
        :param repetitions: number of repetitions.
        :param sets: number of sets.
        :param time_in_seconds: time in seconds. If it is a list, it means that the time was different for each set.
        :param distance_in_meters: distance in meters. If it is a list, it means that the distance was different for each set.
        :param feeling: feeling rating (from 1 to 5).
        :param local_order: local order of the workout in the workout session.
        """
        if weight is not None and weight_unit is not None and repetitions is not None and sets is not None:
            self._weight_or_distance = 0
        elif time_in_seconds is not None and distance_in_meters is not None:
            self._weight_or_distance = 1
        else:
            raise ValueError('Either weight and weight_unit and repetitions and sets or time_in_seconds and distance_in_meters must be provided')
            
        if isinstance(weight, list) and len(weight) != sets:
            raise ValueError('The number of weights must be equal to the number of sets')
        
        if isinstance(distance_in_meters, list) ^ isinstance(time_in_seconds, list):
            raise ValueError('Either all time_in_seconds and distance_in_meters must be lists or none of them must be lists')
        if isinstance(time_in_seconds, list) and isinstance(distance_in_meters, list) and not (len(time_in_seconds) == len(distance_in_meters) == sets):
            raise ValueError('The number of time_in_seconds must be equal to the number of distance_in_meters and equal to the number of sets')

        self._is_list = isinstance(weight, list) or isinstance(distance_in_meters, list)

        self.workout_date = workout_date
        self.exercise_id = exercise_id
        self.order_number = order_number
        self.weight = weight
        self.weight_unit = weight_unit
        self.repetitions = repetitions
        self.sets = sets
        self.time_in_seconds = time_in_seconds
        self.distance_in_meters = distance_in_meters
        self.feeling = feeling

        self.local_order = local_order

    def cast2list(self) -> list['Workout']:
        """
        Casts the workout to a list of workouts.
        """
        if not self._is_list:
            return [self]
        
        ans = []
        for i in range(self.sets):
            ans.append(Workout(
                workout_date=self.workout_date, 
                exercise_id=self.exercise_id, 
                order_number=self.order_number,
                weight=self.weight[i] if self._weight_or_distance == 0 else self.weight, 
                weight_unit=self.weight_unit, 
                repetitions=self.repetitions, 
                sets=1, 
                time_in_seconds=self.time_in_seconds[i] if self._weight_or_distance == 1 else self.time_in_seconds, 
                distance_in_meters=self.distance_in_meters[i] if self._weight_or_distance == 1 else self.distance_in_meters, 
                feeling=self.feeling,
                local_order=self.local_order + i
            ))
        return ans

    def __str__(self) -> str:
        """
        Returns a string representation of the workout session.
        """
        return '{\n'\
               f'\tworkout_date: {self.workout_date},\n'\
               f'\texercise_id: {self.exercise_id},\n'\
               f'\torder_number: {self.order_number},\n'\
               f'\tweight: {self.weight},\n'\
               f'\tweight_unit: {self.weight_unit},\n'\
               f'\trepetitions: {self.repetitions},\n'\
               f'\tsets: {self.sets},\n'\
               f'\ttime_in_seconds: {self.time_in_seconds},\n'\
               f'\tdistance_in_meters: {self.distance_in_meters},\n'\
               f'\tfeeling: {self.feeling},\n'\
               '\n}'



class WorkoutSessionsTable(Table):
    """
    This class is responsible for working with the WorkoutSessions table.
    """

    def __init__(self, connection: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
        """
        Connects to the database.
        :param connection: connection to the database.
        :param cursor: cursor to the database.
        """
        super().__init__('WorkoutSessions', connection, cursor)

    def create(self) -> None:
        """
        Creates the table.
        """
        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS WorkoutSessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE NOT NULL,
                exercise_id INTEGER NOT NULL,
                order_number INTEGER NOT NULL,
                weight REAL,
                weight_unit TEXT CHECK(weight_unit IN ('kg', 'lbs') OR weight_unit IS NULL),
                repetitions INTEGER,
                sets INTEGER,
                time_in_seconds INTEGER,
                distance_in_meters INTEGER,
                feeling INTEGER CHECK(feeling BETWEEN 1 AND 5),
                local_order INTEGER CHECK(local_order >= 0 AND local_order < sets),
                FOREIGN KEY (exercise_id) REFERENCES Exercises(id),
                CHECK (
                    (weight IS NOT NULL AND weight_unit IS NOT NULL AND repetitions IS NOT NULL AND sets IS NOT NULL)
                    OR
                    (time_in_seconds IS NOT NULL AND distance_in_meters IS NOT NULL)
                )
            );
        ''')

    def add_workout_session(self, workout_session: Workout) -> None:
        """
        Adds a new workout to the database.
        :param workout: workout to add.
        """
        for w in workout_session.cast2list():
            try:
                self._cursor.execute(f'''
                    INSERT INTO WorkoutSessions 
                    (date, exercise_id, order_number, weight, weight_unit, repetitions, sets, time_in_seconds, distance_in_meters, feeling, local_order)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                ''', (w.workout_date, w.exercise_id, w.order_number, w.weight, 
                    w.weight_unit, w.repetitions, w.sets, w.time_in_seconds, 
                    w.distance_in_meters, w.feeling, w.local_order)
                )
            except sqlite3.IntegrityError:
                raise Exception(f'Workout with {workout_session.exercise_id} on {workout_session.workout_date} already exists')

    def add_workout_session(self, workout_sessions: list[Workout]) -> None:
        """
        Adds a new workout session to the database.
        :param workout_sessions: list of workout sessions to add.
        """
        for workout_session in workout_sessions:
            self.add_workout(workout_session)
