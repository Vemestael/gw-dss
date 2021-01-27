from os.path import dirname

import peewee

dir_name = dirname(__file__)
connect = peewee.SqliteDatabase(dir_name + '/support_database.db')


def get_connect():
    return connect


def get_cursor():
    return connect.cursor()


class BaseModel(peewee.Model):
    class Meta:
        database = connect


class CallTable(BaseModel):
    date = peewee.DateTimeField(column_name="date")
    phone_number = peewee.TextField(column_name="phone_number")
    talk_time = peewee.FloatField(column_name="talk_time")
    call_status = peewee.TextField(column_name="call_status")

    class Meta:
        table_name = 'Call_table'


class PredictTable(BaseModel):
    date = peewee.DateTimeField(column_name="date")
    descriptor = peewee.TextField(column_name="descriptor")
    channel_count = peewee.IntegerField(column_name="channel_count")
    avg_count_of_served_requests = peewee.FloatField(
        column_name="avg_count_of_served_requests")
    avg_queue_length = peewee.FloatField(column_name="avg_queue_length")

    class Meta:
        table_name = 'Predict_table'


connect.close()
