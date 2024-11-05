from PyQt5 import QtWidgets
import InterfaceOrder
import sqlite3
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtCore import QRegExp
from PyQt5.QtWidgets import QApplication, QCheckBox, QVBoxLayout, QWidget, QButtonGroup, QCalendarWidget

db = sqlite3.connect('orders.db')
cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users(
    fio TEXT,
    SNILS TEXT,
    date TEXT,
    doctor TEXT,
    time TEXT
)''')
db.commit()


class Order(QtWidgets.QMainWindow, InterfaceOrder.Ui_MainWindow):
    def __init__(self):
        super(Order,self).__init__()
        self.setupUi(self)
        self.setWindowTitle('Заказ талона')
        self.pushButton.clicked.connect(self.order)
        
        regExp = QRegExp("[0-9]*")
        validator = QRegExpValidator(regExp, self.lineEdit_3)
        self.lineEdit_3.setValidator(validator)
        
        regExp = QRegExp("[а-яА-Я\\s]+")
        validator = QRegExpValidator(regExp, self.lineEdit_2)
        self.lineEdit_2.setValidator(validator)
    
    def order(self):  
        date = self.dateEdit.date().toString('yyyy-MM-dd')
        doctor = self.comboBox.currentText()
        selected_time = None
        fio = self.lineEdit_2.text()
        snils = self.lineEdit_3.text()
        
        if len(fio) == 0:
            return
        if len(snils) == 0:
            return

        self.group = QButtonGroup()
        self.group.addButton(self.checkBox)
        self.group.addButton(self.checkBox_2)
        self.group.addButton(self.checkBox_3)
        self.group.setExclusive(True)

        if self.checkBox.isChecked():
            selected_time = self.checkBox.text()
        elif self.checkBox_2.isChecked():
            selected_time = self.checkBox_2.text()
        elif self.checkBox_3.isChecked():
            selected_time = self.checkBox_3.text()
        else:
            self.label.setText('Вы не указали время!')
            
        if len(str(snils)) == 11:
            cursor.execute("SELECT * FROM users WHERE date = ? AND time = ? AND doctor = ?", (date, selected_time, doctor))
            existing_order = cursor.fetchone()
            if existing_order:
                self.label.setText('Талон на это время и дату уже заказали!')
                return
            cursor.execute('INSERT INTO users (fio, snils, date, doctor, time) VALUES (?, ?, ?, ?, ?)', (fio, snils, date, doctor, selected_time))
            db.commit()
            self.label.setText('Вы успешно заказали талон!')
        else:
            self.label.setText('Неверно указан СНИЛС!')
        

App = QtWidgets.QApplication([])
window = Order()
window.show()
App.exec()
