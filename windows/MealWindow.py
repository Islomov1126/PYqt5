from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5

from model import Meals


class MealWindow(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(PyQt5.QtCore.Qt.Window)

        self.setWindowTitle('Meals')
        self.row_count = 0

        self.initUI()

        self.sel_meal = None

    def initUI(self):
        self.setGeometry(100, 100, 400, 400)

        self.ql_meal_name = QLabel(self)
        self.ql_meal_name.setText("Meal Name: ")
        self.ql_meal_name.move(30, 30)

        self.qle_meal_name = QLineEdit(self)
        self.qle_meal_name.move(120, 30)

        self.btn_add = QPushButton('Add', self)
        self.btn_add.move(300, 30)
        self.btn_add.clicked.connect(self.onAdd)

        self.btn_update = QPushButton('Update', self)
        self.btn_update.move(300, 60)
        self.btn_update.clicked.connect(self.onUpdate)

        self.btn_del = QPushButton('Delete', self)
        self.btn_del.move(300, 90)
        self.btn_del.clicked.connect(self.onDel)

        self.table = QTableWidget(self)  # Создаём таблицу
        self.table.move(30, 60)
        self.table.setColumnCount(2)     # Устанавливаем три колонки

        # Устанавливаем заголовки таблицы
        self.table.setHorizontalHeaderLabels(['ID', "Meal name"])

        # Устанавливаем всплывающие подсказки на заголовки
        self.table.horizontalHeaderItem(0).setToolTip("This is Meal name")

        self.table.hideColumn(0)

        # Устанавливаем выравнивание на заголовки
        self.table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)

        # заполняем первую строку
        for meals in Meals.objects():
            self.table.setRowCount(self.row_count + 1)
            self.table.setItem(self.row_count, 0,
                               QTableWidgetItem(str(meals.id)))
            self.table.setItem(self.row_count, 1,
                               QTableWidgetItem(str(meals)))
            self.row_count += 1

        # делаем ресайз колонок по содержимому
        self.table.resizeColumnsToContents()
        self.table.clicked.connect(self.onClicked)

    def onAdd(self):
        reg = Meals(self.qle_meal_name.text())
        reg.save()
        self.table.setRowCount(self.row_count + 1)

        self.table.setItem(self.row_count, 0,
                           QTableWidgetItem(str(reg.id)))
        self.table.setItem(self.row_count, 1,
                           QTableWidgetItem(reg.name))
        self.row_count += 1

    def onUpdate(self):
        if self.sel_meal is not None:
            self.sel_meal.name = self.qle_meal_name.text()
            self.sel_meal.save()
            self.table.setItem(
                self.sel_row, 1, QTableWidgetItem(str(self.sel_meal)))

    def onDel(self):
        if self.sel_meal is not None:
            self.sel_meal.delete()
            self.sel_meal = None
            self.table.removeRow(self.sel_row)

    def onClicked(self, item):
        self.sel_row = self.table.currentRow()
        self.qle_meal_name.setText(self.table.item(self.sel_row, 1).text())

        self.sel_meal = Meals(self.table.item(
            self.sel_row, 1).text(), self.table.item(self.sel_row, 0).text())