import os

from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon, QBrush, QColor
from PyQt5.QtWidgets import QWidget, QLabel,QCheckBox,QFrame, QGridLayout, QHBoxLayout, QVBoxLayout, QTableView,\
                            QTableWidget, QAbstractScrollArea,  QHeaderView, QMainWindow, QTableWidgetItem, QTabWidget, QListWidget, QLineEdit, QComboBox, QSpacerItem, QSizePolicy, QAction,\
                            QPushButton

from managers.logfilemanager import LogFileManager
# TODO: This view is missing buttons and also should we change it, so that we make a tab view and we can set the 
# ActionReport view there? 

class ProcessingView(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.title = "Log Processing"
        self.logFileManager = LogFileManager()
        # controller will tell view to update when a new LogFile is created
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.top, self.left, self.width, self.height)
        # self.resize(700, 500)
        self.tableView = QTableView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['File Name', 'Source', 'Validation', 'Cleansing','Ingestion','Selection']) #set headers
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #resize columns to fit into the widget

        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.tableView)
        self.setLayout(self.vBoxLayout)

    def addToTable(self, logfile):
        name = QStandardItem(logfile.getLogName())
        source = QStandardItem(logfile.getPathToFile()) 


        # Wrost implementation of all but this will do, probably should
        # be changed
        validation = QStandardItem()
        if logfile.getValidationStatus() == "null": 
            validation.setText("IN-PROGRESS")
            validation.setBackground(QBrush(QColor("yellow")))
        elif not logfile.getValidationStatus(): 
            validation.setText("FAILED")
            validation.setBackground(QBrush(QColor("red")))
        else: 
            validation.setText("PASSED")
            validation.setBackground(QBrush(QColor("green")))

        cleansing = QStandardItem()
        if logfile.getLogCleansingStatus() == "null": 
            cleansing.setText("IN-PROGRESS")
            cleansing.setBackground(QBrush(QColor("yellow")))
        elif not logfile.getLogCleansingStatus(): 
            cleansing.setText("FAILED")
            cleansing.setBackground(QBrush(QColor("red")))
        else: 
            cleansing.setText("PASSED")
            cleansing.setBackground(QBrush(QColor("green")))
                
        ingestion = QStandardItem()
        if logfile.getIngestionStatus() == "null": 
            ingestion.setText("IN-PROGRESS")
            ingestion.setBackground(QBrush(QColor("yellow")))
        elif not logfile.getIngestionStatus(): 
            ingestion.setText("FAILED")
            ingestion.setBackground(QBrush(QColor("red")))
        else: 
            ingestion.setText("PASSED")
            ingestion.setBackground(QBrush(QColor("green")))
        
        self.model.appendRow([
            name, 
            source, 
            validation, 
            cleansing, 
            ingestion, 
            QStandardItem()])
        self.tableView.setModel(self.model)
        
    def deleteFromTable(self): 
        pass

    def updateRowStatus(self, logfile, process): 
        red = QStandardItem("FAILED")
        red.setBackground(QBrush(QColor("red")))

        green = QStandardItem("PASSED")
        green.setBackground(QBrush(QColor("green")))

        yellow = QStandardItem("IN-PROGRESS")
        yellow.setBackground(QBrush(QColor("yellow")))

        item = None
        row = -1 
        col = -1
        for index in range(self.model.rowCount()): 
            qindex = self.model.index(index, 0)
            name = self.model.data(qindex)

            if name == logfile.getLogName(): 
                row = index
                if process == "validation": 
                    col = 2
                    if logfile.getValidationStatus() == "null": 
                        item = yellow
                    elif not logfile.getValidationStatus(): 
                        item = red
                    else: 
                        item = green
                elif process == "cleansing":
                    col = 3
                    if logfile.getLogCleansingStatus() == "null": 
                        item = yellow
                    elif not logfile.getLogCleansingStatus(): 
                        item = red
                    else: 
                        item = green         
                else: 
                    col = 4
                    if logfile.getIngestionStatus() == "null": 
                        item = yellow 
                    elif not logfile.getIngestionStatus(): 
                        item = red
                    else: 
                        item = green

                break

        self.model.setItem(row, col, item)
        self.tableView.setModel(self.model)
                

    def update(self): 
        # self.logFileManager.addLogFile("file.py", "root/", "text")
        self.parent.updateView(1)
