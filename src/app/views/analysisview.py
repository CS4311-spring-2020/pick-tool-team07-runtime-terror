import sys
sys.path.append("../..")
from managers.vectormanager import VectorManager
from managers.logentrymanager import LogEntry

from app.views.graph.graphwidget import GraphWidget

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt, QSize, QEvent
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QStandardItem, QFontMetrics, QPalette
from PyQt5.QtWidgets import QWidget, QDialog,QFrame, QGridLayout, QHBoxLayout, QVBoxLayout, QTableView,QTableWidget, QTabWidget,\
                            QListWidget, QListWidgetItem, QLineEdit, QComboBox, QSpacerItem, QSizePolicy, QAction, QAbstractItemView,\
                            QHeaderView, QListWidget, QStyledItemDelegate, qApp

class AnalysisView(QWidget): 
    def __init__(self, parent=None): 
        super(QWidget, self).__init__(parent)
        self.vectorManager = VectorManager()
        self.initUI()

    def initUI(self): 
        self.setupMainLayout()
        self.setLayout(self.mainLayout)

    def setupMainLayout(self): 
        #Log Entries table
        self.logEntriesTbl = QTableView()
        self.logEntryModel = QStandardItemModel()
        self.logEntryModel.setHorizontalHeaderLabels(['Host', 'Timestamp', 'Content', 'Source', 'Source Type', 'Associated Vectors'])
        self.logEntriesTbl.setModel(self.logEntryModel)
        self.logEntriesTbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.setupVectorTab()

        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.logEntriesTbl, "Log Entries")
        self.tabWidget.addTab(self.vectorTab, "Vector View")

        # Label for our Vector List
        vectorLbl = QListWidgetItem()
        vectorLbl.setText("Vector Databases")
        vectorLbl.setTextAlignment(Qt.AlignCenter)
        vectorLbl.setFlags(Qt.NoItemFlags)

        self.workspace = QHBoxLayout()
        #self.workspace.addWidget(self.vectorWidget, 10)
        self.workspace.addWidget(self.tabWidget,90)

        # Filtering and search
        hSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.search = QLineEdit()
        self.search.setFixedWidth(250)
        self.filterBox = QComboBox()

        # Container for tab/table controls 
        self.controls = QHBoxLayout()
        self.controls.addItem(hSpacer)
        self.controls.addWidget(self.search)
        self.controls.addWidget(self.filterBox)

        # Container for all workspace
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.controls)
        self.mainLayout.addLayout(self.workspace)

    def setupVectorTab(self): 
        self.graph = GraphWidget()
        self.nodes = QTableView()

        self.vectorViews = QHBoxLayout()
        self.vectorViews.addWidget(self.nodes, 30)
        self.vectorViews.addWidget(self.graph, 70)

        hSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.orientationCb = QComboBox()
        self.unitsCb = QComboBox()
        self.interval = QLineEdit()

        # Graph controls such as orientation, interval units, interval
        self.graphContols = QHBoxLayout()
        self.graphContols.addItem(hSpacer)
        self.graphContols.addWidget(self.orientationCb)
        self.graphContols.addWidget(self.unitsCb)
        self.graphContols.addWidget(self.interval)

        self.container = QVBoxLayout()
        self.container.addLayout(self.graphContols)
        self.container.addLayout(self.vectorViews)

        self.vectorTab = QWidget()
        self.vectorTab.setLayout(self.container)

    def updateVectorList(self):
        vectors = self.vectorManager.getVectors()
        for vector in vectors: 
            icon = QIcon()
            icon.addPixmap(QPixmap("app/images/dbicon.png"), QIcon.Normal, QIcon.Off)
            item = QListWidgetItem()
            item.setText(vector.getName()) 
            item.setIcon(icon)
            item.setSizeHint(QSize(0, 50))
            #self.vectorWidget.addItem(item)

    def addLogEntry(self, logentry):
        host = QStandardItem(logentry.getHost())
        timestamp = QStandardItem(logentry.getTimestamp())
        content = QStandardItem(logentry.getContent())
        source = QStandardItem(logentry.getSource())
        sourcetype = QStandardItem(logentry.getSourceType())

        testWidget = QtWidgets.QWidget()
        combobox = CheckableComboBox(testWidget)
        #combobox.setModel(self.logEntryModel)
        vectors = self.vectorManager.getVectors()
        for vector in vectors: 
            combobox.addItem(vector.name)

        self.logEntryModel.appendRow([
            host,
            timestamp, 
            content,
            source,
            sourcetype,
        ]) 

        row = self.logEntryModel.rowCount() - 1
        col = self.logEntryModel.columnCount() - 1
        a = self.logEntryModel.index(row, col)
        self.logEntriesTbl.setIndexWidget(a, combobox)

    def setVectorSelected(self, item): 
        selVecName = item.text()
        self.vectorManager.setCurrentVector(selVecName)

