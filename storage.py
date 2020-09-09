from datetime import datetime, timezone
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


# These property names are the input interface of `update_popup_settings` and
# the output interface of `select_popup_settings`.
DEFAULT_POPUP_SETTINGS = {
    'width': 240,
    'height': 200,
    'left': 0,
    'top': 0,
    'openAutomatically': False
}


def select_popup_settings():
    db = database()
    query = """
    select
        widthPixels,
        heightPixels,
        leftPixels,
        topPixels,
        launchAutomatically
    from PopupSettings
    order by inserted desc
    limit 1;
    """
    rows = list(db.execute(query))
    if len(rows) == 0:
        # default values
        return DEFAULT_POPUP_SETTINGS
    
    assert len(rows) == 1
    row = rows[0]
    return {
        'width': row[0],
        'height': row[1],
        'left': row[2],
        'top': row[3],
        'openAutomatically': row[4] == 1
    }
    

def update_popup_settings(args):
    def get(param):
        maybe_list = args.get(param)
        if maybe_list is not None:
            value, = maybe_list
            return value
        return DEFAULT_POPUP_SETTINGS[param]

    width = int(get('width'))
    height = int(get('height'))
    left = int(get('left'))
    top = int(get('top'))
    openAutomatically = 'openAutomatically' in args

    db = database()
    statement = """
    insert into PopupSettings(
        inserted,
        widthPixels,
        heightPixels,
        leftPixels,
        topPixels,
        launchAutomatically)
    values(?, ?, ?, ?, ?, ?)
    """

    # Keep the "naive" part of the UTC datetime, but ditch the zone.
    inserted = datetime.now(timezone.utc).replace(tzinfo=None)

    db.execute(statement, (inserted, width, height, left, top, openAutomatically))
    db.commit()


def select_events(begin_datetime, end_datetime):
    """TODO"""


def insert_event(type_name, activity_name):
    """TODO"""
