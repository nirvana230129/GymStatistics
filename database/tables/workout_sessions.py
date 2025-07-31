import sqlite3
from datetime import date

from table import Table


class Workout:
    """
    This class describes a workout — doing of one exercise.
    """

    def __init__(self, 
                 workout_date: date, 
                 exercise_id: str, 
                 order_number: int, 
                 sets: int, 
                 weight: float | list[float] = None, 
                 repetitions: int | list[int] = None, 
                 time_in_seconds: int | list[int] = None, 
                 speed: float | list[float] = None, 
                 units: str = None,
                 feeling: int = None,
                 local_order: int = 0) -> None:
        """
        Initializes a workout. Either weight and repetitions (for exercises with machines or additional equipment) or time_in_seconds and speed (for cardio exercises) must be provided.
        :param workout_date: date of the workout.
        :param exercise_id: ID of the exercise.
        :param order_number: order number of the exercise in the workout.
        :param sets: number of sets (for cardio exercises sets are parts with constant speed).
        :param weight: weight that was used during the workout (in machine or in equipment). If it is a list, it means that the weight was different for each set.
        :param repetitions: number of repetitions. If it is a list, it means that the number of repetitions was different for each set.
        :param time_in_seconds: if it is a list, it means that the time was different for each set.
        :param speed: if it is a list, it means that the speed varied during the exercise.
        :param units: the units of weight on the machine, the weight of an equipment, or the speed (kg/lbs or kph/mph).
        :param feeling: feeling rating (from 1 to 5).
        :param local_order: local order of the workout in the workout session.
        """
        if weight is not None and repetitions is not None:
            self._weight_or_speed = 0
        elif time_in_seconds is not None and speed is not None:
            self._weight_or_speed = 1
        else:
            raise ValueError('Either weight and repetitions (for exercises with machines or additional equipment) or time_in_seconds and speed (for cardio exercises) must be provided.')
            
        if feeling is not None and not 1 <= feeling <= 5:
            raise ValueError("Feeling rating must be from 1 to 5")
        if units is not None:
            if self._weight_or_speed == 0 and units not in ['kg', 'lbs']:
                raise ValueError("Units must be 'kg' or 'lbs' for weights exercises")
            if self._weight_or_speed == 1 and units not in ['kph', 'mph']:
                raise ValueError("Units must be 'kph' or 'mph' for cardio exercises")

        if self._weight_or_speed == 0:
            if isinstance(weight, list) and len(weight) != sets:
                raise ValueError('The number of weights must be equal to the number of sets')
            if isinstance(repetitions, list) and len(repetitions) != sets:
                raise ValueError('The number of repetitions must be equal to the number of sets')
            time_in_seconds = None
            speed = None
        else:
            if isinstance(time_in_seconds, list) and len(time_in_seconds) != sets:
                raise ValueError('The number of times must be equal to the number of sets')
            if isinstance(speed, list) and len(speed) != sets:
                raise ValueError('The number of speeds must be equal to the number of sets')
            if isinstance(time_in_seconds, list) ^ isinstance(speed, list):
                raise ValueError('Either all time_in_seconds and speed must be lists or none of them must be lists')
            weight = None
            repetitions = None


        self._is_list = isinstance(weight, list) or isinstance(speed, list)

        self.workout_date = workout_date
        self.exercise_id = exercise_id
        self.order_number = order_number
        self.sets = sets
        self.weight = weight
        self.repetitions = repetitions
        self.time_in_seconds = time_in_seconds
        self.speed = speed
        self.units = units
        self.feeling = feeling

        self.local_order = local_order

    def convert2list(self) -> list['Workout']:
        """
        Converts the workout into a list of workouts if there is different information for sets. If there is no difference among sets returns list just with current wotkout.
        """
        if not self._is_list:
            return [self]
        
        ans = []
        for i in range(self.sets):
            ans.append(Workout(
                workout_date=self.workout_date, 
                exercise_id=self.exercise_id, 
                order_number=self.order_number,
                sets=1, 
                weight=self.weight[i] if self._weight_or_speed == 0 else self.weight, 
                repetitions=self.repetitions[i] if self._weight_or_speed == 0 and isinstance(self.repetitions, list) else self.repetitions, 
                time_in_seconds=self.time_in_seconds[i] if self._weight_or_speed == 1 else self.time_in_seconds, 
                speed=self.speed[i] if self._weight_or_speed == 1 else self.speed, 
                units=self.units, 
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
               f'\tsets: {self.sets},\n'\
               f'\tweight: {self.weight},\n'\
               f'\trepetitions: {self.repetitions},\n'\
               f'\ttime_in_seconds: {self.time_in_seconds},\n'\
               f'\tspeed: {self.speed},\n'\
               f'\tunits: {self.units},\n'\
               f'\tfeeling: {self.feeling},\n'\
               f'\tlocal_order: {self.local_order},\n'\
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
                weight_unit TEXT CHECK(weight_unit IN ('kg', 'lbs', 'kph', 'mph') OR weight_unit IS NULL),
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

    def add_workout(self, workout: Workout) -> None:
        """
        Adds a new workout to the table.
        :param workout: workout to add.
        """
        for w in workout.convert2list():
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
                raise Exception(f'Workout with {workout.exercise_id} on {workout.workout_date} already exists')

    def add_workout_session(self, workout_sessions: list[Workout]) -> None:
        """
        Adds a new workout session to the table.
        :param workout_sessions: list of workout sessions to add.
        """
        for workout_session in workout_sessions:
            self.add_workout(workout_session)
