# imports
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
                            QApplication, QWidget, QLabel, QLineEdit, QDateEdit, QCheckBox,
                            QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout,
                            QVBoxLayout, QHeaderView)
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np
from sys import exit





# main class
class Fitness(QWidget):
    def __init__(self):
        super().__init__()
        self.settings()
        self.initUI()
        self.btn_click()
        
        
    def settings(self):
        self.setWindowTitle("Fitness Tracker")
        self.resize(800, 600)
      
    
    # initUI
    def initUI(self):

        #create widgets
        self.date_box = QDateEdit()
        self.date_box.setDate(QDate.currentDate())
        self.kal_box = QLineEdit()
        self.kal_box.setPlaceholderText("Number of Calories")
        self.distance_box = QLineEdit()
        self.distance_box.setPlaceholderText("Distance")
        self.description = QLineEdit()
        self.description.setPlaceholderText("Enter a description")

        self.darkmode = QCheckBox("Dark Mode")

        self.add_btn = QPushButton("Add")
        self.delete_btn = QPushButton("Delete")
        self.submit_btn = QPushButton("Submit")
        self.clear_btn = QPushButton("Clear")

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Date"," Calories", "Distance", " Description"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)


        #Design Layout
        self.master_layout = QHBoxLayout()
        self.col1 = QVBoxLayout()
        self.col2 = QVBoxLayout()
        self.subrow1 = QHBoxLayout()
        self.subrow2 = QHBoxLayout()
        self.subrow3 = QHBoxLayout()
        self.subrow4 = QHBoxLayout()
        self.btnrow1 = QHBoxLayout()
        self.btnrow2 = QHBoxLayout()

        self.subrow1.addWidget(QLabel("Date:"))
        self.subrow1.addWidget(self.date_box)
        self.subrow2.addWidget(QLabel("Cal:"))
        self.subrow2.addWidget(self.kal_box)
        self.subrow3.addWidget(QLabel("KM:"))
        self.subrow3.addWidget(self.distance_box)
        self.subrow4.addWidget(QLabel("Des:"))
        self.subrow4.addWidget(self.description)

        self.col1.addLayout(self.subrow1)
        self.col1.addLayout(self.subrow2)
        self.col1.addLayout(self.subrow3)
        self.col1.addLayout(self.subrow4)
        self.col1.addWidget(self.darkmode)

        self.btnrow1.addWidget(self.add_btn)
        self.btnrow1.addWidget(self.delete_btn)
        self.btnrow2.addWidget(self.submit_btn)
        self.btnrow2.addWidget(self.clear_btn)

        self.col1.addLayout(self.btnrow1)
        self.col1.addLayout(self.btnrow2)

        self.col2.addWidget(self.canvas)
        self.col2.addWidget(self.table)

        self.master_layout.addLayout(self.col1, 30)
        self.master_layout.addLayout(self.col2, 70)
        self.setLayout(self.master_layout)
        
        self.load_table()
   

    # Events
    def btn_click(self):
        self.add_btn.clicked.connect(self.add_workout)
    
  

    # load past table
    def load_table(self):
        self.table.setRowCount(0)
        row = 0
        query = QSqlQuery("SELECT * FROM fitness ORDER BY date DESC")
        while query.next():
            id = query.value(0) # first column
            date = query.value(1) # second column
            calories = query.value(2)
            distance = query.value(3)
            description = query.value(4)

            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(id)))
            self.table.setItem(row, 1, QTableWidgetItem(date))
            self.table.setItem(row, 2, QTableWidgetItem(str(calories)))
            self.table.setItem(row, 3, QTableWidgetItem(str(distance)))
            self.table.setItem(row, 4, QTableWidgetItem(description))
            row +=1
            
    

    # Add workout
    def add_workout(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        calories = self.kal_box.text()
        distance = self.distance_box.text()
        description = self.description.text()

        query = QSqlQuery(
                          """
                          INSERT INTO fitness (date, calories, distance, description)
                          VALUES (?,?,?,?)
                          """)   
        query.addBindValue(date)
        query.addBindValue(calories)
        query.addBindValue(distance)
        query.addBindValue(description)
        query.exec()

        self.load_table()
        self.date_box.setDate(QDate.currentDate())
        self.kal_box.clear()
        self.distance_box.clear()
        self.description.clear()



        

    # Delete tables


    # Calculate Calories


    # click functionality


    # Dark Mode



    # Reset



# initialize database, outside class beacuse I need different database for each user




# main

if __name__ == "__main__":
    app = QApplication([])

    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("fitness.db")

    if not db.open():
        QMessageBox.critical(None, "ERROR", "cannot open database")
        exit(2)

    query = QSqlQuery()
    query.exec("""
           CREATE TABLE IF NOT EXISTS fitness(
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           date TEXT,
           calories REAL,
           distance REAL,
           description TEXT)
           """)
    fitness = Fitness()
    fitness.show()
    app.exec()












