import sqlite3
from datetime import date
from .table import Table


class Workout:
    """
    This class describes a workout — doing of one exercise.
    """

    def __init__(self, 
                 schedule_id: str, 
                 sets: int, 
                 weight: float | list[float] = None, 
                 repetitions: int | list[int] = None, 
                 time: int | list[int] = None, 
                 speed: float | list[float] = None, 
                 units: str = None,
                 feeling: int = None,
                 local_order: int = -1) -> None:
        """
        Initializes a workout. Either weight and repetitions (for exercises with machines or additional equipment) or time and speed (for cardio exercises) must be provided.
        :param schedule_id: ID of the record in the Schedule table (id, date, exercise_id, order_number).
        :param sets: number of sets (for cardio exercises sets are parts with constant speed).
        :param weight: weight that was used during the workout (in machine or in equipment). If it is a list, it means that the weight was different for each set.
        :param repetitions: number of repetitions. If it is a list, it means that the number of repetitions was different for each set.
        :param time: time in seconds. If it is a list, it means that the time was different for each set.
        :param speed: if it is a list, it means that the speed varied during the exercise.
        :param units: the units of weight on the machine, the weight of an equipment, or the speed (kg/lbs or kph/mph).
        :param feeling: feeling rating (from 1 to 5).
        :param local_order: number of the current set if there are different values for each set.
        """
        if weight is not None and repetitions is not None:
            self._weight_or_speed = 0
        elif time is not None and speed is not None:
            self._weight_or_speed = 1
        else:
            raise ValueError('Either weight and repetitions (for exercises with machines or additional equipment) or time and speed (for cardio exercises) must be provided.')
            
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
            time = None
            speed = None
        else:
            if isinstance(time, list) ^ isinstance(speed, list):
                raise ValueError('Either all time and speed must be lists or none of them must be lists')
            if isinstance(time, list) and len(time) != sets:
                raise ValueError('The number of times must be equal to the number of sets')
            if isinstance(speed, list) and len(speed) != sets:
                raise ValueError('The number of speeds must be equal to the number of sets')
            if not isinstance(time, list) and local_order == -1 and sets > 1:
                raise ValueError('For cardio exercises, if sets > 1, the record must contain information about each of them')
            weight = None
            repetitions = None


        self._is_list = isinstance(weight, list) or isinstance(repetitions, list) or isinstance(speed, list)

        self.schedule_id = schedule_id
        self.sets = sets
        self.weight = weight
        self.repetitions = repetitions
        self.time = time
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
                schedule_id=self.schedule_id, 
                sets=self.sets, 
                weight=self.weight[i] if self._weight_or_speed == 0 and isinstance(self.weight, list) else self.weight, 
                repetitions=self.repetitions[i] if self._weight_or_speed == 0 and isinstance(self.repetitions, list) else self.repetitions, 
                time=self.time[i] if self._weight_or_speed == 1 else self.time, 
                speed=self.speed[i] if self._weight_or_speed == 1 else self.speed, 
                units=self.units, 
                feeling=self.feeling,
                local_order=i
            ))
        return ans

    def __str__(self) -> str:
        """
        Returns a string representation of the workout session.
        """
        return '{\n'\
               f'\tschedule_id: {self.schedule_id},\n'\
               f'\tsets: {self.sets},\n'\
               f'\tweight: {self.weight},\n'\
               f'\trepetitions: {self.repetitions},\n'\
               f'\ttime: {self.time},\n'\
               f'\tspeed: {self.speed},\n'\
               f'\tunits: {self.units},\n'\
               f'\tfeeling: {self.feeling},\n'\
               f'\tlocal_order: {self.local_order}'\
                '\n}'



class WorkoutsTable(Table):
    """
    This class is responsible for working with the WorkoutsTable table. Workout session describes doing of one exercise.
    """

    def __init__(self, cursor: sqlite3.Cursor) -> None:
        """
        Connects to the database.
        :param cursor: cursor to the database.
        """
        super().__init__('Workouts', cursor)

    def create(self) -> None:
        """
        Creates the table.
        """
        self._cursor.execute("""--sql
            CREATE TABLE IF NOT EXISTS Workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                schedule_id INTEGER NOT NULL,
                feeling INTEGER CHECK(feeling BETWEEN 1 AND 5),
                local_order INTEGER CHECK(local_order >= -1 AND local_order < sets),
                sets INTEGER CHECK(sets > 0),
                weight REAL,
                repetitions INTEGER CHECK(repetitions > 0),
                time INTEGER CHECK(time > 0),
                speed REAL CHECK(speed > 0),
                units TEXT CHECK(units IN ('kg', 'lbs', 'kph', 'mph') OR units IS NULL),
                CHECK(
                    (weight IS NOT NULL AND repetitions IS NOT NULL)
                    OR
                    (time IS NOT NULL AND speed IS NOT NULL)
                ),
                UNIQUE(schedule_id, local_order),
                FOREIGN KEY (schedule_id) REFERENCES Schedule(id)
            );
        """)

    def add_workout(self, workout: Workout) -> None:
        """
        Adds a new workout to the table.
        :param workout: workout to add.
        """
        for w in workout.convert2list():
            self._cursor.execute("""--sql
                INSERT INTO Workouts
                (schedule_id, feeling, local_order, sets, weight, repetitions, time, speed, units)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
            """, (w.schedule_id, w.feeling, w.local_order, w.sets, w.weight, w.repetitions, w.time, w.speed, w.units))
        return self._cursor.lastrowid
    
    def delete_workouts_by_schedule(self, schedule_id: int) -> None:
        """
        Deletes all workouts for the given schedule record.
        :param schedule_id: ID of the schedule record.
        """
        self._cursor.execute("""--sql
            DELETE FROM Workouts
            WHERE schedule_id = ?;
        """, (schedule_id,))
