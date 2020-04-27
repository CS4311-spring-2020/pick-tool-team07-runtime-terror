from PyQt5.QtCore import Qt
import os
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QLabel,QCheckBox,QFrame, QGridLayout, QHBoxLayout, QVBoxLayout, QTableView,\
                            QTableWidget, QMainWindow, QTableWidgetItem, QHeaderView, QTabWidget, QListWidget, QLineEdit, QComboBox, QSpacerItem, QSizePolicy, QAction


class ActionReportView(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.title = "Action Report"
        self.initUI()

    def initUI(self):
        # TODO: ACTION REPORT VIEW
        self.setWindowTitle(self.title)
        #self.setGeometry(self.top, self.left, self.width, self.height)
        #self.tableview = QTableView()
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Filename', 'File path', 'Error Message', 'Error line'])
        self.tableview = QTableView()
        self.tableview.setModel(self.model)
        self.tableview.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # resize columns to fit into the widget

        self.vBoxLayout = QVBoxLayout()
        self.vBoxLayout.addWidget(self.tableview)
        self.setLayout(self.vBoxLayout)

        filename = QStandardItem("auth.log")
        filepath = QStandardItem("/home/eder/Desktop/pick/pick-tool-team07-runtime-terror/test/root/Blue")
        message = QStandardItem("cannot parse character")
        errorline = QStandardItem("23")

        self.model.appendRow([filename, filepath, message, errorline])
        self.tableview.setModel(self.model)