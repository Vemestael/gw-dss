import datetime
from random import randint
from database.db_api import DbApi


def record_generator():
    start_date = datetime.datetime(2020, 6, 1, 0, 0, 0)
    day_count = 14
    time_count = 24
    for single_date in (start_date + datetime.timedelta(days=n) for n in range(day_count)):
        for single_time in (single_date + datetime.timedelta(hours=n) for n in range(time_count)):
            for single_minutes in (single_time + datetime.timedelta(minutes=n) for n in range(randint(1, 10))):
                DbApi.add_new_call(single_minutes, "0000000000", 100, "done")
