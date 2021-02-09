from database.models import CallTable, get_cursor


class DbApi:
    @staticmethod
    def add_new_call(_date, _phone_number, _talk_time, _call_status):
        CallTable.create(
            date=_date,
            phone_number=_phone_number,
            talk_time=_talk_time,
            call_status=_call_status
        )

    @staticmethod
    def get_calls_info_by_date(_date_start, _date_end):
        """_date_* - datetime object"""
        cursor = get_cursor()
        date_start = _date_start.strftime('%Y-%m-%d')
        date_end = _date_end.strftime('%Y-%m-%d')
        # strftime - первый день недели - воскресенье
        query = f"""
                    select strftime('%w', date) WeekNumber,
                    strftime('%H', date) HourNumber,
                    count(id)/(
                        SELECT DISTINCT
                        cast((strftime('%d', '{date_end}') - strftime('%d', '{date_start}') + 1.0)/7.0 as int) * 1.
                        from Call_table
                    )
                    from Call_table
                    where (date BETWEEN '{date_start}' AND '{date_end}')
                    group by WeekNumber, HourNumber
                    """

        cursor.execute(query)
        return cursor.fetchall()

    @staticmethod
    def get_first_date():
        return CallTable.select().limit(1).order_by(CallTable.id).get().date
