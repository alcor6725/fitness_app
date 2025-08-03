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
        self.setWindowTitle("Fitness Tracker 1.2")
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
        
        self.load_table() # loads table on display



    # btn events
    def btn_click(self):
        self.add_btn.clicked.connect(self.add_workout)
        self.delete_btn.clicked.connect(self.delete_workout)
        self.submit_btn.clicked.connect(self.plot_data)
        self.clear_btn.clicked.connect(self.reset)

    # load_table from database
    def load_table(self):
        self.table.setRowCount(0)
        row = 0
        query = QSqlQuery("SELECT * FROM fitness ORDER BY date DESC")
        while query.next():
             id = query.value(0)  
             date = query.value(1)
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


    # add work out to database and display new row
    def add_workout(self):
        date = self.date_box.date().toString("yyyy-MM-dd")
        calories = self.kal_box.text()
        distance = self.distance_box.text()
        description = self.description.text()

        query = QSqlQuery("""INSERT INTO fitness(date, calories, distance, description)
                          VALUES (?,?,?,?)""")
        query.addBindValue(date)
        query.addBindValue(calories)
        query.addBindValue(distance)
        query.addBindValue(description)
        query.exec()
        
        self.load_table()

        self.date_box.setDate(QDate.currentDate)
        self.kal_box.clear()
        self.distance_box.clear()
        self.description.clear()


    # delete work out from database and update display
    def delete_workout(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "ERROR", "Please select row to delete")
        
        fit_id = int(self.table.item(selected_row, 0).text())

        confirm = QMessageBox.question(self,"Deleting selected workout", "Are You Sure?",
                                       QMessageBox.StandardButton.Yes|QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.No:
            return
        
        query = QSqlQuery()
        query.prepare("DELETE FROM fitness WHERE id =?")
        query.addBindValue(fit_id)
        query.exec()

        self.load_table()
      


    # display graph 
    def plot_data(self):
        calories = []
        distances =[]

        query = QSqlQuery("SELECT calories, distance FROM fitness ORDER BY calories ASC")
        while query.next():
            calorie = query.value(0)
            distance = query.value(1)
            calories.append(calorie)
            distances.append(distance)
        
        try:
            min_cal = min(calories)
            max_cal = max(calories)
            normalized_cal = [(cal - min_cal)/(max_cal - min_cal) for cal in calories]
            print(min_cal, max_cal)
            print(calories)
            print(distances)
            print(normalized_cal)
            
            plt.style.use("Solarize_Light2")
            ax = self.figure.subplots()
            ax.scatter(distances, calories, c=normalized_cal, cmap = 'viridis', label = "Data Points")
            ax.set_title("Distance Vs Calories")
            ax.set_xlabel("Distance (km)")
            ax.set_ylabel("Calories (cal)")
            #cbar = ax.figure.colorbar(ax.collections[0], label = "Normalized Calories")
            ax.legend()
            self.canvas.draw()
        
        except Exception as e:
            print("ERROR : {e}")
            QMessageBox.warning(self,"ERROR", "Data Missing")
            

    # Dark Mode

    # Reset
    def reset(self):
        self.date_box.setDate(QDate.currentDate())
        self.kal_box.clear()
        self.distance_box.clear()
        self.description.clear()
        self.figure.clear()
        self.canvas.draw()

# main

if __name__ == "__main__":
    app = QApplication([])
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("fitness.db")

    if not db.open():
        QMessageBox.critical(None, "ERROR", "Could not open Database")
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













