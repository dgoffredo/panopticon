import datetime
from pathlib import Path
import sqlite3


_database_connection = None


def database():
    """Return the shared connection to the sqlite database."""
    global _database_connection

    if _database_connection is not None:
        return _database_connection

    db_path = Path('database.sqlite3')
    init_script_path = Path(__file__).parent.absolute() / 'tables.sql'

    db = sqlite3.connect(db_path)
    script_sql = init_script_path.read_text()
    db.executescript(script_sql)

    _database_connection = db
    return db


def select_popup_settings():
    db = database()
    query = """
    select
        widthPixels,
        heightPixels,
        leftPixels,
        rightPixels,
        launchAutomatically
    from PopupSettings
    order by insertISO8601 desc
    limit 1;
    """
    rows = list(db.execute(query))
    if len(rows) == 0:
        # default values
        return {
            'width': 240,
            'height': 200,
            'left': 0,
            'right': 0,
            'openAutomatically': False
        }
    
    assert len(rows) == 1
    row = rows[0]
    return {
        'width': row[0],
        'height': row[1],
        'left': row[2],
        'right': row[3],
        'openAutomatically': row[4] == 1
    }
    

def update_popup_settings():
    """TODO"""


def select_events(begin_datetime, end_datetime):
    """TODO"""


def insert_event(type_name, activity_name):
    """TODO"""
