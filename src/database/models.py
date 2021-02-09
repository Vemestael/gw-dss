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


connect.close()
