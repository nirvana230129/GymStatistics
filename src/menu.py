from datetime import date, datetime
from database.database import Database


class Interface:
    """
    Класс для взаимодействия с базой данных и отображения меню.
    """

    def __init__(self, db: Database, clear: bool = False, fill: bool = False) -> None:
        self.db = db
        if clear:
            self.db.create()
            self.db.clear()
        if fill:
            self.fill_exercises()
            self.fill_workouts()

    def clear_all(self):
        self.db.clear()

    def fill_exercises(self) -> None:
        test_set = [
            ['Neutral Pull Up', 'Подтягивания узкие', 'Arms (Biceps)'],
            ['Wide Pull Up', 'Подтягивания широкие', 'Back'],
            ['Leg Extension', 'Ноги снизу вверх (первые 2)', 'Legs (Quadriceps)'],
            ['Seated Row', 'Широчайшие', 'Back (Lats)'],
            ['Wide Grip Lat Pulldown', 'Спина', 'Back'],
            ['Seated Leg Curl', 'Ноги сверху вниз (правый)', 'Legs (Hamstrings)'],
            ['Pec Deck', 'Соку бачи вира', 'Chest'],
            ['Cable Rope Pushdown', 'Висюля', 'Arms (Triceps)'],
            ['Chest Press Machine', 'От сердца к солнцу', 'Chest'],
            ['Treadmill', 'Дорожка', 'Legs'],
            ['Barbell Curl', 'Бицепс', 'Arms (Biceps)'],
        ]
        for name, alias, target_muscle_group in test_set:
            self.db.add_exercise(name, alias, target_muscle_group)
        self.db.commit()

    def fill_workouts(self) -> None:
        test_set = [
            {
                'workout_date': '2025-03-27', 'exercise_name': 'Neutral Pull Up', 'order_number': 1, 'feeling': 3,
                'sets': 1, 'weight': 20, 'repetitions': 15, 'units': 'kg',
            },
            {
                'workout_date': '2025-03-27', 'exercise_name': 'Seated Row', 'order_number': 2, 'feeling': 4,
                'sets': 3, 'weight': 35, 'repetitions': 10, 'units': 'kg',
            },
            {
                'workout_date': '2025-03-27', 'exercise_name': 'Treadmill', 'order_number': 3, 'feeling': 5,
                'sets': 1, 'time': 600, 'speed': 5.5, 'units': 'kph',
            },
            {
                'workout_date': '2025-04-05', 'exercise_name': 'Neutral Pull Up', 'order_number': 1, 'feeling': 4,
                'sets': 1, 'weight': 12, 'repetitions': 10, 'units': 'kg',
            },
            {
                'workout_date': '2025-04-05', 'exercise_name': 'Seated Row', 'order_number': 3, 'feeling': 3,
                'sets': 3, 'weight': [35, 37.5, 37.5], 'repetitions': 10, 'units': 'kg',
            },
            {
                'workout_date': '2025-04-05', 'exercise_name': 'Treadmill', 'order_number': 2, 'feeling': 5,
                'sets': 3, 'time': [180, 240, 180], 'speed': [5.5, 8.5, 5.5], 'units': 'kph',
            },
            {
                'workout_date': '2025-04-18', 'exercise_name': 'Neutral Pull Up', 'order_number': 3, 'feeling': 2,
                'sets': 1, 'weight': 7, 'repetitions': 7, 'units': 'kg',
            },
            {
                'workout_date': '2025-04-18', 'exercise_name': 'Seated Row', 'order_number': 2, 'feeling': 4,
                'sets': 3, 'weight': 40, 'repetitions': [10, 10, 8], 'units': 'kg',
            },
            {
                'workout_date': '2025-04-18', 'exercise_name': 'Treadmill', 'order_number': 1, 'feeling': 4,
                'sets': 5, 'time': [180, 60, 120, 60, 300], 'speed': [5.5, 6.5, 8.5, 6.5, 5.5], 'units': 'kph',
            },
        ]
        for workout_session in test_set:
            self.db.add_workout(**workout_session)
        self.db.commit()

    def print_all(self) -> None:
        for i in self.db.print_all_data():
            print(i)

    def _input_exercise(self) -> str | None:
        def _parse_input_exercise() -> str | None:
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

    def show_exercises(self) -> None:
        exercises = self.db.get_exercises_list()
        if not exercises:
            print("В базе данных нет упражнений.")
            return

        print("\nСписок упражнений:")
        print("-" * 80)
        print(f"{'ID':<5} {'Название':<30} {'Псевдоним':<20} {'Группа мышц':<20}")
        print("-" * 80)
        for ex_id, name, alias, muscle_group in exercises:
            print(f"{ex_id:<5} {name:<30} {(alias or ''):<20} {(muscle_group or ''):<20}")

    def show_dates(self) -> None:
        dates = self.db.get_all_dates()
        if not dates:
            print("В базе данных нет тренировок.")
            return

        print("\nСписок дат с тренировками:")
        print("-" * 30)
        for i, workout_date in enumerate(dates, 1):
            print(f"{i}. {workout_date}")

    def show_workouts_by_date(self, workout_date: date) -> None:
        workouts = self.db.get_workouts_by_date(workout_date)
        if not workouts:
            print(f"На {workout_date} нет тренировок.")
            return

        print(f"\nТренировки на {workout_date}:")
        print("-" * 100)
        print(f"{'ID':<5} {'Упражнение':<25} {'Порядок':<8} {'Подходы':<8} {'Вес':<8} {'Повторения':<12} {'Время':<8} {'Скорость':<10} {'Единицы':<8}")
        print("-" * 100)

        for schedule_id, exercise_name, order_num, workout_id, sets, weight, reps, time, speed, units, feeling in workouts:
            if workout_id:
                print(f"{workout_id:<5} {exercise_name:<25} {order_num:<8} {sets:<8} {(str(weight) if weight else ''):<8} {(str(reps) if reps else ''):<12} {(str(time) if time else ''):<8} {(str(speed) if speed else ''):<10} {(units or ''):<8}")
            else:
                print(f"{'N/A':<5} {exercise_name:<25} {order_num:<8} {'N/A':<8} {'N/A':<8} {'N/A':<12} {'N/A':<8} {'N/A':<10} {'N/A':<8}")

    def delete_exercise_interactive(self) -> None:
        self.show_exercises()
        if not self.db.get_exercises_list():
            return
        try:
            exercise_name = input("\nВведите название упражнения для удаления: ").strip()
            if not exercise_name:
                print("Отменено.")
                return
            confirm = input(f"Вы уверены, что хотите удалить упражнение '{exercise_name}' и все связанные данные? (y/N): ").strip().lower()
            if confirm == 'y':
                self.db.delete_exercise(exercise_name)
                print(f"Упражнение '{exercise_name}' успешно удалено.")
            else:
                print("Удаление отменено.")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def delete_workout_by_date_interactive(self) -> None:
        self.show_dates()
        if not self.db.get_all_dates():
            return
        try:
            date_str = input("\nВведите дату тренировки для удаления (YYYY-MM-DD): ").strip()
            if not date_str:
                print("Отменено.")
                return
            workout_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            self.show_workouts_by_date(workout_date)
            confirm = input(f"Вы уверены, что хотите удалить все тренировки на {workout_date}? (y/N): ").strip().lower()
            if confirm == 'y':
                self.db.delete_workout_by_date(workout_date)
                print(f"Все тренировки на {workout_date} успешно удалены.")
            else:
                print("Удаление отменено.")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def delete_specific_workout_interactive(self) -> None:
        self.show_dates()
        if not self.db.get_all_dates():
            return
        try:
            date_str = input("\nВведите дату тренировки (YYYY-MM-DD): ").strip()
            if not date_str:
                print("Отменено.")
                return
            workout_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            self.show_workouts_by_date(workout_date)
            exercise_name = input("Введите название упражнения для удаления: ").strip()
            if not exercise_name:
                print("Отменено.")
                return
            confirm = input(f"Вы уверены, что хотите удалить тренировку '{exercise_name}' на {workout_date}? (y/N): ").strip().lower()
            if confirm == 'y':
                self.db.delete_workout(workout_date, exercise_name)
                print(f"Тренировка '{exercise_name}' на {workout_date} успешно удалена.")
            else:
                print("Удаление отменено.")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def run_delete_menu(self) -> None:
        while True:
            print("\n" + "="*50)
            print("МЕНЮ УДАЛЕНИЯ ДАННЫХ")
            print("="*50)
            print("1. Показать все упражнения")
            print("2. Показать все даты с тренировками")
            print("3. Показать тренировки по дате")
            print("4. Удалить упражнение")
            print("5. Удалить все тренировки по дате")
            print("6. Удалить конкретную тренировку")
            print("0. Вернуться в главное меню")

            choice = input("\nВыберите действие (0-6): ").strip()

            if choice == '0':
                print("Возврат в главное меню.")
                break
            elif choice == '1':
                self.show_exercises()
            elif choice == '2':
                self.show_dates()
            elif choice == '3':
                try:
                    date_str = input("Введите дату (YYYY-MM-DD): ").strip()
                    if date_str:
                        workout_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                        self.show_workouts_by_date(workout_date)
                except ValueError:
                    print("Неверный формат даты. Используйте YYYY-MM-DD.")
            elif choice == '4':
                self.delete_exercise_interactive()
            elif choice == '5':
                self.delete_workout_by_date_interactive()
            elif choice == '6':
                self.delete_specific_workout_interactive()
            else:
                print("Неверный выбор. Попробуйте снова.")

    def run_main_menu(self) -> None:
        while True:
            print("\n" + "="*50)
            print("ГЛАВНОЕ МЕНЮ")
            print("="*50)
            print("1. Добавить упражнение")
            print("2. Добавить тренировку")
            print("3. Найти тренировку")
            print("4. Показать все данные")
            print("5. Построить график прогресса")
            print("6. Управление удалением данных")
            print("0. Выход")

            choice = input("\nВыберите действие (0-6): ").strip()

            if choice == '0':
                print("До свидания!")
                break
            elif choice == '1':
                self.add_exercise_interactive()
            elif choice == '2':
                self.add_workout_interactive()
            elif choice == '3':
                self.find_workout_interactive()
            elif choice == '4':
                self.show_all_data()
            elif choice == '5':
                self.plot_progress_interactive()
            elif choice == '6':
                self.run_delete_menu()
            else:
                print("Неверный выбор. Попробуйте снова.")

    def add_exercise_interactive(self) -> None:
        try:
            exercise_name = input("Введите название упражнения: ").strip()
            if not exercise_name:
                print("Отменено.")
                return
            alias = input("Введите псевдоним (необязательно): ").strip()
            if not alias:
                alias = None
            target_muscle_group = input("Введите целевую группу мышц (необязательно): ").strip()
            if not target_muscle_group:
                target_muscle_group = None
            self.db.add_exercise(exercise_name, alias, target_muscle_group)
            print(f"Упражнение '{exercise_name}' успешно добавлено.")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def add_workout_interactive(self) -> None:
        try:
            date_str = input("Введите дату тренировки (YYYY-MM-DD): ").strip()
            if not date_str:
                print("Отменено.")
                return
            workout_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            exercise_name = input("Введите название упражнения: ").strip()
            if not exercise_name:
                print("Отменено.")
                return
            order_str = input("Введите порядковый номер упражнения: ").strip()
            if not order_str:
                print("Отменено.")
                return
            order_number = int(order_str)
            sets_str = input("Введите количество подходов: ").strip()
            if not sets_str:
                print("Отменено.")
                return
            sets = int(sets_str)
            exercise_type = input("Тип упражнения (1 - силовое, 2 - кардио): ").strip()
            weight = None
            repetitions = None
            time = None
            speed = None
            units = None
            if exercise_type == '1':
                weight_str = input("Введите вес (кг): ").strip()
                if weight_str:
                    weight = float(weight_str)
                reps_str = input("Введите количество повторений: ").strip()
                if reps_str:
                    repetitions = int(reps_str)
                units = 'kg'
            elif exercise_type == '2':
                time_str = input("Введите время в секундах: ").strip()
                if time_str:
                    time = int(time_str)
                speed_str = input("Введите скорость: ").strip()
                if speed_str:
                    speed = float(speed_str)
                units = 'kph'
            else:
                print("Неверный тип упражнения.")
                return
            feeling_str = input("Введите оценку самочувствия (1-5): ").strip()
            feeling = None
            if feeling_str:
                feeling = int(feeling_str)
            self.db.add_workout(
                workout_date=workout_date,
                exercise_name=exercise_name,
                order_number=order_number,
                sets=sets,
                weight=weight,
                repetitions=repetitions,
                time=time,
                speed=speed,
                units=units,
                feeling=feeling
            )
            print("Тренировка успешно добавлена.")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def find_workout_interactive(self) -> None:
        try:
            date_str = input("Введите дату тренировки (YYYY-MM-DD): ").strip()
            if not date_str:
                print("Отменено.")
                return
            workout_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            exercise_name = input("Введите название упражнения: ").strip()
            if not exercise_name:
                print("Отменено.")
                return
            result = self.db.find_workout(workout_date, exercise_name)
            if result:
                print(f"\nНайдены тренировки для '{exercise_name}' на {workout_date}:")
                for record in result:
                    print(record)
            else:
                print(f"Тренировки для '{exercise_name}' на {workout_date} не найдены.")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def show_all_data(self) -> None:
        # Метод print_all_data сам печатает содержимое.
        self.db.print_all_data()

    def plot_progress_interactive(self) -> None:
        try:
            exercise_name = input("Введите название упражнения для построения графика: ").strip()
            if not exercise_name:
                print("Отменено.")
                return
            self.db.plot_weights(exercise_name)
        except ValueError as e:
            print(f"Ошибка: {e}")


