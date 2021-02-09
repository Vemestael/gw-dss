from datetime import date

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QTableWidgetItem
from dateutil import relativedelta

from database.db_api import DbApi
from dataprocessing.input_data import InputData
from predict.predict import Predict


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
        predict_tables = [
            ui.predict_table_1,
            ui.predict_table_2,
            ui.predict_table_3,
            ui.predict_table_4,
            ui.predict_table_5,
            ui.predict_table_6,
            ui.predict_table_7
        ]
        cost_tables = [
            ui.cost_table_1,
            ui.cost_table_2,
            ui.cost_table_3,
            ui.cost_table_4,
            ui.cost_table_5,
            ui.cost_table_6,
            ui.cost_table_7
        ]
        date_start = ui.date_start.date().toPyDate()
        date_end = ui.date_end.date().toPyDate()
        lambda_by_shift = InputData.get_count_of_calls_by_range(date_start, date_end)
        for i in range(len(lambda_by_shift)):
            table = predict_tables[i]
            cost_table = cost_tables[i]
            for j in range(len(lambda_by_shift[i])):
                index = 1
                predicts = Predict(range(1, 10), 20, lambda_by_shift[i][j], 12).get_predict()
                for predict in predicts:
                    for characteristic in predict:
                        table.setItem(index, j + 2, QTableWidgetItem(characteristic))
                        index += 1

                    channel_cost = float(predict[0]) * 200
                    request_cost = (float(predict[0]) * 200) / float(predict[1])
                    request_cost = round(request_cost, 4)
                    cost_table.setItem(index-3, j+2, QTableWidgetItem(str(channel_cost)))
                    cost_table.setItem(index-2, j+2, QTableWidgetItem(str(request_cost)))
