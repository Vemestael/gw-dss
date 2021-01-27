from datetime import date

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QTableWidgetItem
from dateutil import relativedelta

from src.database.db_api import DbApi
from src.dataprocessing.input_data import InputData
from src.predict.predict import Predict


class ButtonHandler:
    @staticmethod
    def all_time_pressed(ui):
        ui.date_start.setDate(QDate(DbApi.get_first_date()))

    @staticmethod
    def last_year_pressed(ui):
        now = date.today()
        ui.date_start.setDate(QDate(now + relativedelta.relativedelta(years=-1)))

    @staticmethod
    def last_6_month_pressed(ui):
        now = date.today()
        ui.date_start.setDate(QDate(now + relativedelta.relativedelta(months=-6)))

    @staticmethod
    def last_3_month_pressed(ui):
        now = date.today()
        ui.date_start.setDate(QDate(now + relativedelta.relativedelta(months=-3)))

    @staticmethod
    def last_month_pressed(ui):
        now = date.today()
        ui.date_start.setDate(QDate(now + relativedelta.relativedelta(months=-1)))

    @staticmethod
    def analyze_pressed(ui):
        tables = [
            ui.predict_table_1,
            ui.predict_table_2,
            ui.predict_table_3,
            ui.predict_table_4,
            ui.predict_table_5,
            ui.predict_table_6,
            ui.predict_table_7
        ]
        date_start = ui.date_start.date().toPyDate()
        date_end = ui.date_end.date().toPyDate()
        lambda_by_shift = InputData.get_count_of_calls_by_range(date_start, date_end)
        for i in range(len(lambda_by_shift)):
            table = tables[i]
            for j in range(len(lambda_by_shift[i])):
                index = 1
                predicts = Predict(range(1, 50), 20, lambda_by_shift[i][j], 1.5).get_predict()
                for predict in predicts:
                    for characteristic in predict:
                        table.setItem(index, j + 2, QTableWidgetItem(characteristic))
                        index += 1
