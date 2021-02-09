from datetime import date
from functools import partial

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDate, QSize, QSettings
from PyQt5.QtWidgets import QTableWidgetItem, QStyledItemDelegate, QStyleOptionViewItem, qApp
from dateutil import relativedelta

from database.db_api import DbApi
from interface.button_handler import ButtonHandler
from interface.gui import Ui_MainWindow


class VerticalTextDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        super(VerticalTextDelegate, self).__init__()

    def paint(self, painter, option, index):
        option_copy = QStyleOptionViewItem(option)
        rect_center = QtCore.QPointF(QtCore.QRectF(option.rect).center())
        painter.save()
        painter.translate(rect_center.x(), rect_center.y())
        painter.rotate(-90.0)
        painter.translate(-rect_center.x(), -rect_center.y())
        option_copy.rect = painter.worldTransform().mapRect(option.rect)

        # Call the base class implementation
        super(VerticalTextDelegate, self).paint(painter, option_copy, index)

        painter.restore()

    def sizeHint(self, option, index):
        val = QSize(self.sizeHint(option, index))
        return QSize(val.height(), val.width())


class Interface(QtWidgets.QMainWindow):
    def __init__(self):
        super(Interface, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()
        self.button_handling()

        settings = QSettings()
        db_path = settings.value('db_path', '')
        if db_path:
            DbApi.connect(db_path)
        else:
            ButtonHandler.set_db_path_triggered(self)

    def init_ui(self):
        self.set_date()
        self.set_predict_table_headers()

    def set_date(self):
        self.ui.date_start.setDate(QDate(QDate(date.today() - relativedelta.relativedelta(weeks=1))))
        self.ui.date_end.setDate(QDate(date.today()))

    def set_predict_table_headers(self):
        tables = [
            self.ui.predict_table_1,
            self.ui.predict_table_2,
            self.ui.predict_table_3,
            self.ui.predict_table_4,
            self.ui.predict_table_5,
            self.ui.predict_table_6,
            self.ui.predict_table_7,
            self.ui.cost_table_1,
            self.ui.cost_table_2,
            self.ui.cost_table_3,
            self.ui.cost_table_4,
            self.ui.cost_table_5,
            self.ui.cost_table_6,
            self.ui.cost_table_7
        ]
        for table in tables:
            table.setSpan(0, 0, 1, 2)
            table.setSpan(1, 0, 3, 1)
            table.setSpan(4, 0, 3, 1)
            table.setSpan(7, 0, 3, 1)

            # horizontal headers
            table.setItem(0, 2, QTableWidgetItem('Смена 1'))
            table.setItem(0, 3, QTableWidgetItem('Смена 2'))
            table.setItem(0, 4, QTableWidgetItem('Смена 3'))

            if 'predict_table' in table.objectName():
                for i in range(0, 10, 3):
                    table.setItem(i + 1, 1, QTableWidgetItem('Количество персонала'))
                    table.setItem(i + 2, 1, QTableWidgetItem('Обработанных заявок'))
                    table.setItem(i + 3, 1, QTableWidgetItem('Длина очереди'))
            else:
                for i in range(0, 10, 3):
                    table.setItem(i + 1, 1, QTableWidgetItem('Стоимость персонала'))
                    table.setItem(i + 2, 1, QTableWidgetItem('Стоимость заявки'))
            table.setItem(1, 0, QTableWidgetItem('Максимум заявок'))
            table.setItem(4, 0, QTableWidgetItem('Оптимально'))
            table.setItem(7, 0, QTableWidgetItem('Мин. очередь'))

            table.setItemDelegateForColumn(0, VerticalTextDelegate(self))
            table.setColumnWidth(0, 10)
            table.setColumnWidth(1, 160)

    def button_handling(self):
        self.ui.analyze.clicked.connect(partial(ButtonHandler.analyze_pressed, self))
        self.ui.all_time.clicked.connect(partial(ButtonHandler.all_time_pressed, self.ui))
        self.ui.last_year.clicked.connect(partial(ButtonHandler.last_year_pressed, self.ui))
        self.ui.last_6_month.clicked.connect(partial(ButtonHandler.last_6_month_pressed, self.ui))
        self.ui.last_3_month.clicked.connect(partial(ButtonHandler.last_3_month_pressed, self.ui))
        self.ui.last_month.clicked.connect(partial(ButtonHandler.last_month_pressed, self.ui))

        self.ui.action_1.triggered.connect(partial(ButtonHandler.set_db_path_triggered, self))
        self.ui.action_2.triggered.connect(partial(ButtonHandler.set_hourly_payment_triggered, self))
        self.ui.action_exit.triggered.connect(qApp.quit)
