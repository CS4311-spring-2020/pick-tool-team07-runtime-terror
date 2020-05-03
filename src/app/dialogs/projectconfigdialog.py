import sys
sys.path.append("../..")

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QListWidget, QStackedWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy, QMessageBox

from managers.eventconfigmanager import EventConfigManager

from app.widgets.dirconfigwidget import DirConfigWidget
from app.widgets.teamconfigwidget import TeamConfigWidget
from app.widgets.eventconfigwidget import EventConfigWidget
from app.widgets.vectorconfigwidget import VectorConfigWidget

class ProjectConfigDialog(QDialog): 
    def __init__(self, parent):
        super(ProjectConfigDialog, self).__init__(parent)
        self.eventConfigManager = EventConfigManager.get_instance()
        self.parent = parent
        self.initUI()

    def initUI(self): 
        self.resize(850,600)
        self.teamConfig = TeamConfigWidget(parent=self, eventManager=self.eventConfigManager)
        self.dirConfig = DirConfigWidget(parent=self, eventManager=self.eventConfigManager)
        self.eventConfig = EventConfigWidget(parent=self, eventManager=self.eventConfigManager)
        self.vectorConfig = VectorConfigWidget(parent=self, eventManager=self.eventConfigManager)
        
        self.stack = QStackedWidget(self)
        self.stack.addWidget(self.teamConfig)
        self.stack.addWidget(self.dirConfig)
        self.stack.addWidget(self.eventConfig)
        self.stack.addWidget(self.vectorConfig)

        self.viewList = QListWidget()
        self.viewList.insertItem(0, "Team Configuration")
        self.viewList.insertItem(1, "Directory Configuration")
        self.viewList.insertItem(2, "Event Configuration")
        self.viewList.insertItem(3, "Vector Configuration")
        self.viewList.currentRowChanged.connect(lambda i : self.stack.setCurrentIndex(i))

        startNewProject = QPushButton("Start New Project")
        startNewProject.clicked.connect(self.start)

        cancel = QPushButton("Cancel")
        cancel.clicked.connect(self.cancel)
        hSpacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Fixed)

        newProjectControlContainer = QHBoxLayout()
        newProjectControlContainer.addItem(hSpacer)
        newProjectControlContainer.addWidget(cancel)
        newProjectControlContainer.addWidget(startNewProject)

        viewContainer = QHBoxLayout()
        viewContainer.addWidget(self.viewList, 30)
        viewContainer.addWidget(self.stack, 60)

        mainContainer = QVBoxLayout(self)
        mainContainer.addLayout(viewContainer)
        mainContainer.addLayout(newProjectControlContainer)

        self.setLayout(mainContainer)

    def start(self):

        msg = QMessageBox()
        msg.setWindowTitle("warning")
        msg.setText("Please fill in missing fields")
        msg.setIcon(QMessageBox.Critical)
        msg.setStandardButtons(QMessageBox.Retry)

        vec = self.vectorConfig.checkIfThereAreVectors() 
        dirc = self.dirConfig.validateInputs()
        eventc = self.eventConfig.validateInputs()
        equalTime = self.eventConfig.validateTimeEqual()
        startLater = self.eventConfig.validateTimeLater()
        vecmsg = "Must have at least one vector"
        dircmsg = "Directory Configuration"
        eventmsg = "Event Configuration"
        timeEqual = "Start and End time can not be equal"
        timeStartLater = "End time can not be before start time"
        
        
        l = [""]

        if (vec and dirc and eventc and (not equalTime or not startLater)):
            self.parent.updateView(2)
            self.accept()
        else:
            if not vec:
                l.append(vecmsg)
                l.append("\n")
            if not dirc:
                l.append(dircmsg)
                l.append("\n")
            if not eventc:
                l.append(eventmsg)
                l.append("\n")
            if (equalTime):
                l.append("-"+timeEqual)
                l.append("\n")
            if (startLater):
                l.append("-"+timeStartLater)
                l.append("\n")
            #list of msgs together and join them into single string 
            msg.setInformativeText(''.join(l))
            answer = msg.exec()
            if answer == QMessageBox.Retry:
                msg.close()
        


    def cancel(self): 
        self.reject()
        # self.done(0)

