from abc import ABC, abstractmethod
from atexit import register
from colorsys import yiq_to_rgb
from ctypes import resize
import datetime
from re import L
from tkinter.messagebox import RETRY
import traceback
from settings import db_path
import sqlite3


class BaseModel(ABC):

    def __init__(self, id=None) -> None:
        self.id = id
        self.__isValid = True

    @property
    def isValid(self):
        return self.__isValid

    @isValid.setter
    def isValid(self, isValid):
        self.__isValid = isValid

    @abstractmethod
    def print():
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @classmethod
    @abstractmethod
    def objects():
        pass

    @classmethod
    @abstractmethod
    def get_by_id(id):
        pass


class Meals(BaseModel):
    table = 'Meal'

    def __init__(self, name, id=None) -> None:
        super().__init__(id)
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self.__name = name
        else:
            self.__name = ''
            self.__isValid = False

    def print():
        pass

    def save(self):
        if self.isValid:
            try:
                with sqlite3.connect(db_path) as conn:
                    cursor = conn.cursor()
                    try:
                        if self.id is None:
                            # insert, create new object (row)
                            cursor.execute(f'''
                                INSERT INTO {Meals.table} ('Name')
                                VALUES ('{self.name}')
                            ''')
                            self.id = cursor.lastrowid
                        else:
                            # update existing row
                            conn.execute(f'''
                                UPDATE {Meals.table} set Name = '{self.name}' where ID = {self.id}
                            ''')

                            conn.commit()
                    except:
                        print('Saqlashda xatolik bo\'ldi')
                        conn.rollback()
                return True
            except:
                print('Bog\'lanishda xatolik')
        else:
            return False

    def delete(self):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Delete From  {Meals.table} where ID = {self.id}
                """
                cursor.execute(query)
                conn.commit()
        except:
            print('Bog\'lanishda xatolik')

    def objects():
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Select *From  {Meals.table}
                """
                for row in cursor.execute(query):
                    yield Meals(row[1], row[0])
        except:
            print('Bog\'lanishda xatolik')

    def get_by_id(id):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            query = f"""
                Select *From  {Meals.table}
                Where ID={id}
                """
            res = cursor.execute(query).fetchone()
            if res is not None:
                return Meals(res[1], res[0])
            else:
                return None

    def __str__(self):
        return f'{self.name}'


class Drink(BaseModel):
    table = 'Drinks'

    def __init__(self, Name, MealID, id=None) -> None:
        super().__init__(id)
        self.Name = Name
        self.MealID = MealID

    @property
    def Name(self):
        return self.__Name

    @Name.setter
    def Name(self, Name):
        if isinstance(Name, str):
            self.__Name = Name
        else:
            self.__Name = ''
            self.__isValid = False

    @property
    def MealID(self):
        return self.__MealID

    @MealID.setter
    def MealID(self, MealID):
        if isinstance(MealID, int) and Meals.get_by_id(MealID) is not None:
            self.__MealID = MealID
        else:
            self.__MealID = None
            self.__isValid = False

    @property
    def meals(self):
        return Meals.get_by_id(self.MealID)

    def print():
        pass

    def save(self):
        if self.isValid:
            try:
                with sqlite3.connect(db_path) as conn:
                    cursor = conn.cursor()
                    try:
                        if self.id is None:
                            # insert, create new object (row)
                            cursor.execute(f'''
                                INSERT INTO {Drink.table} ('Name', MealID)
                                VALUES ('{self.Name}', {self.MealID})
                            ''')
                            self.id = cursor.lastrowid
                        else:
                            # update existing row

                            conn.execute(f'''
                                UPDATE {Drink.table} set Name = '{self.Name}', RegionId={self.MealID} where Id = {self.id}
                            ''')

                            conn.commit()
                    except:
                        print('Saqlashda xatolik bo\'ldi')
                        conn.rollback()
                return True
            except:
                print('Bog\'lanishda xatolik')
        else:
            return False

    def delete(self):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Delete From  {Drink.table} where ID = {self.id}
                """
                cursor.execute(query)
                conn.commit()
        except:
            print('Bog\'lanishda xatolik')

    def objects():
        try:
            print(db_path)
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Select *From  {Drink.table}
                """
                for row in cursor.execute(query):
                    yield Drink(row[1], row[2], row[0])
        except:
            print('Bog\'lanishda xatolik')

    def get_by_id(id):
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            query = f"""
                Select *From  {Drink.table}
                Where ID={id}
                """
            res = cursor.execute(query).fetchone()
            if res is not None:
                return Drink(res[1], res[2], res[0])
            else:
                return None

    def __str__(self):
        return f'{self.meals}\t | {self.Name}'


