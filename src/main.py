from datetime import date
from database.database import Database


class Interface:
    """
    This class is responsible for interacting with the database.
    """

    def __init__(self, db: Database, clear: bool = False, fill: bool = False) -> None:
        """
        Connects to the database.
        :param db_file: database file to connect to.
        :param clear: if True, clears the database.
        :param clear: if True, fills the database.
        """
        self.db = db
        if clear:
            self.db.create()
            self.db.clear()
        if fill:
            self.fill_exercises()
            self.fill_workouts()
    
    def clear_all(self):
        """
        Clears the database
        """
        self.db.clear()

    def fill_exercises(self) -> None:
        """
        Fills the database with exercises.
        """
        test_set = [
            ['Neutral Pull Up',         'Подтягивания узкие',           'Arms (Biceps)'],
            ['Wide Pull Up',            'Подтягивания широкие',         'Back'],
            ['Leg Extension',           'Ноги снизу вверх (первые 2)',  'Legs (Quadriceps)'],
            ['Seated Row',              'Широчайшие',                   'Back (Lats)'],
            ['Wide Grip Lat Pulldown',  'Спина',                        'Back'],
            ['Seated Leg Curl',         'Ноги сверху вниз (правый)',    'Legs (Hamstrings)'],
            ['Pec Deck',                'Соку бачи вира',               'Chest'],
            ['Cable Rope Pushdown',     'Висюля',                       'Arms (Triceps)'],
            ['Chest Press Machine',     'От сердца к солнцу',           'Chest'],
            ['Treadmill',               'Дорожка',                      'Legs'],
            ['Barbell Curl',            'Бицепс',                       'Arms (Biceps)'],
        ]
        for name, alias, target_muscle_group in test_set:
            self.db.add_exercise(name, alias, target_muscle_group)
        self.db.commit()

    def fill_workouts(self) -> None:
        """
        Fills the database with workout sessions.
        """
        test_set = [
            {
                'workout_date': '2025-03-27', 'exercise_name': 'Neutral Pull Up',   'order_number': 1, 'feeling': 3,
                'sets': 1, 'weight': 20, 'repetitions': 15, 'units': 'kg', 
            },
            {
                'workout_date': '2025-03-27', 'exercise_name': 'Seated Row',        'order_number': 2, 'feeling': 4,
                'sets': 3, 'weight': 35, 'repetitions': 10, 'units': 'kg',
            },
            {
                'workout_date': '2025-03-27', 'exercise_name': 'Treadmill',         'order_number': 3, 'feeling': 5,
                'sets': 1, 'time': 600, 'speed': 5.5, 'units': 'kph',
            },

            {
                'workout_date': '2025-04-05', 'exercise_name': 'Neutral Pull Up',   'order_number': 1, 'feeling': 4,
                'sets': 1, 'weight': 12, 'repetitions': 10, 'units': 'kg', 
            },
            {
                'workout_date': '2025-04-05', 'exercise_name': 'Seated Row',        'order_number': 3, 'feeling': 3,
                'sets': 3, 'weight': [35, 37.5, 37.5], 'repetitions': 10, 'units': 'kg',
            },
            {
                'workout_date': '2025-04-05', 'exercise_name': 'Treadmill',         'order_number': 2, 'feeling': 5,
                'sets': 3, 'time': [180, 240, 180], 'speed': [5.5, 8.5, 5.5], 'units': 'kph',
            },

            {
                'workout_date': '2025-04-18', 'exercise_name': 'Neutral Pull Up',   'order_number': 3, 'feeling': 2,
                'sets': 1, 'weight': 7, 'repetitions': 7, 'units': 'kg', 
            },
            {
                'workout_date': '2025-04-18', 'exercise_name': 'Seated Row',        'order_number': 2, 'feeling': 4,
                'sets': 3, 'weight': 40, 'repetitions': [10, 10, 8], 'units': 'kg',
            },
            {
                'workout_date': '2025-04-18', 'exercise_name': 'Treadmill',         'order_number': 1, 'feeling': 4,
                'sets': 5, 'time': [180, 60, 120, 60, 300], 'speed': [5.5, 6.5, 8.5, 6.5, 5.5], 'units': 'kph',
            },
        ]
        for workout_session in test_set:
            self.db.add_workout(**workout_session)
        self.db.commit()

    def print_all(self) -> None:
        """
        Prints all data in the database.
        """
        for i in self.db.get_all_data():
            print(i)

    # @staticmethod
    # def _input_date() -> date | None:
    #     """
    #     Inputs a date from the user.
    #     :return: date or None if date is invalid or user wants to exit.
    #     """
    #     def _parse_date_input() -> date | None:
    #         """
    #         Parse date from the user.
    #         :return: date or None if date is invalid.
    #         """
    #         try:
    #             if user_input == 't':
    #                 return date.today()
    #             if 2 <= len(user_input):
    #                 for el in user_input:
    #                     if not el.isdigit():
    #                         sep = el
    #                         month, day = map(int, user_input.split(sep))
    #                         break
    #                 else:
    #                     month, day = map(int, [user_input[0], user_input[1:]])
    #                 current_year = date.today().year
    #                 res_date = date(current_year, month, day)
    #                 if res_date > date.today():
    #                     res_date = date(current_year - 1, month, day)
    #                 return res_date
    #         except ValueError:
    #             print("\tIncorrect date format. Please enter the date in mm-dd format.")

    #     res = None
    #     while res is None:
    #         user_input = input('\tEnter date (mm-dd) or "t" for today or "exit" to finish: ').strip().lower()
    #         if user_input == 'exit':
    #             break
    #         res = _parse_date_input()
    #     return res

    @staticmethod
    def _input_num(field_name: str, dest_type: type) -> int | float | None:
        """
        Inputs a number from the user.
        :param field_name: name of the field (used in prints).
        :param dest_type: type of the field (int or float).
        :return: number or None if field is invalid or user wants to exit.
        """
        res = None
        while res is None:
            user_input = input(f'\tEnter {field_name}: ').strip().lower()
            if user_input == 'exit':
                break
            try:
                res = dest_type(user_input)
            except ValueError:
                print(f"\tIncorrect input for type {dest_type}. Please try again.")
        return res

    def _input_exercise(self) -> str | None:
        """
        Inputs an exercise from the user.
        :return: exercise or None if exercise is invalid or user wants to exit.
        """
        def _parse_input_exercise() -> str | None:
            """
            Parse input from the user.
            :return: exercise or None if exercise is invalid.
            """
            try:
                if self.db.get_exercise_id(user_input):
                    return user_input

                y_n_inp = ''
                while y_n_inp != 'n':
                    y_n_inp = input(f'\tThere is no exercise "{user_input}" in the database. '
                                f'Do you want to add it? (y/n): ').strip().lower()
                    if y_n_inp == 'y':
                        self.db.add_exercise(user_input)
                        return user_input
            except ValueError:
                print("\tIncorrect input. Please try again.")

        res = None
        while res is None:
            user_input = input(f'\tEnter an exercise ({", ".join(self.db.get_all_exercises())}): ').strip().lower()
            if user_input == 'exit':
                break
            res = _parse_input_exercise()
        return res

    def add_workout(self) -> tuple | None:
        """
        Adds a workout to the database.
        :return: added workout or None if something went wrong.
        """
        workout_date = self._input_date()
        if workout_date is None:
            return None
        print('-' * 60)

        exercise_name = self._input_exercise()
        if exercise_name is None:
            return None
        print('-' * 60)

        weight = self._input_num('weight', float)
        if weight is None:
            return None
        print('-' * 60)

        feeling_rating = self._input_num('feeling rating(1-5)', int)
        if feeling_rating is None:
            return None
        print('-' * 60)

        description = input('    Enter description: ')

        self.db.add_workout(workout_date, exercise_name, weight, feeling_rating, description)
        self.db.commit()
        return self.db.find_workout(workout_date, exercise_name)

    def add_full_workout_day(self) -> None:
        """
        Adds a full workout day to the database.
        """
        workout_date = self._input_date()
        if workout_date is None:
            return None
        print('-' * 60)
    
        for exercise_name in self.db.get_all_exercises():
            again = True
            while again:
                again = False
                user_input = '-'
                while user_input != 'skip' and user_input != '':
                    user_input = input(f'\n\n"{exercise_name.capitalize()}" ({workout_date}). Enter "Skip" to skip '
                                     f'this exercise or press enter to continue: ').strip().lower()
                if user_input == 'skip':
                    break

                print('-' * 60)
                weight = self._input_num('weight', float)
                if weight is None:
                    return None
                print('-' * 60)
                feeling_rating = self._input_num('feeling rating(1-5)', int)
                if feeling_rating is None:
                    return None
                print('-' * 60)
                description = input('    Enter description: ').strip()
                print('-' * 60)

                user_input = '-'
                while user_input != 'skip' and user_input != 'again' and user_input != '':
                    user_input = input(f'"{exercise_name.capitalize()}" ({workout_date}) {weight}kg {feeling_rating}/5 '
                                       f'({description}). Enter "Skip" to skip this exercise or enter "Again" to edit '
                                       f'current exercise or press enter to continue: ').strip().lower()
                if user_input == 'skip':
                    break
                if user_input == 'again':
                    again = True
                else:
                    self.db.add_workout(workout_date, exercise_name, weight, feeling_rating, description)
        self.db.commit()


