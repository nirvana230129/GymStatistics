import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime


conn = sqlite3.connect('gym_tracker.db')
c = conn.cursor()
c.execute('''
          CREATE TABLE IF NOT EXISTS workouts (
              date DATE,
              machine TEXT,
              weight REAL,
              rating INTEGER,
              PRIMARY KEY (date, machine)
          )
          ''')
conn.commit()
