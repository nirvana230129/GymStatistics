import sqlite3
from abc import ABC, abstractmethod


class Table(ABC):
    """
    Base abstract wrapper over an SQLite table.
    Defines common interface and typical operations.
    """

    def __init__(self, table_name: str, cursor: sqlite3.Cursor) -> None:
        """
        Initialize the table wrapper.

        :param table_name: table name
        :param cursor: SQLite cursor
        """
        self._cursor = cursor
        self.table_name = table_name

    @abstractmethod
    def create(self) -> None:
        """
        Create the table if it does not exist.
        """
        pass

    def drop(self) -> None:
        """
        Drop the table if it exists.
        """
        self._cursor.execute(f'DROP TABLE IF EXISTS {self.table_name};')

    def clear(self) -> None:
        """
        Delete all rows from the table.
        """
        self._cursor.execute(f'DELETE FROM {self.table_name};')

    def delete_by_id(self, id):
        """
        Delete a row by its primary key.

        :param id: row identifier
        """
        self._cursor.execute(f"""
            DELETE FROM {self.table_name}
            WHERE id = ?;
        """, (id,))

    def get_all_data(self) -> list[tuple]:
        """
        Get all rows from the table.

        :return: list of tuples
        """
        self._cursor.execute(f'SELECT * FROM {self.table_name};')
        return self._cursor.fetchall()

    def print_all_data(self) -> None:
        """
        Print all rows of the table.
        """
        print(self.get_all_data(), end='\n\n')