def input_date() -> date | None:
    """
    Inputs a date from the user.
    :return: date or None if date is invalid or user wants to exit.
    """
    def _parse_date_input() -> date | None:
        """
        Parse date from the user.
        :return: date or None if date is invalid.
        """
        try:
            if user_input == 't':
                return date.today()
            if 2 <= len(user_input):
                for el in user_input:
                    if not el.isdigit():
                        sep = el
                        month, day = map(int, user_input.split(sep))
                        break
                else:
                    month, day = map(int, [user_input[0], user_input[1:]])
                current_year = date.today().year
                res_date = date(current_year, month, day)
                if res_date > date.today():
                    res_date = date(current_year - 1, month, day)
                return res_date
        except ValueError:
            print("\tIncorrect date format. Please enter the date in mm-dd format.")

    res = None
    while res is None:
        user_input = input('\tEnter date (mm-dd) or "t" for today or "exit" to finish: ').strip().lower()
        if user_input == 'exit':
            break
        res = _parse_date_input()
    return res

'''
# interface = Interface(db_file='gym_tracker.db')

# tip = '0.Exit, 1.Add workout day, 2.Add single workout, 3.Print all'
# tip = '0.Exit, 1.Add workout day, 2.Add single workout, 3.Print all'
# inp = input(f'Enter command ({tip}): ')
# while inp != 'exit' and inp != '0':
#     if inp.lower() in ['add workout day', '1']:
#         interface.add_full_workout_day()

#     if inp.lower() in ['add single workout', '2']:
#         interface.add_full_workout_day()

#     if inp.lower() in ['add single workout', '2']:
#         print(interface.add_workout(), end='\n\n')

#     elif inp.lower() in ['Print all', '3']:
#         interface.print_all()

#     inp = input(f'Enter command ({tip}): ')
'''

# db = Database('src/database/gym_tracker.db')
# i = Interface(db, clear=True)

# i.print_all()
# db.plot_weights('Seated Row')
# db.close()
