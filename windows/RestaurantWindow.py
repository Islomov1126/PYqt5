from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import PyQt5

from model import Meal, Drinks, Restaurant


class RestaurantWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()

    def initUI(self):

        self.resize(800, 450)

        self.qlb_meal = QLabel("Meal", self)
        self.qlb_meal.move(40, 30)

        self.cbb_meal = QComboBox(self)
        self.cbb_meal.move(70, 30)

        self.cbb_meal.setGeometry(70,30,130,20)

        self.qlb_drinks = QLabel("Drinks", self)
        self.qlb_drinks.move(210, 30)

        self.cbb_drinks = QComboBox(self)
        self.cbb_drinks.move(230, 30)
        self.cbb_drinks.setGeometry(250, 30, 80, 20)

        self.qlb_est_year = QLabel("Est_year", self)
        self.qlb_est_year.move(40, 80)

        self.le_est_year = QLineEdit(self)
        self.le_est_year.move(150, 80)
        self.le_est_year.setGeometry(150, 80, 185, 20)

        self.qlb_num_of_meals = QLabel("Num_of_meals", self)
        self.qlb_num_of_meals.move(40, 120)

        self.le_num_of_meals = QLineEdit(self)
        self.le_num_of_meals.move(150, 120)
        self.le_num_of_meals.setGeometry(150, 120, 185, 20)

        self.qlb_prices = QLabel("Prices", self)
        self.qlb_prices.move(40, 160)

        self.le_prices = QLineEdit(self)
        self.le_prices.move(150, 160)
        self.le_prices.setGeometry(150, 160, 185, 20)

        self.qlb_ceo = QLabel("CEO", self)
        self.qlb_ceo.move(40, 200)

        self.le_ceo = QLineEdit(self)
        self.le_ceo.move(150, 200)
        self.le_ceo.setGeometry(150, 200, 185, 20)

        self.table = QTableWidget(self)
        self.table.setGeometry(370, 30, 702, 530)
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(
            ["Meal id", 'Meal name', 'Drinks id', 'Drinks name',
             "restaurant id", "Est_year", "Quantity_of_meals", "Meal prices", "Restaurant CEO"])
        self.table.setRowCount(0)
        self.table.hideColumn(0)
        self.table.hideColumn(2)
        self.table.hideColumn(4)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setColumnWidth(6, 200)


        self.btn_add = QPushButton("Add", self)
        self.btn_add.setGeometry(150, 270, 185, 40)
        self.btn_add.clicked.connect(self.onAdd)

        self.btn_upd = QPushButton("Update", self)
        self.btn_upd.setGeometry(150, 350, 185, 40)
        self.btn_upd.clicked.connect(self.onUpd)

        self.btn_del = QPushButton("Delete", self)
        self.btn_del.setGeometry(150, 430, 185, 40)
        self.btn_del.clicked.connect(self.onDel)

        for rest in Restaurant.objects():
            drinks = rest.Drinks
            meal = drinks.Meal
            row_count = self.table.rowCount()
            self.table.setRowCount(row_count + 1)
            self.table.setItem(row_count, 0,
                               QTableWidgetItem(str(meal.id)))
            self.table.setItem(row_count, 1,
                               QTableWidgetItem(str(meal.Name)))
            self.table.setItem(row_count, 2,
                               QTableWidgetItem(str(drinks.id)))
            self.table.setItem(row_count, 3,
                               QTableWidgetItem(str(drinks.Name)))
            self.table.setItem(row_count, 4,
                               QTableWidgetItem(str(rest.id)))
            self.table.setItem(row_count, 5,
                               QTableWidgetItem(str(rest.Year)))
            self.table.setItem(row_count, 6,
                               QTableWidgetItem(str(rest.Count_page)))
            self.table.setItem(row_count, 7,
                               QTableWidgetItem(str(rest.Price)))
            self.table.setItem(row_count, 8,
                               QTableWidgetItem(str(rest.Author)))

        self.table.clicked.connect(self.onClicked)

        self.cbb_meal.currentIndexChanged.connect(self.changedBT)
        for rest in Meal.objects():
            self.cbb_meal.addItem(rest.Name, rest.id)
        self.cbb_drinks.currentIndexChanged.connect(self.fillTable)

    def changedBT(self):
        res_id = self.cbb_meal.currentData()
        self.cbb_drinks.clear()
        for rest in Drinks.objects():
            if rest.Bookid == res_id:
                self.cbb_drinks.addItem(rest.Name, rest.id)

    def onClicked(self):
        self.sel_row = self.table.currentRow()
        self.le_est_year.setText(self.table.item(self.sel_row, 5).text())
        self.le_num_of_meals.setText(self.table.item(self.sel_row, 6).text())
        self.le_prices.setText(self.table.item(self.sel_row, 7).text())
        self.le_ceo.setText(self.table.item(self.sel_row, 8).text())

        self.sel_Restaurant = Restaurant(int(self.table.item(
            self.sel_row, 5).text()), int(self.table.item(self.sel_row, 6).text())
                             , int(self.table.item(self.sel_row, 7).text()), self.table.item(self.sel_row, 8).text(),
                             self.table.item(self.sel_row, 4).text(), self.table.item(self.sel_row, 0).text())

    def onAdd(self):
        meal = Meal.get_by_id(self.cbb_meal.currentData())
        drinks = Drinks.get_by_id(self.cbb_drinks.currentData())

        rest = Restaurant(int(self.le_book_year.text()), int(self.le_book_countpage.text()),
                    int(self.le_book_price.text()), self.le_book_author.text(), drinks.id)
        rest.save()

        row_count = self.table.rowCount()
        self.table.setRowCount(row_count + 1)
        self.table.setItem(row_count, 0,
                           QTableWidgetItem(str(meal.id)))
        self.table.setItem(row_count, 1,
                           QTableWidgetItem(str(meal.Name)))
        self.table.setItem(row_count, 2,
                           QTableWidgetItem(str(drinks.id)))
        self.table.setItem(row_count, 3,
                           QTableWidgetItem(str(drinks.Name)))
        self.table.setItem(row_count, 4,
                           QTableWidgetItem(str(rest.id)))
        self.table.setItem(row_count, 5,
                           QTableWidgetItem(str(rest.Est_year)))
        self.table.setItem(row_count, 6,
                           QTableWidgetItem(str(rest.Num_of_meals)))
        self.table.setItem(row_count, 7,
                           QTableWidgetItem(str(rest.Prices)))
        self.table.setItem(row_count, 8,
                           QTableWidgetItem(str(rest.CEO)))

    def onUpd(self):
        if self.sel_Restaurant is not None:
            est_year = int(self.le_est_year.text())
            num_of_meals = int(self.le_num_of_meals.text())
            prices = int(self.le_prices.text())
            ceo = self.le_ceo.text()
            rest_id = self.rest.currentData()
            drinks_id = int(self.table.item(self.sel_row, 4).text())

            ress = Restaurant(est_year, num_of_meals, prices,
                         ceo, rest_id, drinks_id)
            ress.save()

            self.fillTable()

    def onDel(self):
        if self.sel_Restaurant is not None:
            est_year = int(self.le_est_year.text())
            num_of_meals = int(self.le_num_of_meals.text())
            prices = int(self.le_prices.text())
            ceo = self.le_ceo.text()
            rest_id = self.rest.currentData()
            drinks_id = int(self.table.item(self.sel_row, 4).text())

            ress = Restaurant(est_year, num_of_meals, prices,
                         ceo, rest_id, drinks_id)
            ress.delete()

            self.fillTable()

    def fillTable(self):
        self.table.clear()
        self.table.setHorizontalHeaderLabels(
            ["Meal id", "Meal name", "Drinks id", "Drinks name",
             "Restaurant id", "Est year", "Num of meals", "Prices"
                , "Ceo"])
        self.table.setRowCount(0)
        self.table.hideColumn(0)
        self.table.hideColumn(2)
        self.table.hideColumn(4)
        current_id = self.cbb_drinks.currentData()
        for rest in Restaurant.objects():
            if current_id == rest.Restaurantid:
                drinks = rest.Drinks
                meal = drinks.Meal
                rowCount = self.table.rowCount()
                self.table.setRowCount(rowCount + 1)
                self.table.setItem(rowCount, 0,
                                   QTableWidgetItem(str(meal.id)))
                self.table.setItem(rowCount, 1,
                                   QTableWidgetItem(str(meal.Name)))
                self.table.setItem(rowCount, 2,
                                   QTableWidgetItem(str(drinks.id)))
                self.table.setItem(rowCount, 3,
                                   QTableWidgetItem(str(drinks.Name)))
                self.table.setItem(rowCount, 4,
                                   QTableWidgetItem(str(rest.id)))
                self.table.setItem(rowCount, 5,
                                   QTableWidgetItem(str(rest.Est_year)))
                self.table.setItem(rowCount, 6,
                                   QTableWidgetItem(str(rest.Num_of_meals)))
                self.table.setItem(rowCount, 7,
                                   QTableWidgetItem(str(rest.Prices)))
                self.table.setItem(rowCount, 8,
                                   QTableWidgetItem(str(rest.CEO)))
        self.table.resizeColumnsToContents()
        self.table.setColumnWidth(3, 200)
        self.table.setColumnWidth(8, 275)