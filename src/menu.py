from datetime import date, datetime
from database.database import Database
from tabulate import tabulate
from input import parse_input


class Interface:
    """
    User-facing interface for interacting with the database via menus.
    """

    def __init__(self, db: Database, clear: bool = False, fill: bool = False) -> None:
        """
        Initialize interface with a database instance.

        :param db: database adapter
        :param clear: if True, recreate and clear tables
        :param fill: if True, seed demo data (exercises and workouts)
        """
        self.db = db
        if clear:
            self.db.create()
            self.db.clear()
        if fill:
            self.fill_exercises()
            self.fill_workouts()

    def fill_exercises(self) -> None:
        """
        Seed a small set of demo exercises.
        """
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

    def add_exercise(self) -> None:
        """
        Interactive flow to add a new exercise.
        """
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

    def add_workout_day(self) -> None:
        """
        Add a full workout day - date is asked once, then multiple exercises.
        """
        print("\n=== ВВОД ТРЕНИРОВОЧНОГО ДНЯ ===")
        workout_date = parse_input('date', 'Enter workout date')
        if workout_date is None:
            print("Отменено.")
            return
            
        print(f"\nВводим тренировки на {workout_date}")
        print("Доступные упражнения:", ", ".join([f'{i[1]} ({i[2]})' for i in self.db.get_all_exercises()]))
        
        order_number = 0
        while True:
            print("\n" + "-" * 40)
            exercise_name = input("Введите название упражнения (или 'exit' для завершения): ").strip()
            if exercise_name.lower() == 'exit':
                break                
            if not exercise_name:
                print("Название упражнения не может быть пустым.")
                continue
            if not self.db.get_exercise_id(exercise_name):
                add_new = input(f"Упражнение '{exercise_name}' не найдено. Добавить? (y/n): ").strip().lower()
                if add_new == 'y':
                    self.db.add_exercise(exercise_name)
                else:
                    continue
            
            print(f"\nВвод данных для упражнения: {exercise_name}")
            
            sets = parse_input('int', 'Enter sets number')
            if sets is None:
                print("Отменено.")
                continue
                
            exercise_type = input("Тип упражнения (1 - силовое, 2 - кардио): ").strip()
            weight = None
            repetitions = None
            time = None
            speed = None
            units = None
            
            if exercise_type == '1':
                weight = parse_input('float', 'Enter weight')
                if weight is None:
                    print("Отменено.")
                    continue
                repetitions =parse_input('int', 'Enter number of repetitions')
                if repetitions is None:
                    print("Отменено.")
                    continue
                units = 'kg'
            elif exercise_type == '2':
                time = parse_input('int', 'Enter time in seconds')
                if time is None:
                    print("Отменено.")
                    continue
                speed = parse_input('float', 'Enter speed')
                if speed is None:
                    print("Отменено.")
                    continue
                units = 'kph'
            else:
                print("Неверный тип упражнения.")
                continue
                
            feeling = parse_input('int', 'Enter feeling rating')
            if feeling is None:
                print("Отменено.")
                continue
                
            # Добавляем тренировку
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
            print(f"Тренировка '{exercise_name}' успешно добавлена.")
            
            order_number += 1
            
        self.db.commit()
        print("Тренировочный день завершен.")

    def add_single_exercise(self) -> None:
        """
        Add a single exercise for a specific date.
        """
        print("\n=== ВВОД ОДНОГО УПРАЖНЕНИЯ ===")
        workout_date = parse_input('date', 'Enter workout date')
        if workout_date is None:
            print("Отменено.")
            return
            
        exercise_name = input("Введите название упражнения: ").strip()
        if not exercise_name:
            print("Отменено.")
            return
            
        # Проверяем, существует ли упражнение
        if not self.db.get_exercise_id(exercise_name):
            add_new = input(f"Упражнение '{exercise_name}' не найдено. Добавить? (y/n): ").strip().lower()
            if add_new == 'y':
                self.db.add_exercise(exercise_name)
            else:
                return
                
        print(f"\nВвод данных для упражнения: {exercise_name} на {workout_date}")
        
        order_number = parse_input('int', 'Enter order number')
        if order_number is None:
            print("Отменено.")
            return
            
        sets = parse_input('int', 'Enter sets number')
        if sets is None:
            print("Отменено.")
            return
            
        exercise_type = input("Тип упражнения (1 - силовое, 2 - кардио): ").strip()
        weight = None
        repetitions = None
        time = None
        speed = None
        units = None
        
        if exercise_type == '1':
            weight = parse_input('float', 'Enter weight')
            if weight is None:
                print("Отменено.")
                return
            repetitions = parse_input('int', 'Enter number of repetitions')
            if repetitions is None:
                print("Отменено.")
                return
            units = 'kg'
        elif exercise_type == '2':
            time = parse_input('int', 'Enter time in seconds')
            if time is None:
                print("Отменено.")
                return
            speed = parse_input('float', 'Enter speed')
            if speed is None:
                print("Отменено.")
                return
            units = 'kph'
        else:
            print("Неверный тип упражнения.")
            return
            
        feeling = parse_input('int', 'Enter feeling rating')
        if feeling is None:
            print("Отменено.")
            return
            
        # Добавляем тренировку
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
        self.db.commit()
        print(f"Тренировка '{exercise_name}' успешно добавлена.")

    def delete_exercise_interactive(self) -> None:
        """
        Interactive deletion of an exercise with all related data.
        """
        self.show_table_data(self.db.get_all_exercises())
        if not self.db.get_all_exercises():
            return
        try:
            exercise_name = input("\nВведите название упражнения для удаления: ").strip()
            if not exercise_name:
                print("Отменено.")
                return
            confirm = input(f"Вы уверены, что хотите удалить упражнение '{exercise_name}' и все связанные данные? (y/n): ").strip().lower()
            if confirm == 'y':
                self.db.delete_exercise(exercise_name)
                print(f"Упражнение '{exercise_name}' успешно удалено.")
            else:
                print("Удаление отменено.")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def delete_workout_by_date_interactive(self) -> None:
        """
        Interactive deletion of all workouts for a given date.
        """
        self.show_dates()
        if not self.db.get_all_dates():
            return
        try:
            workout_date = parse_input('date', 'Enter workout date')
            if workout_date is None:
                print("Отменено.")
                return
                
            self.show_workouts_by_date(workout_date)
            confirm = input(f"Вы уверены, что хотите удалить все тренировки на {workout_date}? (y/n): ").strip().lower()
            if confirm == 'y':
                self.db.delete_workout_by_date(workout_date)
                print(f"Все тренировки на {workout_date} успешно удалены.")
            else:
                print("Удаление отменено.")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def delete_specific_workout_interactive(self) -> None:
        """
        Interactive deletion of workouts for a given date and exercise.
        """
        self.show_dates()
        if not self.db.get_all_dates():
            return
        try:
            workout_date = parse_input('date', 'Enter workout date')
            if workout_date is None:
                print("Отменено.")
                return
                
            self.show_workouts_by_date(workout_date)
            exercise_name = input("Введите название упражнения для удаления: ").strip()
            if not exercise_name:
                print("Отменено.")
                return
                
            confirm = input(f"Вы уверены, что хотите удалить тренировку '{exercise_name}' на {workout_date}? (y/n): ").strip().lower()
            if confirm == 'y':
                self.db.delete_workout(workout_date, exercise_name)
                print(f"Тренировка '{exercise_name}' на {workout_date} успешно удалена.")
            else:
                print("Удаление отменено.")
        except ValueError as e:
            print(f"Ошибка: {e}")

    def run_delete_menu(self) -> None:
        """
        Run the nested delete menu loop.
        """
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
                # self.show_exercises()
                self.show_table_data(self.db.get_all_exercises())
            elif choice == '2':
                self.show_dates()
            elif choice == '3':
                try:
                    workout_date = parse_input('date', 'Enter workout date')
                    if workout_date:
                        self.show_workouts_by_date(workout_date)
                except ValueError:
                    print("Ошибка при вводе даты.")
            elif choice == '4':
                self.delete_exercise_interactive()
            elif choice == '5':
                self.delete_workout_by_date_interactive()
            elif choice == '6':
                self.delete_specific_workout_interactive()
            else:
                print("Неверный выбор. Попробуйте снова.")

    def run_main_menu(self) -> None:
        """
        Run the main menu loop.
        """
        while True:
            print("\n\n" + "="*50)
            print("ГЛАВНОЕ МЕНЮ")
            print("="*50)
            print("1. Добавить упражнение")
            print("2. Добавить выполнение одного упражнения")
            print("3. Добавить тренировочный день")
            print("4. Найти тренировку")
            print("5. Показать все упражнения")
            print("6. Показать все расписание")
            print("7. Показать все тренировки")
            print("8. Построить график прогресса")
            print("9. Управление удалением данных")
            print("0. Выход")

            choice = input("\nВыберите действие (0-9): ").strip()

            if choice == '0':
                print("До свидания!")
                break
            elif choice == '1':
                self.add_exercise()
            elif choice == '2':
                self.add_single_exercise()
            elif choice == '3':
                self.add_workout_day()
            elif choice == '4':
                self.find_workout()
            elif choice == '5':
                self.show_table_data(self.db.get_all_exercises())
            elif choice == '6':
                self.show_table_data(self.db.get_all_schedule())
            elif choice == '7':
                self.show_table_data(self.db.get_all_workouts())
            elif choice == '8':
                self.plot_progress()
            elif choice == '9':
                self.run_delete_menu()
            else:
                print("Неверный выбор. Попробуйте снова.")

    def find_workout(self) -> None:
        """
        Interactive search for workouts by date and exercise.
        """
        try:
            workout_date = parse_input('date', 'Enter workout date')
            if workout_date is None:
                print("Отменено.")
                return
                
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

    def show_dates(self) -> None:
        """
        Print all distinct dates that have workouts.
        """
        dates = self.db.get_all_dates()
        if not dates:
            print("В базе данных нет тренировок.")
            return

        print("\nСписок дат с тренировками:")
        print("-" * 30)
        for i, workout_date in enumerate(dates, 1):
            print(f"{i}. {workout_date}")
    
    def show_workouts_by_date(self, workout_date: date) -> None:
        """
        Print workouts scheduled/executed for a given date.

        :param workout_date: date to query
        """
        workouts = self.db.get_workouts_by_date(workout_date)
        if not workouts:
            print(f"На {workout_date} нет тренировок.")
            return
        self.show_table_data(workouts)

    def show_table_data(self, data) -> None:
        """
        Print the table.
        """
        print(tabulate(data, headers=self.db.get_columns(), tablefmt="grid"))

    def plot_progress(self) -> None:
        """
        Interactive plotting for average weight over time for an exercise.
        """
        try:
            exercise_name = input("Введите название упражнения для построения графика: ").strip()
            if not exercise_name:
                print("Отменено.")
                return
            self.db.plot_weights(exercise_name)
        except ValueError as e:
            print(f"Ошибка: {e}")


