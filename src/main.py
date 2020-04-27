from PyQt5 import QtWidgets
from app.mainwindow import MainWindow

# THIS IS A TEST COMMENT FOR DEVELOP BRANCH
# WILL BE DELETED ONCE WE KNOW DEVELOP BRANCH IS 
# GOOD TO BE WORKED FROM

if __name__ == '__main__': 
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())