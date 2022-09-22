from operator import le
import sys
import time
import traceback
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from model import Drink, Restaurants
from windows.MealWindow  import MealWindow
from windows.DrinksWindow import DrinkWindow



class Window(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.initUI()
        self.initActions()
        self.initMenu()
        self.initTable()
        self.fillTable()
        self.msg = QMessageBox()

    def initUI(self):
        btn_add = QPushButton("Add", self)
        btn_add.move(30, 30)
        btn_add.clicked.connect(self.onAdd)

        btn_add = QPushButton("Update", self)
        btn_add.move(130, 30)
        btn_add.clicked.connect(self.onUpdate)

        btn_add = QPushButton("Delete", self)
        btn_add.move(230, 30)
        btn_add.clicked.connect(self.onDel)



        ql = QLabel("Est_year: ", self)
        ql.move(1050, 60)
        ql = QLabel("Name_of_meal: ", self)
        ql.move(1050, 90)
        ql = QLabel("Refreshments: ", self)
        ql.move(1050, 120)
        ql = QLabel("M_price: ", self)
        ql.move(1050, 150)
        ql = QLabel("R_price: ", self)
        ql.move(1050, 180)
        ql = QLabel("Drinks: ", self)
        ql.move(1050, 210)

        self.qle_est_year = QLineEdit(self)
        self.qle_est_year.move(1150, 60)
        self.qle_name_of_meal = QLineEdit(self)
        self.qle_name_of_meal.move(1150, 90)
        self.qle_refreshments = QLineEdit(self)
        self.qle_refreshments.move(1150, 120)
        self.qle_m_price = QLineEdit(self)
        self.qle_m_price.move(1150, 150)
        self.qle_r_price = QLineEdit(self)
        self.qle_r_price.move(1150, 180)
        self.cbb_drinks = QComboBox(self)
        self.cbb_drinks.move(1150, 210)
        for item in Drink.objects():
            self.cbb_drinks.addItem(item.Name, item.MealID)


    def onAdd(self):
        try:
            est_year = int(self.qle_est_year.text())
            name_of_meal = self.qle_name_of_meal.text()
            refreshments = self.qle_refreshments.text()
            m_price = int(self.qle_m_price.text())
            r_price = int(self.qle_r_price.text())
            drinkID = self.cbb_drinks.currentData()


            rest = Restaurants(est_year, name_of_meal, refreshments, m_price, r_price, drinkID)
            rest.save()
            print(rest.Est_year)

            drink = rest.drinks
            meal = drink.meals
            row_count = self.table.rowCount()
            self.table.setRowCount(row_count + 1)
            self.table.setItem(row_count, 0,
                               QTableWidgetItem(str(rest.id)))
            self.table.setItem(row_count, 1,
                               QTableWidgetItem(str(rest.Est_year)))
            self.table.setItem(row_count, 2,
                               QTableWidgetItem(rest.Name_of_meal))
            self.table.setItem(row_count, 3,
                               QTableWidgetItem(rest.Refreshments))
            self.table.setItem(row_count, 4,
                               QTableWidgetItem(str(rest.M_price)))
            self.table.setItem(row_count, 5,
                               QTableWidgetItem(str(rest.R_price)))

            self.table.setItem(row_count, 6,
                               QTableWidgetItem(str(meal.Name)))
            self.table.setItem(row_count, 7,
                               QTableWidgetItem(str(drink.id)))
            self.table.setItem(row_count, 8,
                               QTableWidgetItem(drink.Name))
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setWindowTitle("Bajarildi")
            self.msg.setText("Ma'lumot saqlandi....")
            self.msg.show()
        except Exception as exp:
            self.msg.setIcon(QMessageBox.Critical)
            self.msg.setWindowTitle("Xatolik")
            self.msg.setText(str(exp))
            self.msg.show()

            traceback.print_exc()

    def onUpdate(self):
        try:
            id = int(self.table.item(self.sel_row, 0).text())
            est_year = int(self.qle_est_year.text())
            name_of_meals = self.qle_name_of_meal.text()
            refreshments = (self.qle_refreshments.text())
            m_price = int(self.qle_m_price.text())
            r_price = int(self.qle_r_price.text())
            drinkId = self.cbb_drinks.currentData()

            rest = Restaurants(est_year, name_of_meals, refreshments, m_price, r_price, drinkId, id)
            rest.save()


            drink = rest.drinks
            meal = drink.meals
            row_count = self.table.currentRow()
            self.table.setItem(row_count, 0,
                               QTableWidgetItem(str(rest.id)))
            self.table.setItem(row_count, 1,
                               QTableWidgetItem(str(rest.Est_year)))
            self.table.setItem(row_count, 2,
                               QTableWidgetItem(rest.Name_of_meal))
            self.table.setItem(row_count, 3,
                               QTableWidgetItem(rest.Refreshments))
            self.table.setItem(row_count, 4,
                               QTableWidgetItem(str(rest.M_price)))
            self.table.setItem(row_count, 5,
                               QTableWidgetItem(str(rest.R_price)))

            self.table.setItem(row_count, 6,
                               QTableWidgetItem(str(meal.name)))
            self.table.setItem(row_count, 7,
                               QTableWidgetItem(str(drink.id)))
            self.table.setItem(row_count, 8,
                               QTableWidgetItem(drink.Name))
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setWindowTitle("Bajarildi")
            self.msg.setText("Ma'lumot saqlandi....")
            self.msg.show()
        except Exception as exp:
            self.msg.setIcon(QMessageBox.Critical)
            self.msg.setWindowTitle("Xatolik")
            self.msg.setText(str(exp))
            self.msg.show()

            traceback.print_exc()

    def onDel(self):
        try:
            Est_year = int(self.table.item(self.sel_row, 1).text())
            Name_of_meal = (self.table.item(self.sel_row, 2).text())
            Refreshments = (self.table.item(self.sel_row, 3).text())
            M_price = int(self.table.item(self.sel_row, 4).text())
            R_price = int(self.table.item(self.sel_row, 5).text())
            DrinkId = int(self.table.item(self.sel_row, 7).text())
            id = int(self.table.item(self.sel_row, 0).text())

            resto = Restaurants(Est_year,Name_of_meal,Refreshments,M_price,R_price,DrinkId,id)
            resto.delete()
            self.qle_est_year.setText('')
            self.qle_name_of_meal.setText('')
            self.qle_refreshments.setText('')
            self.qle_m_price.setText('')
            self.qle_r_price.setText('')

            row_count = self.table.currentRow()
            self.table.removeRow(row_count)

            self.msg.setIcon(QMessageBox.Information)
            self.msg.setWindowTitle("Bajarildi")
            self.msg.setText("Ma'lumot o'chirildi....")
            self.msg.show()
        except Exception as exp:
            self.msg.setIcon(QMessageBox.Critical)
            self.msg.setWindowTitle("Xatolik")
            self.msg.setText(str(exp))
            self.msg.show()

            traceback.print_exc()

    def initTable(self):
        self.table = QTableWidget(self)  # Создаём таблицу
        self.table.move(30, 60)
        self.table.setMinimumSize(1000, 600)
        self.table.setColumnCount(9)     # Устанавливаем три колонки
        self.table.setSelectionBehavior(QTableWidget.SelectRows)

        # Устанавливаем заголовки таблицы
        self.table.setHorizontalHeaderLabels(
            ['Id', "Est_year", "Name_of_meals", "Refreshments", "M_price", "R_price", "Meal", "drink id", "Drinks"])

        self.table.hideColumn(0)
        self.table.hideColumn(7)
        self.table.clicked.connect(self.onClicked)

    def initActions(self):
        self.newAction = QAction("&New...", self)
        self.newAction.triggered.connect(self.onnewAction)
        self.openAction = QAction("&Open...", self)
        self.saveAction = QAction("&Save", self)
        self.exitAction = QAction("&Exit", self)

        self.mealAction = QAction("&Meals", self)
        self.mealAction.triggered.connect(self.onMealWindow)
        self.drinkAction = QAction("&Drinks", self)
        self.drinkAction.triggered.connect(self.onDrinksWindow)

    def fillTable(self):

        for rest in Restaurants.objects():
            drink = rest.drinks
            meal = drink.meals
            row_count = self.table.rowCount()
            self.table.setRowCount(row_count + 1)
            self.table.setItem(row_count, 0,
                               QTableWidgetItem(str(rest.id)))
            self.table.setItem(row_count, 1,
                               QTableWidgetItem(str(rest.Est_year)))
            self.table.setItem(row_count, 2,
                               QTableWidgetItem(rest.Name_of_meal))
            self.table.setItem(row_count, 3,
                               QTableWidgetItem(rest.Refreshments))
            self.table.setItem(row_count, 4,
                               QTableWidgetItem(str(rest.M_price)))
            self.table.setItem(row_count, 5,
                               QTableWidgetItem(str(rest.R_price)))

            self.table.setItem(row_count, 6,
                               QTableWidgetItem(str(meal.name)))
            self.table.setItem(row_count, 7,
                               QTableWidgetItem(str(drink.id)))
            self.table.setItem(row_count, 8,
                               QTableWidgetItem(drink.Name))
            # делаем ресайз колонок по содержимому
        self.table.resizeColumnsToContents()

    def onClicked(self):
        try:
            self.sel_row = self.table.currentRow()
            est_year = self.table.item(self.sel_row, 1).text()
            self.qle_est_year.setText(est_year)
            name_of_meal = self.table.item(self.sel_row, 2).text()
            self.qle_name_of_meal.setText(name_of_meal)
            refreshments = (self.table.item(self.sel_row, 3).text())
            self.qle_refreshments.setText(str(refreshments))
            m_price = int(self.table.item(self.sel_row, 4).text())
            self.qle_m_price.setText(str(m_price))
            r_price = int(self.table.item(self.sel_row, 5).text())
            self.qle_r_price.setText(str(r_price))
            drinkId = int(self.table.item(self.sel_row, 7).text())
            for i in range(self.cbb_drinks.count()):
                if self.cbb_drinks.itemData(i) == drinkId:
                    self.cbb_drinks.setCurrentIndex(i)
                    break
        except Exception as exp:
            self.msg.setIcon(QMessageBox.Critical)
            self.msg.setWindowTitle("Xatolik")
            self.msg.setText(str(exp))
            self.msg.show()

            traceback.print_exc()

    def onnewAction(self):
        pass

    def initMenu(self):
        menuBar = self.menuBar()
        self.setMenuBar(menuBar)

        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)

        servicesMenu = menuBar.addMenu("&Services")
        servicesMenu.addAction(self.mealAction)
        servicesMenu.addAction(self.drinkAction)

        helpMenu = menuBar.addMenu("&Help")

    def onMealWindow(self):
        self.mealw = MealWindow()
        self.mealw.show()

    def onDrinksWindow(self):
        self.drinkw = DrinkWindow()
        self.drinkw.show()


app = QApplication(sys.argv)

w = Window()
w.showMaximized()

app.exec()
