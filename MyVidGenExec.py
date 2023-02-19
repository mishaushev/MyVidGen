import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QPlainTextEdit, QHBoxLayout, QVBoxLayout

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        #Window Size
        self.window_width, self.window_height = 720, 900
        self.setMinimumSize(self.window_width, self.window_height)

        #Window Title
        self.setWindowTitle('MVGEN')
        layout = QVBoxLayout()
        self.setLayout(layout)

        #Command Line input Widget
        #self.editorCommand = QPlainTextEdit()
        #layout.addWidget(self.editorCommand, 3)

        #Command Line Output Widget
        self.editorOutput = QPlainTextEdit()
        layout.addWidget(self.editorOutput, 7)

        buttonLayout = QHBoxLayout()
        layout.addLayout(buttonLayout)

        #Main Button
        self.button_run = QPushButton('&Run Command', clicked=self.runCommand)
        buttonLayout.addWidget(self.button_run)

        #Clear Button
        self.button_clear = QPushButton('&Clear', clicked=lambda: self.editorOutput.clear())
        buttonLayout.addWidget(self.button_clear)

        #self.editorCommand.insertPlainText('dir')

    def runCommand(self):
        import MyVidGen
        
        #Call the function from MyVidGen.py
        MyVidGen.my_vid_gen_exec()   
        

if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QApplication.setAttribute(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    #App Instance
    app = QApplication(sys.argv)
    #App Style
    app.setStyleSheet('''
        QWidget {
            font-size: 30px;
        }
    ''')
    
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')

