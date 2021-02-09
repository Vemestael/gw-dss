import datetime

from database.models import CallTable, PredictTable, get_cursor

class DbApi:
    @staticmethod
    def add_new_predict(descriptor, channel_count, avg_count_of_served_requests, avg_queue_length):
        PredictTable.create(
            date=datetime.datetime.now(),
            descriptor=descriptor,
            channel_count=channel_count,
            avg_count_of_served_requests=avg_count_of_served_requests,
            avg_queue_length=avg_queue_length
        )

    @staticmethod
    def get_last_predicts() -> dict:
        query = PredictTable.select().limit(3).order_by(PredictTable.id.desc())
        return query.dicts().execute()

    @staticmethod
    def get_predicts(limit=50) -> dict:
        """limit - number of records(default = 50)"""
        query = PredictTable.select().limit(limit).order_by(PredictTable.id.desc())
        return query.dicts().execute()

    @staticmethod
    def update_predict(predict_id, _descriptor, _channel_count, _avg_count_of_served_requests, _avg_queue_length):
        predict = PredictTable(id=predict_id)
        predict.descriptor = _descriptor
        predict.channel_count = _channel_count
        predict.avg_count_of_served_requests = _avg_count_of_served_requests
        predict.avg_queue_length = _avg_queue_length
        predict.save()

    @staticmethod
    def delete_predicts(limit=1):
        """limit - number of records(default = 1)"""
        predict_id = DbApi.get_predicts(1)[0].get('id')
        query = PredictTable.delete().where(PredictTable.id > predict_id - limit)
        query.execute()

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
