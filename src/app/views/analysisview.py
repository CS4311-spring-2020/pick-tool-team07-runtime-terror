import sys
sys.path.append("../..")
from managers.vectormanager import VectorManager

from app.views.graph.graphgenerator import GraphGenerator

from PyQt5.QtCore import Qt, QSize
<<<<<<< HEAD
from PyQt5.QtGui import QIcon, QPixmap, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QDialog,QFrame, QGridLayout, QHBoxLayout, QVBoxLayout, QTableView,QTableWidget, QTabWidget,\
                            QListWidget, QListWidgetItem, QLineEdit, QComboBox, QSpacerItem, QSizePolicy, QAction, QAbstractItemView,\
                            QHeaderView
=======
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QDialog,QFrame, QGridLayout, QHBoxLayout, QVBoxLayout, QTableView,QTableWidget, QTabWidget,\
                            QListWidget, QListWidgetItem, QLineEdit, QComboBox, QSpacerItem, QSizePolicy, QAction, QAbstractItemView
>>>>>>> b76c6e8c70917cc11d680a95d1fcaf6f76eaa0f4

class AnalysisView(QWidget): 
    def __init__(self, parent=None): 
        super(QWidget, self).__init__(parent)
        self.vectorManager = VectorManager.get_instance()
        self.initUI()

    def initUI(self): 
        self.setupMainLayout()
        self.setLayout(self.mainLayout)

    def setupMainLayout(self): 
        #Log Entries table
        self.logEntriesTbl = QTableView()
<<<<<<< HEAD
        self.logEntryModel = QStandardItemModel()
        self.logEntryModel.setHorizontalHeaderLabels(['Host', 'Timestamp', 'Content', 'Source', 'Source Type'])
        self.logEntriesTbl.setModel(self.logEntryModel)
        self.logEntriesTbl.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

=======
>>>>>>> b76c6e8c70917cc11d680a95d1fcaf6f76eaa0f4
        self.setupVectorTab()

        self.tabWidget = QTabWidget()
        self.tabWidget.addTab(self.logEntriesTbl, "Log Entries")
        self.tabWidget.addTab(self.vectorTab, "Vector View")

        # Label for our Vector List
        vectorLbl = QListWidgetItem()
        vectorLbl.setText("Vector Databases")
        vectorLbl.setTextAlignment(Qt.AlignCenter)
        vectorLbl.setFlags(Qt.NoItemFlags)

        # Defined Vectors list
        self.vectorWidget = QListWidget()
        self.vectorWidget.setDragDropMode(QAbstractItemView.DragDrop)
        self.vectorWidget.setAcceptDrops(True)
        self.vectorWidget.addItem(vectorLbl)
        self.vectorWidget.itemActivated.connect(self.setVectorSelected)

        self.workspace = QHBoxLayout()
        self.workspace.addWidget(self.vectorWidget, 10)
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
        self.graph = QWidget()
        self.graph.setLayout(QVBoxLayout())
        self.setupGraph()
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

    def setupGraph(self): 
        graph = self.graph
        graphGenerator = GraphGenerator()
        selectedVector = self.vectorManager.getCurrentVector()
        if selectedVector: 
            graphGenerator.generateVectorGraph(selectedVector)
        graphGenerator.build()
        qgv = graphGenerator.getGraph()
        graph.layout().addWidget(qgv)

    def updateVectorList(self):
        vectors = self.vectorManager.getVectors()
        for vector in vectors: 
            icon = QIcon()
            icon.addPixmap(QPixmap("app/images/dbicon.png"), QIcon.Normal, QIcon.Off)
            item = QListWidgetItem()
            item.setText(vector.getName()) 
            item.setIcon(icon)
            item.setSizeHint(QSize(0, 50))
            self.vectorWidget.addItem(item)

<<<<<<< HEAD
    def addLogEntry(self, logentry):
        print(logentry)
        host = QStandardItem(logentry.getHost())
        timestamp = QStandardItem(logentry.getTimestamp())
        content = QStandardItem(logentry.getContent())
        source = QStandardItem(logentry.getSource())
        sourcetype = QStandardItem(logentry.getSourceType())

        self.logEntryModel.appendRow([
            host,
            timestamp, 
            content,
            source,
            sourcetype
        ])
        self.logEntriesTbl.setModel(self.logEntryModel)

=======
>>>>>>> b76c6e8c70917cc11d680a95d1fcaf6f76eaa0f4
    def setVectorSelected(self, item): 
        selVecName = item.text()
        print(selVecName)
        self.vectorManager.setCurrentVector(selVecName)
    