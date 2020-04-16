from PyQt5.QtWidgets import QWidget, QDialog, QHBoxLayout, QVBoxLayout, QPushButton, QFormLayout, QLineEdit, QComboBox, QLabel
from app.views.graph.graphgenerator import GraphGenerator

class AddNodeWidget(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.initUI()

    def initUI(self): 
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.l = QFormLayout()
        buttons_layout = QHBoxLayout()

        main_layout.addLayout(self.l)
        main_layout.addLayout(buttons_layout)

        leNodeName = QLineEdit()
        leNodeLabel = QLineEdit()
        cbxNodeType = QComboBox()
        self.leImagePath = QLineEdit()

        pbOK = QPushButton()
        pbOK.clicked.connect(lambda: self.parent().accept())
        pbCancel = QPushButton()
        pbCancel.clicked.connect(lambda: self.parent().reject())
        browse = QPushButton("Browse")
        browse.clicked.connect(self.browse)
        browse.setEnabled(False)

        cbxNodeType.addItems(["None","circle","box", "image"])
        cbxNodeType.currentIndexChanged.connect(
            lambda: browse.setEnabled(True) if cbxNodeType.currentText() == "image" else browse.setEnabled(False))
        pbOK.setText("&OK")
        pbCancel.setText("&Cancel")
        buttons_layout.addWidget(pbOK)
        buttons_layout.addWidget(pbCancel)

        self.l.setWidget(0, QFormLayout.LabelRole, QLabel("Node Name"))
        self.l.setWidget(0, QFormLayout.FieldRole, leNodeName)
        self.l.setWidget(1, QFormLayout.LabelRole, QLabel("Node Label"))
        self.l.setWidget(1, QFormLayout.FieldRole, leNodeLabel)
        self.l.setWidget(2, QFormLayout.LabelRole, QLabel("Node Type"))
        self.l.setWidget(2, QFormLayout.FieldRole, cbxNodeType)
        self.l.setWidget(3, QFormLayout.LabelRole, QLabel("Node Image"))
        self.l.setWidget(3, QFormLayout.FieldRole, self.leImagePath)
        self.l.setWidget(4, QFormLayout.SpanningRole, browse)
    
    def getResults(self):
        results = [] 
        for i in range(self.l.rowCount()):
            item = self.l.itemAt(i, QFormLayout.FieldRole)
            try: 
                text = item.widget().text()
            except Exception:  
                text = item.widget().currentText()
            results.append(text)
        return results

    def browse(self): 
        from PyQt5.QtCore import QFileInfo
        from PyQt5.QtWidgets import QFileDialog
        imagepath = str(QFileDialog.getOpenFileName(self, "Select Image", filter="Image files (*.png *.jpg)")[0])
        print(imagepath)
        if imagepath: 
            self.leImagePath.setText(imagepath)

class AddEdgeWidget(QWidget): 
    def __init__(self, nodes, parent=None): 
        super(QWidget, self).__init__(parent)
        self.nodes = nodes
        self.initUI()

    def initUI(self): 
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        self.l = QFormLayout()
        buttons_layout = QHBoxLayout()

        main_layout.addLayout(self.l)
        main_layout.addLayout(buttons_layout)
        
        source = QComboBox()
        destination = QComboBox()

        pbOK = QPushButton()
        pbOK.clicked.connect(lambda: self.parent().accept())
        pbCancel = QPushButton()
        pbCancel.clicked.connect(lambda: self.parent().reject())
        source.addItems(self.nodes)
        destination.addItems(self.nodes)
        
        pbOK.setText("&OK")
        pbCancel.setText("&Cancel")
        buttons_layout.addWidget(pbOK)
        buttons_layout.addWidget(pbCancel)

        self.l.setWidget(0, QFormLayout.LabelRole, QLabel("Source Node"))
        self.l.setWidget(0, QFormLayout.FieldRole, source)
        self.l.setWidget(1, QFormLayout.LabelRole, QLabel("Destination Node"))
        self.l.setWidget(1, QFormLayout.FieldRole, destination)

    def getResults(self):
        source = self.l.itemAt(0, QFormLayout.FieldRole).widget().currentText()
        destination = self.l.itemAt(1, QFormLayout.FieldRole).widget().currentText()
        return (source, destination)

class GraphWidget(QWidget): 
    def __init__(self, parent=None): 
        super(QWidget, self).__init__(parent)
        self.graphGenerator = GraphGenerator()
        self.initUI()

    def initUI(self): 
        self.setLayout(QVBoxLayout())

        graphControls = QHBoxLayout()
        addNode = QPushButton("Add Node")
        addNode.clicked.connect(self.addNode)
        graphControls.addWidget(addNode)

        addEdge = QPushButton("Add Edge")
        addEdge.clicked.connect(self.addEdge)
        graphControls.addWidget(addEdge)

        self.layout().addLayout(graphControls)

        # selectedVector = self.vectorManager.getCurrentVector()
        # if selectedVector: 
        #     graphGenerator.generateVectorGraph(selectedVector)
        self.graphGenerator.build()
        qgv = self.graphGenerator.getGraph()
        self.layout().addWidget(qgv)

    def addNode(self): 
        dlg = QDialog()
        dlg.ok=False
        dlg.node_name=""
        dlg.node_label=""
        dlg.node_type="None"
        
        addNodeWidget = AddNodeWidget(dlg)
        dlg.setLayout(addNodeWidget.layout())

        dlg.exec()

        result = dlg.result()

        if result == QDialog.Accepted: 
            results=addNodeWidget.getResults()
            if results[2] == "image": 
                #TODO validate path to image
                self.graphGenerator.addNode(
                    name= results[0], 
                    label= results[1], 
                    shape= results[3]
                )
            else: 
                self.graphGenerator.addNode(
                    name= results[0], 
                    label= results[1], 
                    shape= results[2]
                )
        else: 
            # Just putting this here in case we need to handel the rejected case
            pass

        self.graphGenerator.build()

    def addEdge(self): 
        # nodes = self.graphGenerator.getNodes()
        dlg = QDialog()

        addEdgeWidget = AddEdgeWidget(
            [node.name for node in self.graphGenerator.getNodes()],
            dlg)
        dlg.setLayout(addEdgeWidget.layout())

        dlg.exec()

        result = dlg.result()

        if result == QDialog.Accepted: 
            results=addEdgeWidget.getResults()
            self.graphGenerator.addEdge(results[0], results[1])
        self.graphGenerator.build()

