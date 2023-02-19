from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


def my_ui_function():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 300, 300)
    win.setWindowTitle("Music Video Generator")
    
    label = QtWidgets.QLabel(win)
    label.setText("Music Video Generator")
    label.move(50,50)
    
    b1 = QtWidgets.QPushButton(win)
    b1.setText("Click me")
    b1.clicked.connect(clicked)
    
    win.show()
    sys.exit(app.exec_())

def clicked():
    
    # Import the module
    import MyVidGen

        
    #Call the function from MyVidGen.py
    MyVidGen.my_vid_gen_exec()    