class CheckableComboBox(QComboBox):

    # Subclass Delegate to increase item height
    class Delegate(QStyledItemDelegate):
        def sizeHint(self, option, index):
            size = super().sizeHint(option, index)
            size.setHeight(20)
            return size

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make the combo editable to set a custom text, but readonly
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        # Make the lineedit the same color as QPushButton
        palette = qApp.palette()
        palette.setBrush(QPalette.Base, palette.button())
        self.lineEdit().setPalette(palette)

        # Use custom delegate
        self.setItemDelegate(CheckableComboBox.Delegate())

        # Update the text when an item is toggled
        self.model().dataChanged.connect(self.updateText)

        # Hide and show popup when clicking the line edit
        self.lineEdit().installEventFilter(self)
        self.closeOnLineEditClick = False

        # Prevent popup from closing when clicking on an item
        self.view().viewport().installEventFilter(self)

    def resizeEvent(self, event):
        # Recompute text to elide as needed
        self.updateText()
        super().resizeEvent(event)

    def eventFilter(self, object, event):

        if object == self.lineEdit():
            if event.type() == QEvent.MouseButtonRelease:
                if self.closeOnLineEditClick:
                    self.hidePopup()
                else:
                    self.showPopup()
                return True
            return False

        if object == self.view().viewport():
            if event.type() == QEvent.MouseButtonRelease:
                index = self.view().indexAt(event.pos())
                item = self.model().item(index.row())

                if item.checkState() == Qt.Checked:
                    item.setCheckState(Qt.Unchecked)
                else:
                    item.setCheckState(Qt.Checked)
                return True
        return False

    def showPopup(self):
        super().showPopup()
        # When the popup is displayed, a click on the lineedit should close it
        self.closeOnLineEditClick = True

    def hidePopup(self):
        super().hidePopup()
        # Used to prevent immediate reopening when clicking on the lineEdit
        self.startTimer(100)
        # Refresh the display text when closing
        self.updateText()

    def timerEvent(self, event):
        # After timeout, kill timer, and reenable click on line edit
        self.killTimer(event.timerId())
        self.closeOnLineEditClick = False

    def updateText(self):
        texts = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                texts.append(self.model().item(i).text())
        text = ", ".join(texts)

        # Compute elided text (with "...")
        metrics = QFontMetrics(self.lineEdit().font())
        elidedText = metrics.elidedText(text, Qt.ElideRight, self.lineEdit().width())
        self.lineEdit().setText(elidedText)

    def addItem(self, text, data=None):
        item = QStandardItem()
        item.setText(text)
        if data is None:
            item.setData(text)
        else:
            item.setData(data)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setData(Qt.Unchecked, Qt.CheckStateRole)
        self.model().appendRow(item)

    def addItems(self, texts, datalist=None):
        for i, text in enumerate(texts):
            try:
                data = datalist[i]
            except (TypeError, IndexError):
                data = None
            self.addItem(text, data)

    def currentData(self):
        # Return the list of selected items data
        res = []
        for i in range(self.model().rowCount()):
            if self.model().item(i).checkState() == Qt.Checked:
                res.append(self.model().item(i).data())
        return res
   