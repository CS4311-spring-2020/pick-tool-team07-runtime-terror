from PyQt5.QtCore import Qt

import os
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
        self.top = 100
        self.left = 100
        self.width = 500
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.resize(700, 500)
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(['File Name', 'Source', 'Validation', 'Cleansing','Ingestion','Selection']) #set headers
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) #resize columns to fit into the widget
        row = self.tableWidget.rowCount()
        self.tableWidget.insertRow(row)

        start = QPushButton("Start Analysis")
        start.clicked.connect(self.update)

        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.tableWidget)
        self.vBoxLayout.addWidget(start)
        self.setLayout(self.vBoxLayout)

    def startProcess(self):
        # TODO: Needs to be updated once we have a SplunkInterface to communicate with splunk
        # Also we need to add a CleansingProcess or CleansingManager? 
        row = 0
        # root_dir will come from event config right?
        #root_dir = self.
        for dirName, subdirList, fileList in os.walk(root_dir, topdown=False):
            print('Found directory: %s' % dirName)
            for fname in fileList:
                print('\t%s' % fname)
                print ()
                # x = 10
                info = QTableWidgetItem(fname)
                vName = QTableWidgetItem(fname)
                cName = QTableWidgetItem(fname)
                iName = QTableWidgetItem(fname)
                checkBox = QCheckBox()
                source = QTableWidgetItem(dirName)
                self.tableWidget.setItem(row, 1, source)
                self.tableWidget.setItem(row, 0, info)
                self.tableWidget.setItem(row, 2, vName)
                self.tableWidget.setItem(row, 3, cName)
                self.tableWidget.setItem(row, 4, iName)
                self.tableWidget.setCellWidget(row, 5, checkBox)
                # the code below was to show the the file when on ingestion, cleansing, validation (it was hard coded)
                for i in range(4):
                    self.tableWidget.takeItem(i, 2)
                    self.tableWidget.takeItem(i + 10, 2)
                    i += 1
                for x in range(2, 4) and range(8, 10):
                    self.tableWidget.takeItem(x, 3)
                    x += 1
                for y in range(3, 10) and range(15, 25):
                    self.tableWidget.takeItem(y, 4)
                    y += 1
                row += 1

    # this will probably be removed once we update the MainWindow view structure
    def update(self): 
        self.parent.updateView(1)
