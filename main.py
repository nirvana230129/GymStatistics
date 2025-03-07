import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import tkinter as tk
from tkinter import messagebox


class Database:
    def __init__(self, db_file, table_name):
        self._connection = sqlite3.connect(db_file)
        self._cursor = self._connection.cursor()
        self.table_name = table_name

    def drop_table(self):
        self._cursor.execute(f'DROP TABLE IF EXISTS {self.table_name};')

    def create_table(self):
        self._cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                date DATE NOT NULL,
                machine VARCHAR NOT NULL,
                weight REAL,
                rating INTEGER,
                description TEXT,
                PRIMARY KEY (date, machine)
            );
        ''')

    def add_workout(self, date: datetime.date, machine: str, weight: float = None, rating: int = None,
                    description: str = None):
        try:
            self._cursor.execute(f'''
                INSERT INTO {self.table_name} (date, machine, weight, rating, description)
                VALUES (?, ?, ?, ?, ?);
            ''', (date, machine, weight, rating, description))
        except sqlite3.IntegrityError:
            raise Exception(f'Workout with {machine} on {date} already exists')

    def commit(self):
        self._connection.commit()

    def plot_weights(self, machine):
        self._cursor.execute(f'''
            SELECT date, weight 
            FROM {self.table_name} 
            WHERE machine = ?
        ''', (machine,))
        data = self._cursor.fetchall()
        print(data)
        dates = [row[0] for row in data]
        weights = [row[1] for row in data]

        plt.figure(figsize=(10, 5))
        plt.plot(dates, weights, marker='o')
        plt.title(f'Weight Progression for {machine}')
        plt.xlabel('Date')
        plt.ylabel('Weight')
        plt.grid(True)
        plt.show()


db = Database('gym_tracker.db', 'workouts')
db.drop_table()
db.create_table()
db.commit()
db.add_workout(str(datetime.today().date()), 'бицепс', 35)
db.add_workout(datetime(2025, 3, 1).date(), 'Bench Press', 60, 5)
db.add_workout(datetime(2025, 3, 2).date(), 'Bench Press', 62.5, 4)
db.add_workout(datetime(2025, 3, 3).date(), 'Bench Press', 65, 4)
db.add_workout(datetime(2025, 3, 4).date(), 'Bench Press', 70, 2)
db.commit()


# Функция для добавления данных о тренировке
def add_workout_entry():
    date = date_entry.get()
    machine = machine_entry.get()
    weight = weight_entry.get()
    rating = rating_entry.get()
    description = description_entry.get()

    try:
        db.add_workout(datetime.strptime(date, '%Y-%m-%d').date(), machine, float(weight), int(rating), description)
        db.commit()
        messagebox.showinfo("Success", "Workout added successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Функция для отображения графика
def plot_weights_graph():
    machine = machine_entry.get()
    db.plot_weights(machine)

# Создание главного окна
root = tk.Tk()
root.title("Gym Tracker")

# Поля для ввода данных
tk.Label(root, text="Date (YYYY-MM-DD)").grid(row=0, column=0)
date_entry = tk.Entry(root)
date_entry.grid(row=0, column=1)

tk.Label(root, text="Machine").grid(row=1, column=0)
machine_entry = tk.Entry(root)
machine_entry.grid(row=1, column=1)

tk.Label(root, text="Weight").grid(row=2, column=0)
weight_entry = tk.Entry(root)
weight_entry.grid(row=2, column=1)

tk.Label(root, text="Rating (1-5)").grid(row=3, column=0)
rating_entry = tk.Entry(root)
rating_entry.grid(row=3, column=1)

tk.Label(root, text="Description").grid(row=4, column=0)
description_entry = tk.Entry(root)
description_entry.grid(row=4, column=1)

# Кнопка для добавления данных
add_button = tk.Button(root, text="Add Workout", command=add_workout_entry)
add_button.grid(row=5, column=0, columnspan=2)

# Кнопка для отображения графика
plot_button = tk.Button(root, text="Plot Weights", command=plot_weights_graph)
plot_button.grid(row=6, column=0, columnspan=2)

# Запуск главного цикла
root.mainloop()
