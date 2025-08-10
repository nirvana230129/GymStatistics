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

    def clear(self) -> None:
        """
        Clears the table.
        """
        self._cursor.execute(f'DELETE FROM {self._table_name};')

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

    def get_all_data(self) -> list[tuple]:
        """
        Gets all data from the table.
        :return: list of all data.
        """
        self._cursor.execute(f'SELECT * FROM {self._table_name};')
        return self._cursor.fetchall()

    def print_all_data(self) -> None:
        """
        Prints all data of the table.
        """
        print(self.get_all_data(), end='\n\n')
