from database.database import Database
from menu import Interface


def main() -> None:
    db = Database('src/database/gym_tracker.db')
    ui = Interface(db)
    ui.run_main_menu()
    db.close()


if __name__ == '__main__':
    main()
