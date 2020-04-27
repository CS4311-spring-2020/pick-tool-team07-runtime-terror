from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal  
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QAction, QStackedLayout, QBoxLayout, QWidget,\
                            QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QToolBar, QToolButton



from app.views.analysisview import AnalysisView
from app.views.processingview import ProcessingView
from app.views.actionReportView import ActionReportView
from app.dialogs.projectconfigdialog import ProjectConfigDialog

from managers.logfilemanager import LogFileManager
from managers.eventconfigmanager import EventConfigManager

class CleansingThread(QThread): 
    logfileadd_callback = pyqtSignal(object)

    def __init__(self): 
        super(CleansingThread, self).__init__()
        self.logfilemanager = LogFileManager()
        self.eventConfig = EventConfigManager.get_instance().getEventConfig()
        

    def run(self): 
        self.remove_empty()
        self.createLogFiles()

    def createLogFiles(self):
        import os
        print("IN GETFIles")
        for dirName, subdirList, filelist in os.walk(self.eventConfig.getRootDir(), topdown=False):
            for fname in filelist:
                self.logfilemanager.addLogFile(fname, dirName + "/" + fname, os.path.splitext(fname))
                self.logfilemanager.updateCleanseStatus(fname, True)
                self.logfileadd_callback.emit(self.logfilemanager.getLogFile(fname))

    def remove_empty(self):
        import os
        print("IN REMOVE EMPTY")
        for dirName, subdirList, filelist in os.walk(self.eventConfig.getRootDir(), topdown=False):
            for fname in filelist:
                if (fname != '.DS_Store'):
                    with open(dirName + "/" + fname) as in_file, open((dirName + "/" + fname), 'r+') as out_file:
                        print(fname)
                        out_file.writelines(line for line in in_file if line.strip())
                        out_file.truncate()

from splunk.splunkinterface import SplunkClient
from managers.logentrymanager import LogEntryManager
class IngestionThread(QThread): 
    logfile_callback = pyqtSignal(object)
    logentry_callback = pyqtSignal(object)

    def __init__(self):
        super(IngestionThread, self).__init__()
        self.splunk = SplunkClient()
        self.fileManager = LogFileManager()
        self.entryManager = LogEntryManager.get_instance()

    def run(self): 
        logFiles = self.fileManager.getLogFiles()

        for logFile in logFiles: 
            if logFile.getIngestionStatus(): 
                continue

            logFilePath = logFile.getPathToFile()
            print(logFilePath)
            self.splunk.upload(logFilePath)

            results = self.splunk.results(logFilePath)

            for result in results: 
                self.entryManager.addEntry(
                    result["host"], 
                    result["timestamp"], 
                    result["content"], 
                    result["source"], 
                    result["sourcetype"] 
                )
                self.logentry_callback.emit(
                    self.entryManager.getEntryByContent(result["content"]))

            # We need some form to verify if we actually got results from splunk
            logFile.setIngestionStatus(True)

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

        self.menubar = self.menuBar()
        self.filemenu = self.menubar.addMenu("File")
        self.editmenu = self.menubar.addMenu("Edit")
        self.filemenu.addAction(self.newProject)
        self.editmenu.addAction(self.editConfig)

    def keyPress(self, e): 
        pass
    
    def newProjectProcess(self):
        from PyQt5.QtWidgets import QDialog
        newProjectDialog = ProjectConfigDialog(self)
        newProjectDialog.exec()

        result = newProjectDialog.result()

        if result == QDialog.Accepted: 
            print("Accepted")
            self.analysisView.updateVectorList()
            thread = CleansingThread()
            thread.logfileadd_callback.connect(self.processingView.addToTable)
            thread.finished.connect(self.cleansingThreadDone)
            thread.start()
            self.threads.append(thread)
        else: 
            # Just putting this here in case we need to handel the rejected case
            pass

    def cleansingThreadDone(self):
        print("Im Here")
        thread = IngestionThread()
        thread.logentry_callback.connect(self.analysisView.addLogEntry)
        thread.start()
        self.threads.append(thread)

    def updateView(self, n): 
        self.windowStack.setCurrentIndex(n)
        self.setCentralWidget(self.widget)
