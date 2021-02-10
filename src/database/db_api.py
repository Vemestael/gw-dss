import sqlite3
from datetime import datetime


class DbApi:
    conn = None

    @staticmethod
    def connect(db_path):
        DbApi.conn = sqlite3.connect(db_path)

    @staticmethod
    def get_cursor():
        return DbApi.conn.cursor()

    @staticmethod
    def close():
        DbApi.conn.close()

    @staticmethod
    def add_new_call(_date, _phone_number, _talk_time, _call_status):
        query = f"""
                insert into Call_table(date, phone_number, talk_time, status)
                values ({_date}, {_phone_number}, {_talk_time}, {_call_status})
        """

        DbApi.get_cursor().execute(query)

    @staticmethod
    def get_calls_info_by_date(_date_start, _date_end):
        """_date_* - datetime object"""
        cursor = DbApi.get_cursor()
        date_start = _date_start.strftime('%Y-%m-%d')
        date_end = _date_end.strftime('%Y-%m-%d')

        last_date = DbApi.get_last_date()
        first_date = DbApi.get_first_date()
        if datetime.combine(_date_end, datetime.min.time()) < last_date:
            last_date = datetime.combine(_date_end, datetime.min.time())
        if datetime.combine(_date_start, datetime.min.time()) > first_date:
            first_date = datetime.combine(_date_start, datetime.min.time())
        day_count = last_date - first_date
        week_count = day_count.days // 7 if not day_count.days % 7 else day_count.days // 7 + 1

        # strftime - первый день недели - воскресенье
        query = f"""
                    select strftime('%w', date) WeekDayNumber,
                    strftime('%H', date) HourNumber,
                    count(id)/{week_count}
                    from Call_table
                    where (date BETWEEN '{date_start}' AND '{date_end}')
                    group by WeekDayNumber, HourNumber
                    """

        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def get_first_date():
        cursor = DbApi.get_cursor()
        query = f"""
            select date
            from Call_table
            order by id limit 1
        """

        cursor.execute(query)
        return datetime.strptime(cursor.fetchall()[0][0][:-10], '%Y-%m-%d %H:%M:%S')
        # [:-10] - срез точки и миллисекунд

    @staticmethod
    def get_last_date():
        cursor = DbApi.get_cursor()
        query = f"""
            select date
            from Call_table
            order by id desc limit 1
        """

        cursor.execute(query)
        return datetime.strptime(cursor.fetchall()[0][0][:-10], '%Y-%m-%d %H:%M:%S')
        # [:-10] - срез точки и миллисекунд
