
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5

from model import Meals, Drink


class DrinkWindow(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self.initUI()
        # self.fillTable()

    def onAdd(self):
        meal = Meals.get_by_id(self.cbb_meal.currentData())

        drink = Drink(self.le_dist.text(), meal.id)
        drink.save()

        row_count = self.table.rowCount()
        self.table.setRowCount(row_count + 1)
        self.table.setItem(row_count, 0,
                           QTableWidgetItem(str(meal.id)))
        self.table.setItem(row_count, 1,
                           QTableWidgetItem(str(meal.name)))
        self.table.setItem(row_count, 2,
                           QTableWidgetItem(str(drink.id)))
        self.table.setItem(row_count, 3,
                           QTableWidgetItem(str(drink.Name)))

    def onUpd(self):
        drink_name = self.le_drink.text()
        meal_id = self.cbb_meal.currentData()
        drink_id = int(self.table.item(self.sel_row, 2).text())

        drink = Drink(drink_name, meal_id, drink_id)
        drink.save()

        self.fillTable()

    def onDel(self):
        drink_name = self.le_drink.text()
        meal_id = self.cbb_meal.currentData()
        drink_id = int(self.table.item(self.sel_row, 2).text())

        drink = Drink(drink_name, meal_id, drink_id)
        drink.delete()

        self.fillTable()

    def onClicked(self):
        self.sel_row = self.table.currentRow()
        drink_name = self.table.item(self.sel_row, 3).text()
        self.le_drink.setText(drink_name)

    def initUI(self):

        self.setGeometry(200, 200, 680, 400)
        self.resize(680, 400)

        self.qlb_meal = QLabel("Meal", self)
        self.qlb_meal.move(30, 30)

        self.cbb_meal = QComboBox(self)
        self.cbb_meal.move(80, 30)

        self.qlb_drink = QLabel("Drinks", self)
        self.qlb_drink.move(280, 30)

        self.le_drink = QLineEdit(self)
        self.le_drink.move(380, 30)

        self.btn_add = QPushButton("Add", self)
        self.btn_add.move(530, 30)
        self.btn_add.clicked.connect(self.onAdd)

        self.btn_upd = QPushButton("Update", self)
        self.btn_upd.move(530, 60)
        self.btn_upd.clicked.connect(self.onUpd)

        self.btn_del = QPushButton("Delete", self)
        self.btn_del.move(530, 90)
        self.btn_del.clicked.connect(self.onDel)

        self.table = QTableWidget(self)
        self.table.setGeometry(30, 60, 480, 300)
        self.table.setColumnCount(4)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        self.table.clicked.connect(self.onClicked)

        self.cbb_meal.currentIndexChanged.connect(self.fillTable)
        for meals in Meals.objects():
            self.cbb_meal.addItem(meals.name, meals.id)

    def fillTable(self):
        self.table.clear()
        self.table.setHorizontalHeaderLabels(
            ["Meal id", 'Meal name', 'drink id', 'Drink name'])
        self.table.setRowCount(0)
        self.table.hideColumn(0)
        self.table.hideColumn(2)
        current_id = self.cbb_meal.currentData()
        for drink in Drink.objects():
            drink.MealID
            if current_id == drink.MealID:
                meal = drink.meal
                row_count = self.table.rowCount()
                self.table.setRowCount(row_count + 1)
                self.table.setItem(row_count, 0,
                                   QTableWidgetItem(str(meal.id)))
                self.table.setItem(row_count, 1,
                                   QTableWidgetItem(str(meal.Name)))
                self.table.setItem(row_count, 2,
                                   QTableWidgetItem(str(drink.id)))
                self.table.setItem(row_count, 3,
                                   QTableWidgetItem(str(drink.Name)))
        self.table.resizeColumnsToContents()
