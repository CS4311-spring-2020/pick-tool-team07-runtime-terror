import sys
sys.path.append("../..")
from managers.vectormanager import VectorManager
from managers.nodemanager import NodeManager
from managers.logentrymanager import LogEntryManager

from app.views.graph.graphwidget import GraphWidget

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import Qt, QSize, QEvent, pyqtSlot
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QStandardItem, QFontMetrics, QPalette
from PyQt5.QtWidgets import QWidget, QDialog,QFrame, QGridLayout, QHBoxLayout, QVBoxLayout, QTableView,QTableWidget, QTabWidget,\
                            QListWidget, QListWidgetItem, QLineEdit, QComboBox, QSpacerItem, QSizePolicy, QAction, QAbstractItemView,\
                            QHeaderView, QListWidget, QStyledItemDelegate, qApp, QLabel

class AnalysisView(QWidget): 
    def __init__(self, parent=None): 
        super(QWidget, self).__init__(parent)
        self.vectorManager = VectorManager()
        self.nodeManager = NodeManager()
        self.logentryManager = LogEntryManager.get_instance()
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
        nodeModel = QStandardItemModel()
        nodeModel.setHorizontalHeaderLabels([
            "Name", 
            "Timestamp", 
            "Description", 
            "Log Entry Refrence", 
            "Log Creator", 
            "Icon", 
            "Source", 
            "Visible"
        ])
        self.nodes.setModel(nodeModel)
        # self.nodes.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.vectorViews = QHBoxLayout()
        self.vectorViews.addWidget(self.nodes, 30)
        self.vectorViews.addWidget(self.graph, 70)

        hSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed)
        vectorsLable = QLabel("Vectors")
        self.vectorsCB = QComboBox()
        self.vectorsCB.currentIndexChanged.connect(self.vectorHandle)
        self.vectorAdded()
        # self.unitsCb = QComboBox()
        # self.interval = QLineEdit()

        # Graph controls such as orientation, interval units, interval
        self.graphContols = QHBoxLayout()
        self.graphContols.addItem(hSpacer)
        self.graphContols.addWidget(vectorsLable)
        self.graphContols.addWidget(self.vectorsCB)
        # self.graphContols.addWidget(self.unitsCb)
        # self.graphContols.addWidget(self.interval)

        self.container = QVBoxLayout()
        self.container.addLayout(self.graphContols)
        self.container.addLayout(self.vectorViews)

        self.vectorTab = QWidget()
        self.vectorTab.setLayout(self.container)

    def vectorAdded(self):
        self.vectorsCB.clear()
        self.vectorsCB.addItem("")
        vectors = self.vectorManager.getVectors()
        for vector in vectors: 
            self.vectorsCB.addItem(vector.getName())

    def vectorHandle(self, item):
        vectorname = self.vectorsCB.currentText()
        vector = self.vectorManager.getVectorByName(vectorname)
        if vector == None: 
            return 
        # Update node tableview
        nodeModel = self.nodes.model()
        nodeModel.removeRows(0, nodeModel.rowCount())
        for nodeId in vector.getNodes(): 
            node = self.nodeManager.getNode(nodeId)
            # "Name", "Timestamp", "Description", "Log Entry Refrence", "Log Creator", "Icon", "Source", "Visible"
            nodeModel.appendRow([
                QStandardItem(node.getName()), 
                QStandardItem(node.getTimeStamp()), 
                QStandardItem(node.getDesc()), 
                QStandardItem(node.getLogEntryRef()), 
                QStandardItem(node.getLogCreator()), 
                QStandardItem(node.getIcon()), 
                QStandardItem(node.getSource()), 
                QStandardItem(node.getVisible())
            ])
        self.nodes.setModel(nodeModel)

        # Todo add nodes to graph


    def addLogEntry(self, logentry):
        host = QStandardItem(logentry.getHost())
        timestamp = QStandardItem(logentry.getTimestamp())
        content = QStandardItem(logentry.getContent())
        source = QStandardItem(logentry.getSource())
        sourcetype = QStandardItem(logentry.getSourceType())

        testWidget = QtWidgets.QWidget()
        combobox = CheckableComboBox(testWidget)
        combobox.itemcheck_callback.connect(self.handelLogEntryChange)
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

    def handelLogEntryChange(self, item): 
        if item.checkState() == Qt.Checked: 
            vectorName = item.text()
            row = item.row()
            logEntryContent = self.logEntryModel.item(row, 2).text()
            logentry = self.logentryManager.getEntryByContent(logEntryContent)
            vector = self.vectorManager.getVectorByName(vectorName)
            self.vectorManager.associateLogEntry(logentry, vector)
        else: 
            # TODO: Remove association
            print("uncheck")


class CheckableComboBox(QComboBox):
    itemcheck_callback = QtCore.pyqtSignal(QStandardItem)
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

                self.itemcheck_callback.emit(item)
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
   