from PyQt5 import QtCore 
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QAction, QStackedLayout, QBoxLayout, QWidget,\
                            QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QToolBar, QToolButton, QDialog, QButtonGroup

from app.views.analysisview import AnalysisView
from app.views.processingview import ProcessingView
from app.views.actionReportView import ActionReportView
from app.dialogs.projectconfigdialog import ProjectConfigDialog
#import dialog from edit vector configuration for edit Vector Process
from app.widgets.vectorconfigwidget import VectorConfigWidget
from app.widgets.eventconfigwidget import EventConfigWidget

from processes.cleansing import CleansingThread
from processes.ingestion import IngestionThread

from managers.eventconfigmanager import EventConfigManager

# TODO: Add save and restoring abilities to the application
class MainWindow(QMainWindow): 
    def __init__(self):
        super(MainWindow, self).__init__()
        self.threads = []
        self.initUI()

    def initUI(self): 
        self.setMinimumSize(500,500)
        self.showMaximized()
        self.setupMenuBar()
        self.setupToolBar()

        self.windowStack = QStackedLayout()

        self.analysisView = AnalysisView(self)
        self.processingView = ProcessingView(self)
        self.actionreportview = ActionReportView(self)

        self.windowStack.addWidget(self.analysisView)
        self.windowStack.addWidget(self.processingView)
        self.windowStack.addWidget(self.actionreportview)

        self.widget = QWidget()
        self.widget.setLayout(self.windowStack)

        self.setCentralWidget(self.widget)

    def setupToolBar(self):
        toolBar = QToolBar()
        self.toolbar = self.addToolBar(toolBar)

        logProcessingView = QToolButton()
        logProcessingView.setText("Log Processing View")
        logProcessingView.setCheckable(True)
        logProcessingView.clicked.connect(lambda: self.updateView(1))

        analysisView = QToolButton()
        analysisView.setText("Analysis View")
        analysisView.setCheckable(True)
        analysisView.clicked.connect(lambda: self.updateView(0))

        actionreportView = QToolButton()
        actionreportView.setText("Action Report")
        actionreportView.setCheckable(True)
        actionreportView.clicked.connect(lambda: self.updateView(2))

        group = QButtonGroup(self)
        group.exclusive()

        for button in (
                analysisView,
                logProcessingView,
                actionreportView
        ):
            toolBar.addWidget(button)
            group.addButton(button)



    def setupMenuBar(self): 
        # Menu Bar
        self.newProject = QAction("New Project", self)
        self.newProject.triggered.connect(self.newProjectProcess)

        self.editConfig = QAction("Edit Configuration", self)
        self.editConfig.triggered.connect(self.editConfigDialog)

        self.editVectorConfig = QAction("Edit Vector Configuration", self)
        self.editVectorConfig.triggered.connect(self.editVecProcess)

        self.menubar = self.menuBar()
        self.filemenu = self.menubar.addMenu("File")
        self.editmenu = self.menubar.addMenu("Edit")
        self.filemenu.addAction(self.newProject)
        self.editmenu.addAction(self.editConfig)
        self.editmenu.addAction(self.editVectorConfig)
    
    def newProjectProcess(self):
        newProjectDialog = ProjectConfigDialog(self)
        newProjectDialog.exec()

        result = newProjectDialog.result()

        if result == QDialog.Accepted: 
            EventConfigManager.get_instance().save()
            self.analysisView.vectorAdded()

            # TODO Start all processing threads
            cleansing_thread = CleansingThread()
            cleansing_thread.logfileadd_callback.connect(self.processingView.addToTable)
            cleansing_thread.finished.connect(lambda: self.threads.remove(cleansing_thread))
            cleansing_thread.start()
            self.threads.append(cleansing_thread)

            ingestion_thread = IngestionThread()
            ingestion_thread.logfile_callback.connect(self.processingView.updateRowStatus)
            ingestion_thread.logentry_callback.connect(self.analysisView.addLogEntry)
            ingestion_thread.finished.connect(lambda: self.threads.remove(ingestion_thread))
            ingestion_thread.start()
            self.threads.append(ingestion_thread)
        else: 
            # Just putting this here in case we need to handel the rejected case
            pass

    def editVecProcess(self):
        dialog = QDialog(self)
        container = QHBoxLayout()
        newVectorEditDialog = VectorConfigWidget(self)
        container.addWidget(newVectorEditDialog)
        doneBtn = QPushButton("Done",self)
        container.addWidget(doneBtn)
        dialog.setLayout(container) 
        doneBtn.clicked.connect(lambda: dialog.accept())
        dialog.exec()

    def editConfigDialog(self): 
        dialog = QDialog(self)
        config = EventConfigWidget(parent=dialog, eventManager=EventConfigManager.get_instance())

        container = QVBoxLayout()
        container.addWidget(config)
        dialog.setLayout(container)
        dialog.exec()


    def updateView(self, n): 
        self.windowStack.setCurrentIndex(n)
        self.setCentralWidget(self.widget)
