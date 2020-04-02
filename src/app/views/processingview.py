import os

from PyQt5.QtCore import Qt, QVariant
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QLabel,QCheckBox,QFrame, QGridLayout, QHBoxLayout, QVBoxLayout, QTableView,\
                            QTableWidget, QAbstractScrollArea,  QHeaderView, QMainWindow, QTableWidgetItem, QTabWidget, QListWidget, QLineEdit, QComboBox, QSpacerItem, QSizePolicy, QAction,\
                            QPushButton

# TODO: This view is missing buttons and also should we change it, so that we make a tab view and we can set the 
# ActionReport view there? 

class ProcessingView(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.title = "Log Processing"
        self.logFileManager = LogFileManager().get_instance()
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

        checkIcon = QIcon()
        checkIcon.addPixmap(QPixmap("app/images/check.png"), QIcon.Normal, QIcon.Off)
        errorIcon = QIcon()
        errorIcon.addPixmap(QPixmap("app/images/error.png"), QIcon.Normal, QIcon.Off)
        
        validation = QStandardItem()
        if logfile.getValidationStatus(): 
            validation.setIcon(checkIcon)
        else: 
            validation.setIcon(errorIcon)

        cleansing = QStandardItem()
        if logfile.getLogCleansingStatus(): 
            cleansing.setIcon(checkIcon)
        else: 
            cleansing.setIcon(errorIcon)
        
        ingestion = QStandardItem()
        if logfile.getIngestionStatus(): 
            ingestion.setIcon(checkIcon)
        else: 
            ingestion.setIcon(errorIcon)
        
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
        self.logFileManager.addLogFile("file.py", "root/", "text")
        self.parent.updateView(1)
