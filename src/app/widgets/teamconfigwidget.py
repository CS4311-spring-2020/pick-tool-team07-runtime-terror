from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QTableView, QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QRadioButton, QLineEdit

class TeamConfigWidget(QWidget):
    def __init__(self, parent=None, eventManager=None):
        super(TeamConfigWidget, self).__init__(parent)  
        self.eventConfigManager = eventManager
        self.initUI()

    def initUI(self):
        viewLabel = QLabel()
        viewLabel.setText("Team Configuration")
        viewLabel.setAlignment(Qt.AlignHCenter|Qt.AlignVCenter)

        self.leadRbtn = QRadioButton()
        self.leadRbtn.setText("Lead")

        self.leadIpLbl = QLabel()
        self.leadIpLbl.setText("Lead IP Address")
        self.leadIp = QLineEdit()
        
        self.ipContainer = QHBoxLayout()
        self.ipContainer.addWidget(self.leadIpLbl)
        self.ipContainer.addWidget(self.leadIp)

        self.connectionsLbl = QLabel()
        self.connectionsLbl.setText("Connections")

        self.connectionsView = QTableView()

        self.connectBtn = QPushButton()
        self.connectBtn.setText("Connect")
        self.connectBtn.clicked.connect(self.connect)


        teamViewContainer = QVBoxLayout()
        teamViewContainer.addWidget(viewLabel)
        teamViewContainer.addWidget(self.leadRbtn)
        teamViewContainer.addLayout(self.ipContainer)
        teamViewContainer.addWidget(self.connectionsLbl)
        teamViewContainer.addWidget(self.connectionsView)
        teamViewContainer.addWidget(self.connectBtn)

        self.setLayout(teamViewContainer)

    def connect(self): 
        #TODO: There will be a different interpretation of how this will be handled if 
        # the lead clicks connect.
        pass