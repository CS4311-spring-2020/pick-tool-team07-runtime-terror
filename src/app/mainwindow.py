from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QAction, QStackedLayout, QBoxLayout, QWidget,\
                            QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QToolBar, QToolButton



from app.views.analysisview import AnalysisView
from app.views.processingview import ProcessingView
from app.dialogs.projectconfigdialog import ProjectConfigDialog
#import dialog from edit vector configuration for edit Vector Process
from app.widgets.vectorconfigwidget import VectorConfigWidget

# TODO: Add save and restoring abilities to the application
class MainWindow(QMainWindow): 
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self): 
        self.setMinimumSize(500,500)
        self.showMaximized()
        self.setupMenuBar()
        self.setupToolBar()

        self.windowStack = QStackedLayout()

        self.analysisView = AnalysisView(self)
        self.processingView = ProcessingView(self)

        #Sets home pic        
        pic_label = QLabel()
        home_page = QPixmap("PICK_home.png")
        pic_label.setPixmap(home_page.scaled(self.width(),self.height(), QtCore.Qt.IgnoreAspectRatio, QtCore.Qt.FastTransformation))

        self.windowStack.addWidget(pic_label)
        self.windowStack.addWidget(self.analysisView)
        self.windowStack.addWidget(self.processingView)

        self.widget = QWidget()
        self.widget.setLayout(self.windowStack)

        self.setCentralWidget(self.widget)

    def setupToolBar(self):
        logProcessingView = QToolButton()
        logProcessingView.setText("Log Processing View")
        logProcessingView.clicked.connect(lambda: self.updateView(2))
        
        analysisView = QToolButton()
        analysisView.setText("Analysis View")
        analysisView.clicked.connect(lambda: self.updateView(1))

        toolBar = QToolBar()
        toolBar.addWidget(logProcessingView)
        toolBar.addWidget(analysisView)

        self.toolbar = self.addToolBar(toolBar)


    def setupMenuBar(self): 
        # Menu Bar
        self.newProject = QAction("New Project", self)
        self.newProject.triggered.connect(self.newProjectProcess)

        self.editConfig = QAction("Edit Configuration", self)
        self.editConfig.triggered.connect(lambda: self.updateView(1))

        #edit vector configuration in menu bar
        self.editVectorConfig = QAction("Edit Vector Configuration", self)
        self.editVectorConfig.triggered.connect(self.editVecProcess)

        self.menubar = self.menuBar()
        self.filemenu = self.menubar.addMenu("File")
        self.editmenu = self.menubar.addMenu("Edit")
        self.filemenu.addAction(self.newProject)
        self.editmenu.addAction(self.editConfig)
        #place edit vector configuration option in the menu bar
        self.editmenu.addAction(self.editVectorConfig)

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
        else: 
            # Just putting this here in case we need to handel the rejected case
            pass

    def editVecProcess(self):
        from PyQt5.QtWidgets import QDialog
        #first create the dialog object
        dialog = QDialog(self)
        # create a new container with a horizontal 
        # layout that we will add vector editor to so we can 
        # add that to the qdialog 
        container = QHBoxLayout()
        # create a new instance of the the vector config widget
        newVectorEditDialog = VectorConfigWidget(self)
        # then place the instance of the new widget into the 
        # container with the horizontal layout
        container.addWidget(newVectorEditDialog)
        # create push button
        doneBtn = QPushButton("Done",self)
        # add the button to the container
        container.addWidget(doneBtn)
        #apply layout to dailog
        dialog.setLayout(container) 
        # how to add layout to qdialog
        #show event loop using dialog.exec()
        doneBtn.clicked.connect(lambda: dialog.accept())
        dialog.exec()
        
        

    def updateView(self, n): 
        self.windowStack.setCurrentIndex(n)
        self.setCentralWidget(self.widget)
