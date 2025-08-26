import sqlite3
from abc import ABC, abstractmethod


class Table(ABC):
    """
    Table class is the interface for working with tables.
    """

    def __init__(self, table_name: str, cursor: sqlite3.Cursor) -> None:
        """
        Connects to the database.
        :param table_name: name of the table.
        :param cursor: cursor to the database.
        """
        self._cursor = cursor
        self.table_name = table_name

    @abstractmethod
    def create(self) -> None:
        """
        Creates the table.
        """
        pass

    def drop(self) -> None:
        """
        Delets the table
        """
        self._cursor.execute(f'DROP TABLE IF EXISTS {self.table_name};')

    def clear(self) -> None:
        """
        Clears the table.
        """
        self._cursor.execute(f'DELETE FROM {self.table_name};')

    def delete_by_id(self, id):
        """
        Deletes a record with the given ID.
        :param id: ID of the record to delete.
        """
        self._cursor.execute(f"""
            DELETE FROM {self.table_name}
            WHERE id = ?;
        """, (id,))

    def get_all_data(self) -> list[tuple]:
        """
        Gets all data from the table.
        :return: list of all data.
        """
        self._cursor.execute(f'SELECT * FROM {self.table_name};')
        return self._cursor.fetchall()

    def print_all_data(self) -> None:
        """
        Prints all data of the table.
        """
        print(self.get_all_data(), end='\n\n')
