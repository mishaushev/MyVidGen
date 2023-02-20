import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QProgressBar
from PyQt5.QtCore import QTimer
import MyVidGen

class MainWindow():
    
    #Main Window
    def my_ui_function():
        app = QApplication(sys.argv)
    win = QMainWindow()
    
    
    label = QtWidgets.QLabel(win)
    label.setText("Music Video Generator")
    label.move(50,50)
    
    b1 = QtWidgets.QPushButton(win)
    b1.setText("Click me")
    b1.clicked.connect(MyVidGen.my_vid_gen_exec())
    
    win.show()

class ProgressBar(QWidget):
    
    #Progress Bard
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Music Video Generator")
        self.resize(500,75)
        
        self.progressBar =QProgressBar(self)
        self.progressBar.setGeometry(25, 25, 300, 40)
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(0)
        
        #Increases Progress Bar Steps
        timer = QTimer(self)
        timer.timeout.connect(self.Increase_Step)
        timer.start(1000)
    
    def Increase_Step(self):
        self.progressBar.setValue(self.progressBar.value() + 1)

app = QApplication(sys.argv)

programm = ProgressBar()
programm.show()

sys.exit(app.exec_())





 