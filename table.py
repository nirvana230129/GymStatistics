import sqlite3
from abc import ABC, abstractmethod


class Table(ABC):
    """
    Table class is the interface for working with tables.
    """

    def __init__(self, table_name: str, connection: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
        """
        Connects to the database.
        :param table_name: name of the table.
        :param connection: connection to the database.
        :param cursor: cursor to the database.
        """
        self._connection = connection
        self._cursor = cursor
        self._table_name = table_name

    def drop(self) -> None:
        """
        Deletes the table.
        """
        self._cursor.execute(f'DROP TABLE IF EXISTS {self._table_name};')

    @abstractmethod
    def create(self) -> None:
        """
        Creates the table.
        """
        pass

    def commit(self) -> None:
        """
        Commits the changes to the database.
        """
        self._connection.commit()
        """
        Gets all exercises.
        :return: list of all exercises.
        """
        self._cursor.execute('SELECT name FROM Exercises;')
        data = self._cursor.fetchall()
        return [i[0] for i in data]

    def print_all(self) -> None:
        """
        Prints all data of the table.
        """
        self._cursor.execute(f'SELECT * FROM {self._table_name};')
        data = self._cursor.fetchall()
        print(data, end='\n\n')
