from database.database import Database
from menu import Interface


def main() -> None:
    """
    Application entrypoint: initialize DB, run the interactive menu, close DB.
    """
    db = Database('src/database/gym_tracker.db')
    ui = Interface(db)
    ui.run_main_menu()
    db.close()


if __name__ == '__main__':
    main()
