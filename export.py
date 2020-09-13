import storage

import csv
from datetime import datetime, timedelta


def durations_csv(begin, end):
    """Return the relative path to a CSV file containing the activity duration
    intervals between the specified dates. The datetimes of the rows of the
    CSV will be >= begin and <= end.
    """
    # Get the minimum and maximum datetimes from the database. These will be the
    # "infinity" values used in the name of the file (if one or both of
    # `begin`/`end` is `None`). This is helpful, so that the names of the
    # files always indicate the truth about what they contain.
    least, most = storage.select_maximal_time_range()

    # If there are no rows, then `least == most == None`, and we can return a
    # special no-rows CSV.
    if least is None:
        assert most is None
        return 'csv/empty.csv'
    else:
        if begin is None:
            begin = least
        if end is None:
            end = most
        csv_basename = f'{begin.isoformat()} to {end.isoformat()}.csv'

    rows = storage.select_durations(begin, end)
    if len(rows) == 0:
        return 'csv/empty.csv'

    path = 'csv/' + csv_basename
    header = ['begin', 'end', 'activity', 'milliseconds']
    write_csv(path, header, rows)
    return path


def write_csv(path, header_row, data_rows):
    # newline='' per the csv module documentation
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header_row)
        writer.writerows(data_rows)
