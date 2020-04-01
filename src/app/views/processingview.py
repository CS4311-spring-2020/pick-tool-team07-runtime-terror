from PyQt5.QtCore import Qt

import os
from PyQt5.QtGui import QStandardItemModel, QStandardItem
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
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        # self.resize(700, 500)
        self.tableView = QTableView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['File Name', 'Source', 'Validation', 'Cleansing','Ingestion','Selection']) #set headers
        self.tableView.setModel(self.model)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #resize columns to fit into the widget

        start = QPushButton("Start Analysis")
        start.clicked.connect(self.update)

        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.tableView)
        self.vBoxLayout.addWidget(start)
        self.setLayout(self.vBoxLayout)

    def addToTable(self, logfile):
        name = QStandardItem(logfile.getLogName())
        source = QStandardItem(logfile.getPathToFile())
        validation = QStandardItem(str(logfile.getValidationStatus()))
        cleansing = QStandardItem(str(logfile.getLogCleansingStatus()))
        ingestion = QStandardItem(str(logfile.getIngestionStatus()))
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

    def updateTable(self): 
        pass
    
    def update(self): 
        self.logfileManager.addLogFile("file.py", "root/", "text")
        self.parent.updateView(1)
