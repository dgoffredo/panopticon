from datetime import datetime, date
from pathlib import Path
import sqlite3


class _Queries:
    def __init__(self):
        """Each "foo.sql" in "sql/" sets the attribute "foo" on this object to
        a string that is the contents of "sql/foo.sql".

        So, the SQL queries that this module makes will be the `.foo` or
        `.bar` of some `_Queries` instance.
        """
        for path in (Path(__file__).parent.absolute() / 'sql').iterdir():
            setattr(self, path.stem, path.read_text())


_queries = _Queries()


_database_connection = None


def database():
    """Return the shared connection to the sqlite database."""
    global _database_connection

    if _database_connection is not None:
        return _database_connection

    db = sqlite3.connect('database.sqlite3')
    db.executescript(_queries.tables)
    db.execute("pragma foreign_keys = on")

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

    # Assumed-local (i.e. "naive" no-timezone) datetime
    inserted = datetime.now()

    db.execute(statement, (inserted, width, height, left, top, openAutomatically))
    db.commit()


def select_maximal_time_range():
    (least, most), = database().execute(_queries.range)

    if least is not None:
        least = datetime.fromisoformat(least)
    if most is not None:
        most = datetime.fromisoformat(most)

    return least, most


def select_durations(begin_datetime, end_datetime):
    db = database()
    cursor = db.execute(_queries.durations, (begin_datetime, end_datetime))
    result = []
    for begin, end, activity, milliseconds in cursor:
        result.append((
            datetime.fromisoformat(begin),
            datetime.fromisoformat(end),
            activity,
            milliseconds))

    return result


def insert_event(type_name, activity_name):
    db = database()
    statement = """
    insert into Event(inserted, type, activityAfter)
    values(?, ?, ?)
    """

    # Assumed-local (i.e. "naive" no-timezone) datetime
    inserted = datetime.now()

    db.execute(statement, (inserted, type_name, activity_name))
    db.commit()
