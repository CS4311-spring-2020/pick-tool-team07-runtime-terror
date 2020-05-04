from PyQt5.QtCore import Qt, QDate, QDateTime
from PyQt5.QtWidgets import QWidget, QVBoxLayout,QHBoxLayout, QLabel, QPushButton, QLineEdit, QDateTimeEdit

class EventConfigWidget(QWidget):
    def __init__(self, hide=False, parent=None, eventManager=None): 
        super(EventConfigWidget, self).__init__(parent) 
        self.hide = hide
        self.eventConfigManager = eventManager
        self.initUI()

    def initUI(self): 
        self.viewLabel = QLabel("Event Configuration")
        self.viewLabel.setAlignment(Qt.AlignHCenter|Qt.AlignVCenter)

        self.eventNameLbl = QLabel("Event Name")
        self.eventName = QLineEdit()

        self.eventDescriptionLbl = QLabel("Event Description")
        self.eventDescription = QLineEdit()

        self.startTimeLbl = QLabel("Start Date and Time")
        self.startTime = QDateTimeEdit(QDateTime.currentDateTime())
        self.startTime.setDisplayFormat("yyyy-MM-ddT-HH:mm:ssZ")

        self.endTimeLbl = QLabel("End Date and Time")
        self.endTime = QDateTimeEdit(QDateTime.currentDateTime())
        self.endTime.setDisplayFormat("yyyy-MM-ddT-HH:mm:ssZ")

        saveBtn = QPushButton("Save")
        saveBtn.clicked.connect(self.save)
        if self.hide == True: 
            saveBtn.hide()

        eventConfigContainer = QVBoxLayout()
        eventConfigContainer.addWidget(self.viewLabel)
        eventConfigContainer.addWidget(self.eventNameLbl)
        eventConfigContainer.addWidget(self.eventName)
        eventConfigContainer.addWidget(self.eventDescriptionLbl)
        eventConfigContainer.addWidget(self.eventDescription)
        eventConfigContainer.addWidget(self.startTimeLbl)
        eventConfigContainer.addWidget(self.startTime)
        eventConfigContainer.addWidget(self.endTimeLbl)
        eventConfigContainer.addWidget(self.endTime)
        eventConfigContainer.addWidget(saveBtn)

        self.setLayout(eventConfigContainer)

    def save(self):
        print(self.parent())
        print(self.hide)
        if self.parent() and self.hide == False: 
            self.parent().accept()
            
        self.eventConfigManager.setEventAttributes(
            self.eventName.text(), 
            self.eventDescription.text(), 
            self.startTime.dateTime().toPyDateTime(),#.toUTC(),
            self.endTime.dateTime().toPyDateTime()#.toUTC()
        )
        print(self.startTime.dateTime().toUTC().toString())


    def validateInputs(self):
        name = self.eventName.text()
        description = self.eventDescription.text()
        if (not name or not description):
            return False
        else:
            return True

    def validateTimeEqual(self):
        eq = self.startTime.dateTime().__ge__(self.endTime.dateTime())
        if(eq and not self.validateTimeLater()):
            return True
        else: 
            return False

    def validateTimeLater(self):
        sGreat = self.startTime.dateTime().__gt__(self.endTime.dateTime())
        if(sGreat):
            return True
        else: 
            return False