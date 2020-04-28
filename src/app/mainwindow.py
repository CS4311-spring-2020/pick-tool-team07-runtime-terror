from PyQt5 import QtCore 
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QAction, QStackedLayout, QBoxLayout, QWidget,\
                            QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QToolBar, QToolButton

from app.views.analysisview import AnalysisView
from app.views.processingview import ProcessingView
from app.views.actionReportView import ActionReportView
from app.dialogs.projectconfigdialog import ProjectConfigDialog
#import dialog from edit vector configuration for edit Vector Process
from app.widgets.vectorconfigwidget import VectorConfigWidget

from processes.cleansing import CleansingThread
from processes.ingestion import IngestionThread

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

        #Sets home pic        
        # pic_label = QLabel()
        # home_page = QPixmap("app/images/PICK_home.png")
        # pic_label.setPixmap(home_page.scaled(self.width(),self.height(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation))

        # self.windowStack.addWidget(pic_label)
        self.windowStack.addWidget(self.analysisView)
        self.windowStack.addWidget(self.processingView)
        self.windowStack.addWidget(self.actionreportview)

        self.widget = QWidget()
        self.widget.setLayout(self.windowStack)

        self.setCentralWidget(self.widget)

    def setupToolBar(self):
        logProcessingView = QToolButton()
        logProcessingView.setText("Log Processing View")
        logProcessingView.clicked.connect(lambda: self.updateView(1))
        
        analysisView = QToolButton()
        analysisView.setText("Analysis View")
        analysisView.clicked.connect(lambda: self.updateView(0))

        actionreportView = QToolButton()
        actionreportView.setText("Action Report")
        actionreportView.clicked.connect(lambda: self.updateView(2))


        toolBar = QToolBar()
        toolBar.addWidget(logProcessingView)
        toolBar.addWidget(analysisView)
        toolBar.addWidget(actionreportView)

        self.toolbar = self.addToolBar(toolBar)


    def setupMenuBar(self): 
        # Menu Bar
        self.newProject = QAction("New Project", self)
        self.newProject.triggered.connect(self.newProjectProcess)

        self.editConfig = QAction("Edit Configuration", self)
        self.editConfig.triggered.connect(lambda: self.updateView(1))

        self.editVectorConfig = QAction("Edit Vector Configuration", self)
        self.editVectorConfig.triggered.connect(self.editVecProcess)

        self.menubar = self.menuBar()
        self.filemenu = self.menubar.addMenu("File")
        self.editmenu = self.menubar.addMenu("Edit")
        self.filemenu.addAction(self.newProject)
        self.editmenu.addAction(self.editConfig)
        self.editmenu.addAction(self.editVectorConfig)

    def keyPress(self, e): 
        pass
    
    def newProjectProcess(self):
        from PyQt5.QtWidgets import QDialog
        newProjectDialog = ProjectConfigDialog(self)
        newProjectDialog.exec()

        result = newProjectDialog.result()

        if result == QDialog.Accepted: 
            EventConfigManager.get_instance().save()
            self.analysisView.updateVectorList()
            thread = CleansingThread()
            thread.logfileadd_callback.connect(self.processingView.addToTable)
            thread.finished.connect(self.cleansingThreadDone)
            thread.start()
            self.threads.append(thread)
        else: 
            # Just putting this here in case we need to handel the rejected case
            pass

    def editVecProcess(self):
        from PyQt5.QtWidgets import QDialog
        dialog = QDialog(self)
        container = QHBoxLayout()
        newVectorEditDialog = VectorConfigWidget(self)
        container.addWidget(newVectorEditDialog)
        doneBtn = QPushButton("Done",self)
        container.addWidget(doneBtn)
        dialog.setLayout(container) 
        doneBtn.clicked.connect(lambda: dialog.accept())
        dialog.exec()
        
    def cleansingThreadDone(self):
        print("Im Here")
        thread = IngestionThread()
        thread.logentry_callback.connect(self.analysisView.addLogEntry)
        thread.start()
        self.threads.append(thread)

    def updateView(self, n): 
        self.windowStack.setCurrentIndex(n)
        self.setCentralWidget(self.widget)
