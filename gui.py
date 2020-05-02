import sys, os
from pathlib import Path
from subprocess import call, check_output
from time import sleep
import json
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QSplashScreen, QMainWindow, QApplication, QPlainTextEdit, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QFileDialog, QInputDialog
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtGui import QIcon, QPixmap
            
class Splash(QDialog):
    def __init__(self, parent=None):
        super(Splash, self).__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.splash = QSplashScreen(QPixmap('/home/bob/present/proj/WorksArea/icons/logo.png'))
        self.splash.show()
        QTimer.singleShot(5000, self.splash.close)
        
class iac2tf(QMainWindow):
    def __init__(self):
        super(iac2tf, self).__init__()
        self.initUI()
        self.setGeometry(0, 0, 1700, 1000)
        self.setWindowTitle('Iac 2 Tf')
        self.setStyleSheet('background-color : lightblue')
        self.leftTextBox = QPlainTextEdit(self)
        self.leftTextBox.move(135, 50)
        self.leftTextBox.resize(650,930)          
        self.leftTextBox.setStyleSheet('background-color : white')
        self.leftTextBox.appendPlainText(str("HERE WILL BE YOUR INPUT IaC-File"))
        self.rightTextBox = QPlainTextEdit(self)
        self.rightTextBox.move(925, 50)
        self.rightTextBox.resize(650,930)
        self.rightTextBox.setStyleSheet('background-color : white')
        self.rightTextBox.appendPlainText(str("THIS WILL HOUSE THE TERRFORM OUTPUT FILE"))       

    #fill main screen
    def initUI(self): 
       # self.openFilebutton = self.button('openFile', 'Open File', self.open,110,30,5,50)
        self.openFile = QtWidgets.QPushButton('Open File',self)
        self.openFile.clicked.connect(self.open)
        self.openFile.setStyleSheet("background-color: green")
        self.openFile.resize(130,30)
        self.openFile.move(5,50)
        
        self.ProcessFile = QtWidgets.QPushButton('Process File',self)
        self.ProcessFile.clicked.connect(self.processFile)
        self.ProcessFile.setStyleSheet("background-color: green")
        self.ProcessFile.resize(130,30)
        self.ProcessFile.move(5, 80)     
               
        self.refreshRight = QtWidgets.QPushButton('Clear Right Text Area', self)
        self.refreshRight.setStyleSheet("background-color: red")
        self.refreshRight.clicked.connect(lambda:self.rightTextBox.setPlainText("THIS WILL HOUSE THE TERRFORM OUTPUT FILE"))
        self.refreshRight.resize(130,30)
        self.refreshRight.move(795, 920)

        
        self.saveRight = QtWidgets.QPushButton('Save Right File', self)
        self.saveRight.setStyleSheet("background-color: orange")
        self.saveRight.clicked.connect(lambda:self.save(self.rightTextBox.toPlainText()))
        self.saveRight.resize(130,30)
        self.saveRight.move(795, 950)

        
        self.refreshLeft = QtWidgets.QPushButton('Clear Left Text Area',self)
        self.refreshLeft.setStyleSheet("background-color: red")
        self.refreshLeft.clicked.connect(lambda:self.leftTextBox.setPlainText("HERE WILL BE YOUR INPUT IaC-File"))
        self.refreshLeft.resize(130,30)
        self.refreshLeft.move(5, 920)
        
        self.saveLeft = QtWidgets.QPushButton('Save Left File', self)
        self.saveLeft.setStyleSheet("background-color: orange")
        self.saveLeft.clicked.connect(lambda:self.save(self.leftTextBox.toPlainText()))
        self.saveLeft.resize(130,30)
        self.saveLeft.move(5, 950)  
        
        self.exitApp = QtWidgets.QPushButton('Exit', self)
        self.exitApp.setStyleSheet("background-color: red")
        self.exitApp.clicked.connect(app.exit)
        self.exitApp.resize(115,30)  
        self.exitApp.move(1580, 50) 
     
        self.secCheckRhs = QtWidgets.QPushButton('Security Check\nRight Hand\nOutput', self)
        self.secCheckRhs.setStyleSheet("background-color: darkgreen")
        self.secCheckRhs.clicked.connect(self.securityCheckLHS)
        self.secCheckRhs.resize(115,150)  
        self.secCheckRhs.move(1580, 80)

        # Create new action
        menuFileOpen = QAction(QIcon('/home/bob/present/proj/WorksArea/icons/open.png'), '&Open Document', self)        
        menuFileOpen.setShortcut('Ctrl+O')
        menuFileOpen.setStatusTip('Open document')
        menuFileOpen.triggered.connect(self.open)
        menuExit = QAction('&Exit Application', self)        
        menuExit.setStatusTip('Exit Application')
        menuExit.triggered.connect(app.exit)
        menuSaveLeft = QAction(QIcon('/home/bob/present/proj/WorksArea/icons/save.png'), 'Save Left Text', self)        
        menuSaveLeft.setShortcut('Ctrl+L')
        menuSaveLeft.setStatusTip('Save Left Documents')
        menuSaveLeft.triggered.connect(lambda:self.save(self.leftTextBox.toPlainText()))
        menuSaveRight = QAction(QIcon('/home/bob/present/proj/WorksArea/icons/save.png'), 'Save Right Text', self)        
        menuSaveRight.setShortcut('Ctrl+R')
        menuSaveRight.setStatusTip('Save Right Documents')
        menuSaveRight.triggered.connect(lambda:self.save(self.rightTextBox.toPlainText()))
             

        #set up file menu
        menuBar = self.menuBar()
        self.fileMenu = menuBar.addMenu('File')
        self.fileMenu.addAction(menuFileOpen) 
        self.fileMenu.addAction(menuExit)  
        self.fileMenu = menuBar.addMenu('Save')
        self.fileMenu.addAction(menuSaveLeft)           
        self.fileMenu.addAction(menuSaveRight) 
    
    
    #Open file      
    def open(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileNames(self, 'Open File', "", 'JSON Files (CloudFormation) (*.json)' , options=options )
        #QFileDialog.getSaveFileName()
        inputScript = (open(file[0])).read() 
        data = json.loads(inputScript)
        jsonout = data
        disp = json.dumps(jsonout, indent=4)
        self.displayText(self.leftTextBox, disp)
    
    #Save file with side arg passed in     
    def save(self, side):
        outputToFile = side
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self,"File Save","","*.txt;;*.tf;;*.json;;*.jinja;;*.sh;;*.py;;*.sav;;*.csv;;*", options=options)
        ext = _.replace("*", "")
        if fileName:
            with open(str(fileName)+str(ext), 'w') as outTextBox:
                outTextBox.write(str(outputToFile))
                #print(fileName,_)         
               
    #Process the left hand text area                 
    def processFile(self):
        home = str(Path.home())
        os.chdir(home)
        textboxValue = self.leftTextBox.toPlainText()
        name = self.popUp('pull', 'File Output Name')
        didItParse = check_output(["/home/bob/present/proj/WorksArea/iac2tf", "-s", textboxValue, "-o" ,name ],universal_newlines=True)
        print(type(didItParse))
        print(didItParse)
        if didItParse == "This failed to parse" :
            self.popUp('push', str("YOUR SCRIPT FAILED TO PARSE, PLEASE CHECK THE SYNTAX"),"")
        else:
            inputScript = (open(name+".tf")).read() 
            self.displayText(self.rightTextBox, inputScript)
            self.popUp('push', str("YOUR TF FILE IS SAVED TO :"), str(home+"/"+name+".tf") )
            
    #Security Check the left hand text area                 
    def securityCheckLHS(self):
        self.popUp('push', str("AFTER CLOSURE OF THIS POP UP, PLEASE AWAIT THE NEXT POP UP. THE PROCESSING WILL CONTINUE IN THE BACKGROUND AND TAKE UPTO 5mins"),"")
        textboxValue = self.rightTextBox.toPlainText()
        secCheck = check_output(["/home/bob/present/proj/WorksArea/iac2tf", "-Sec", textboxValue], universal_newlines=True)
        #print(os.environ)
        #print(secCheck)
        if secCheck == "n" :
            print(str("NO"))
            self.popUp('push', str("YOUR SCRIPT FAILED BASIC SECURITY CHECKS"), "")
        else:
            print(str("YES"))
            self.popUp('push', str("YOUR SCRIPT PASSED BASIC SECURITY CHECKS"), "")
            
    #Display text to either side, side to display and what is passed in
    def displayText(self, side, disp):
        side.setPlainText(disp)        
    
    #Pop up asking for input or show output
    def popUp(self, *args):
        title = "Iac 2 Tf"
        if args[0] == "push" :
            choice = QMessageBox.question(self, title , args[1]+" "+args[2], QMessageBox.Close)
        elif args[0] == "pull":
            text, okPressed = QInputDialog.getText(self, title ,args[1], QLineEdit.Normal, "")
            if okPressed and text != '':
                return(text)
        else :
            print("POP UP DIDNT HAPPEN :( CONTACT OWNER")

#Start :)       
app = QApplication(sys.argv)
win = iac2tf()
win.show()
splashScreen = Splash()
sys.exit(app.exec_())