class Restaurants(BaseModel):
    table = 'Restaurant'

    def __init__(self, Est_year, Name_of_meal,Refreshments,M_price, R_price, Drinksid, id=None) -> None:
        super().__init__(id)
        self.Est_year = Est_year
        self.Name_of_meal = Name_of_meal
        self.Refreshments = Refreshments
        self.M_price = M_price
        self.R_price = R_price
        self.Drinksid = Drinksid

    @property
    def Est_year(self):
        return self.__Est_year

    @Est_year.setter
    def Est_year(self, Est_year):
        if isinstance(Est_year, int):
            self.__Est_year = Est_year
        else:
            self.__Est_year = 0
            self.__isValid = False

    @property
    def Name_of_meal(self):
        return self.__Name_of_meal

    @Name_of_meal.setter
    def Name_of_meal(self, Name_of_meal):
        if isinstance(Name_of_meal, str):
            self.__Name_of_meal = Name_of_meal
        else:
            self.__Name_of_meal = ''
            self.__isValid = False

    @property
    def Refreshments(self):
        return self.__Refreshments

    @Refreshments.setter
    def Refreshments(self, Refreshments):
        if isinstance(Refreshments, str):
            self.__Refreshments = Refreshments
        else:
            self.__Refreshments = ''
            self.__isValid = False

    @property
    def M_price(self):
        return self.__M_price

    @M_price.setter
    def M_price(self, M_price):
        if isinstance(M_price, int):
            self.__M_price = M_price
        else:
            self.__M_price = 0
            self.__isValid = False

    @property
    def R_price(self):
        return self.__R_price

    @R_price.setter
    def R_price(self, R_price):
        if isinstance(R_price, int):
            self.__R_price = R_price
        else:
            self.__R_price = 0
            self.__isValid = False

    @property
    def Drinksid(self):
        return self.__Drinksid

    @Drinksid.setter
    def Drinksid(self, Drinksid):
        if isinstance(Drinksid, int):
            self.__Drinksid = Drinksid
        else:
            self.__Drinksid = 0
            self.__isValid = False

    @property
    def drinks(self):
        return Drink.get_by_id(self.Drinksid)

    def del_by_id(id):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Delete From  {Restaurants.table} where ID = {id}
                """
                cursor.execute(query)
                conn.commit()
        except:
            print('Bog\'lanishda xatolik')

    def save(self):
        if self.isValid:
            try:

                with sqlite3.connect(db_path) as conn:

                    cursor = conn.cursor()
                    try:
                        if self.id is None:

                            # insert, create new object (row)
                            cursor.execute(f'''
                                INSERT INTO {Restaurants.table} (Est_year, Name_of_meal, Refreshments, M_price, R_price, Drinksid)
                                VALUES ({self.Est_year}, '{self.Name_of_meal}', '{self.Refreshments}', {self.M_price}, {self.R_price}, {self.Drinksid})
                            ''')
                            print("hi")
                            self.id = cursor.lastrowid
                        else:
                            # update existing row

                            conn.execute(f'''
                                UPDATE {Restaurants.table} set
                                Est_year = {self.Est_year},
                                Name_of_meal = '{self.Name_of_meal}',
                                Refreshments = '{self.Refreshments}',
                                M_price = {self.M_price},
                                R_price = {self.R_price},
                                Drinksid = {self.Drinksid}
                                where ID = {self.id}
                            ''')

                            conn.commit()
                    except:
                        print('Saqlashda xatolik bo\'ldi')
                        conn.rollback()
                        raise
                return True
            except:
                print('Bog\'lanishda xatolik')
                raise

        else:
            return False

    def delete(self):
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                print(self.id)
                query = f"""
                Delete From  {Restaurants.table} where ID = {self.id}
                """
                cursor.execute(query)
                conn.commit()
        except:
            print('Bog\'lanishda xatolik')

    def objects():
        try:
            print(db_path)
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                query = f"""
                Select *From  {Restaurants.table}
                """
                for row in cursor.execute(query):
                    yield Restaurants(row[1], row[2], row[3], row[4], row[5], row[6], row[0])
        except:
            traceback.print_exc()
            print('Bog\'lanishda xatolik')

    def print():
        pass

    def get_by_id(id):
        pass