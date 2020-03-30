from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QFileDialog, QWidget, QListWidget, QStackedWidget, QTableView, QVBoxLayout,\
                            QHBoxLayout, QLabel, QPushButton, QRadioButton, QLineEdit, QDateTimeEdit, QSpacerItem, QSizePolicy

class DirConfigWidget(QWidget):
    def __init__(self, parent=None, eventManager=None):  
        super(DirConfigWidget, self).__init__(parent)
        self.eventConfigManager = eventManager
        self.initUI()

    def initUI(self): 
        viewLabel = QLabel()
        viewLabel.setText("Directory Configuration")
        viewLabel.setAlignment(Qt.AlignHCenter|Qt.AlignVCenter)
        viewLabelCon = QHBoxLayout()
        viewLabelCon.addWidget(viewLabel)

        # Root directory controls
        rootDirLbl = QLabel("Root Directory")
        self.rootDirPath = QLineEdit()
        self.rootDirBrowse = QPushButton("Browse")
        self.rootDirBrowse.clicked.connect(self.browse_root)
        
        # Root Directory controls container
        rootDirContainer = QHBoxLayout()
        rootDirContainer.addWidget(self.rootDirPath)
        rootDirContainer.addWidget(self.rootDirBrowse)

        # Red Folder controls
        redFolderLbl = QLabel("Red Team Folder")
        self.redFolderPath = QLineEdit()
        self.redFolderBrowse = QPushButton("Browse")
        self.redFolderBrowse.clicked.connect(lambda: self.browse_folder("red"))
        self.redFolderBrowse.setEnabled(False)

        # Red folder controls container
        redContainer = QHBoxLayout()
        redContainer.addWidget(self.redFolderPath)
        redContainer.addWidget(self.redFolderBrowse)

        # Blue Folder controls
        blueFolderLbl = QLabel("Blue Team Folder")
        self.blueFolderPath = QLineEdit()
        self.blueFolderBrowse = QPushButton("Browse")
        self.blueFolderBrowse.clicked.connect(lambda: self.browse_folder("blue"))
        self.blueFolderBrowse.setEnabled(False)

        # Blue folder controls container
        blueContainer = QHBoxLayout()
        blueContainer.addWidget(self.blueFolderPath)
        blueContainer.addWidget(self.blueFolderBrowse)

        # Blue Folder controls
        whiteFolderLbl = QLabel("White Team Folder")
        self.whiteFolderPath = QLineEdit()
        self.whiteFolderBrowse = QPushButton("Browse")
        self.whiteFolderBrowse.clicked.connect(lambda: self.browse_folder("white"))
        self.whiteFolderBrowse.setEnabled(False)

        # Blue folder controls container
        whiteContainer = QHBoxLayout()
        whiteContainer.addWidget(self.whiteFolderPath)
        whiteContainer.addWidget(self.whiteFolderBrowse)

        saveBtn = QPushButton("Save")
        saveBtn.clicked.connect(self.saveConfig)

        dirViewContainer = QVBoxLayout()
        dirViewContainer.addLayout(viewLabelCon)
        dirViewContainer.addWidget(rootDirLbl)
        dirViewContainer.addLayout(rootDirContainer)
        dirViewContainer.addWidget(redFolderLbl)
        dirViewContainer.addLayout(redContainer)
        dirViewContainer.addWidget(blueFolderLbl)
        dirViewContainer.addLayout(blueContainer)
        dirViewContainer.addWidget(whiteFolderLbl)
        dirViewContainer.addLayout(whiteContainer)
        dirViewContainer.addWidget(saveBtn)

        self.setLayout(dirViewContainer)

    def browse_root(self): 
        rootpath = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if rootpath: 
            self.enableBtns()
            self.setRootPath(rootpath)
    
    def browse_folder(self, ftype):
        rootpath = self.rootDirPath.text()
        folderpath = str(QFileDialog.getExistingDirectory(self, "Select Directory", rootpath)) 
        if ftype == "red": 
            self.redFolderPath.setText(folderpath)
        elif ftype == "blue": 
            self.blueFolderPath.setText(folderpath)
        else: 
            self.whiteFolderPath.setText(folderpath)

    def saveConfig(self):
        self.eventConfigManager.setDirAttributes(
            self.rootDirPath.text(),
            self.redFolderPath.text(),
            self.blueFolderPath.text(),
            self.whiteFolderPath.text()
        )

    def enableBtns(self):
        self.redFolderBrowse.setEnabled(True)
        self.blueFolderBrowse.setEnabled(True)
        self.whiteFolderBrowse.setEnabled(True)
    
    def setRootPath(self, path):
        self.rootDirPath.setText(path) 
        self.redFolderPath.setText(path)
        self.blueFolderPath.setText(path)
        self.whiteFolderPath.setText(path)