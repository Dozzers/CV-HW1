import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QHBoxLayout, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QGroupBox, QAction, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import cv2



class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.title = 'Histogram Equalization'
        self.left = 10
        self.top = 10
        self.width = 1280 #Default width
        self.height = 720 #Default hheight
        self.inputImageDirectory = ''
        self.inputImage = 0
        self.targetImageDirectory = ''
        self.targetImage = 0
        self.initUI() #Initialize the UI

    def openInputImage(self):
        # This function is called when the user clicks File->Input Image.
        return NotImplementedError

        self.inputImageDirectory = QFileDialog.getOpenFileName()[0] #find file directory
        self.inputImage = cv2.imread(self.inputImageDirectory, 1) #read the image
        inputLabel = QLabel(self)   #the only way I could find to display image in PyQt5 easily
        pixmap = QPixmap(self.inputImageDirectory)
        inputLabel.setPixmap(pixmap)
        inputBoxV = QVBoxLayout()
        inputBoxV.addWidget(inputLabel) #add image to the VBox
        self.inputBox.setLayout(inputBoxV) # add to the inputBox which is declared in initUI
    def openTargetImage(self):
        # This function is called when the user clicks File->Target Image.
        self.targetImageDirectory = QFileDialog.getOpenFileName()[0]
        self.targetImage = cv2.imread(self.targetImageDirectory, 1)

        targetLabel = QLabel(self)
        pixmap = QPixmap(self.targetImageDirectory)
        targetLabel.setPixmap(pixmap)
        
        targetBoxV = QVBoxLayout()
        targetBoxV.addWidget(targetLabel)
        self.targetBox.setLayout(targetBoxV)
    def initUI(self):
        
        
        self.setGeometry(self.left,self.top,self.width,self.height)
        self.setWindowTitle(self.title)
        
        actionOpenInput = QAction(" Open Input", self)
        actionOpenInput.setStatusTip('Chose an image from files for input')
        actionOpenInput.triggered.connect(self.openInputImage)
        
        actionOpenTarget = QAction(" Open Target", self)
        actionOpenTarget.setStatusTip('Chose an image from files for target')
        actionOpenTarget.triggered.connect(self.openTargetImage)
        
        actionExit = QAction(" Exit", self)
        actionExit.setStatusTip('Close the application')
        actionExit.triggered.connect(self.close)
        
        self.statusBar()
        
        
        mainMenu = self.menuBar() #Top menu bar for file operations
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(actionOpenInput)
        fileMenu.addAction(actionOpenTarget)
        fileMenu.addAction(actionExit)
        
        buttonEqualizeHistogram = QAction('Equalize Histogram', self)
        buttonEqualizeHistogram.setToolTip('runs the function')
        buttonEqualizeHistogram.triggered.connect(self.histogramButtonClicked)
        
        toolbar = self.addToolBar('Tools') #Toolbar for equalize histogram button
        toolbar.addAction(buttonEqualizeHistogram)
        
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.mainB  = QHBoxLayout()
        
        self.inputBox = QGroupBox("Input") #Groupboxes to display image and histogram

        self.targetBox = QGroupBox("Target")

        self.resultBox = QGroupBox("Result")

        
        self.mainB.addWidget(self.inputBox)
        self.mainB.addWidget(self.targetBox)
        self.mainB.addWidget(self.resultBox)
        self.centralWidget.setLayout(self.mainB)
        
        self.show()

    def histogramButtonClicked(self):
        if not self.inputLoaded and not self.targetLoaded:
            # Error: "First load input and target images" in MessageBox
            return NotImplementedError
        if not self.inputLoaded:
            # Error: "Load input image" in MessageBox
            return NotImplementedError
        elif not self.targetLoaded:
            # Error: "Load target image" in MessageBox
            return NotImplementedError

    def calcHistogram(self, I):
        # Calculate histogram
        return NotImplementedError

class PlotCanvas(FigureCanvas):
    def __init__(self, hist, parent=None, width=5, height=4, dpi=100):
        return NotImplementedError
        # Init Canvas
        self.plotHistogram(hist)

    def plotHistogram(self, hist):
        return NotImplementedError
        # Plot histogram

        self.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())