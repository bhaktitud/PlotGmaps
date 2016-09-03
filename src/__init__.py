import os,sys
from src.mapframe import window
from PySide.QtGui import *
from PySide.QtCore import *


def run():
    app = QApplication(sys.argv)
    GUI = window()
    GUI.show()
    sys.exit(app.exec_())
    
    
if __name__ == '__main__':
    run()