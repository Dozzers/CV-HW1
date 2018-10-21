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

        self.inputImageDirectory = QFileDialog.getOpenFileName()[0] #find file directory
        self.inputImage = cv2.imread(self.inputImageDirectory, 1) #read the image
        
        self.inputHist = self.calcHistogram(self.inputImage) #calculate and return RGB histogram
        input_canvas = self.plotHistogram(self.inputHist) #plot the histogram and return it
        

        inputLabel = QLabel(self)   #the only way I could find to display image in PyQt5 easily
        pixmap = QPixmap(self.inputImageDirectory)
        inputLabel.setPixmap(pixmap)
        
        inputBoxV = QVBoxLayout()
        inputBoxV.addWidget(inputLabel) #add image to the VBox
        inputBoxV.addWidget(input_canvas) #add plot to the VBox
        self.inputBox.setLayout(inputBoxV) # add to the inputBox which is declared in initUI
    def openTargetImage(self):
        #SAME CODE ACTUALLY WITH THE openInputImage
        self.targetImageDirectory = QFileDialog.getOpenFileName()[0]
        self.targetImage = cv2.imread(self.targetImageDirectory, 1)
        
        self.targetHist = self.calcHistogram(self.targetImage)
        target_canvas = self.plotHistogram(self.targetHist)
        
        targetLabel = QLabel(self)
        pixmap = QPixmap(self.targetImageDirectory)
        targetLabel.setPixmap(pixmap)
        
        targetBoxV = QVBoxLayout()
        targetBoxV.addWidget(targetLabel)
        targetBoxV.addWidget(target_canvas)
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
        
    def calcLUT(self, ICDF, TCDF): #takes inputCDF and targetCDF as parameters
        LUT = np.zeros((3,256))
        
        for x in range(0,3): #iterate for all 3 channels
            for gi in range(256): #iterate for all intensity index of input image
                gj=0
                #if targetCDF is smaller than inputCDF increment the target index until not
                while TCDF[x][gj]<ICDF[x][gi] and gj<255: 
                    gj = gj+1
                
                #and assign the gj index to the LUT table corresponding to gi index
                LUT[x][gi]=gj
        #return look-up table
        return LUT

    def calcCDF(self, I):
        height, width, channels = I.shape
        totalSize = (width*height) #total pixel number of the image
        
        histI = self.calcHistogram(I) #calculate the histogram image in order to use this function modular
        
        blueHist = np.zeros((1,256))
        blueHist[0][:] = histI[0]
        
        greenHist = np.zeros((1,256))
        greenHist[0][:] = histI[1]
        
        redHist = np.zeros((1,256))
        redHist[0][:] = histI[2]
        
        blueCDF = np.zeros((1,256))
        greenCDF = np.zeros((1,256))
        redCDF = np.zeros((1,256))
        CDF = np.zeros((3,256))
        
        #all the intensity values summed up with divided by total pixel number
        for i in range(0,256):
            if i == 0: #if the index is 0 nothing to sum with before
                blueCDF[0][i] = blueHist[0][i]/totalSize
                greenCDF[0][i] = greenHist[0][i]/totalSize
                redCDF[0][i] = redHist[0][i]/totalSize
            else: #sum with last CDF index value and at the index value divided by total pixel number 
                blueCDF[0][i] = blueCDF[0][i-1]+(blueHist[0][i]/totalSize)
                greenCDF[0][i] = greenCDF[0][i-1]+(greenHist[0][i]/totalSize)
                redCDF[0][i] = redCDF[0][i-1]+(redHist[0][i]/totalSize)
        
      
        CDF[0][:] =blueCDF[0][:]
        CDF[1][:] =greenCDF[0][:]
        CDF[2][:] =redCDF[0][:]
        
        #three channel CDF obtained and returned  
        return CDF
        
        

    def calcHistogram(self, I):
        b,g,r = cv2.split(I) #split the rgb channels of image
        height, width, channels = I.shape #find the height and width of image
        
        channelHist = np.zeros((3,256)) #create an empty array
        
        for i in range(0,height): #to navigate between all pixels go all columns
            for j in range(0, width): # and all rows
                #increment the histogram value between (0-255) corresponding color channel value of that pixel
                channelHist[0][b[i][j]]+=1  #blue
                channelHist[1][g[i][j]]+=1  #green
                channelHist[2][r[i][j]]+=1  #red
            
        return channelHist
    
    def plotHistogram(self, hist):
        canvas = FigureCanvas(Figure(figsize=(5, 3))) #canvas created to return drawable image by PyQt
        
        ax = canvas.figure.subplots(3, sharex=True, sharey=True) #Divided to the three subplot

        blueHist = np.zeros((1,256)) #To iterate all intensity values this change has been made
        blueHist[0][:] = hist[0]
        
        greenHist = np.zeros((1,256)) #To iterate all intensity values this change has been made
        greenHist[0][:] = hist[1]
        
        redHist = np.zeros((1,256)) #To iterate all intensity values this change has been made
        redHist[0][:] = hist[2]
        
        #Intensity values plotted as bar with the corresponding channel color
        ax[0].bar(range(0,256), redHist[0,:], color='red')
        ax[1].bar(range(0,256), greenHist[0,:], color='green') 
        ax[2].bar(range(0,256), blueHist[0,:], color='blue')
        
        return canvas #canvas returned

#It starts the qtApp
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

