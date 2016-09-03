'''
Created on Aug 27, 2016

@author: root
'''

from PySide.QtGui import QMainWindow, QWidget, QHBoxLayout, QFrame, QVBoxLayout,\
    QPushButton, QCheckBox, QFileDialog, QGroupBox, QGridLayout
from PySide import QtWebKit, QtCore
from src.data_read import *
import pygmaps
import utm


class window(QMainWindow):
    def __init__(self):
        super(window, self).__init__()

        self.resize(1024,720)
        self.centralWidget = QWidget(self)
        self.setWindowTitle('Plotting Points (Google Maps)')
        
        self.layout = QHBoxLayout(self.centralWidget)
        
        self.frame = QFrame(self.centralWidget)
        self.frameLayout = QVBoxLayout(self.frame)
        
        self.web = QtWebKit.QWebView()
        
        group_left = QGroupBox('Data Preparation')
        groupLeft_layout = QGridLayout()
        
        self.openButton = QPushButton("Open file")
        self.openButton.clicked.connect(self.openfile)
        
        self.optUTM = QCheckBox('UTM Data')
        
        
        groupLeft_layout.addWidget(self.optUTM,0,0)
        groupLeft_layout.addWidget(self.openButton,1,0)
        
        groupLeft_layout.setRowStretch(2,1)
        group_left.setLayout(groupLeft_layout)
        
        self.frameLayout.addWidget(self.web)
        self.layout.addWidget(group_left)
        self.layout.addWidget(self.frame)
        self.layout.setStretch(1,1)
        self.setCentralWidget(self.centralWidget)
        
        url = 'http://maps.google.com'
        
        self.showMap(url)   
        
    def openfile(self):
        
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '/home')
        
        if fname:
            f = open(fname)
            
            with f:
                data = f.read().splitlines()
                self.plottomap(data)
        else:
            print 'a'
    
    
    def dataConst(self,dataline):
    
        coord_list = []
    
        for data in dataline:
            catch_data = map(float, data.strip().split())
            coord_list.append(tuple(catch_data))
        
        if self.optUTM.isChecked() == True:
            coord_list = self.UTMtoLatLon(coord_list)
        
        return coord_list
        
        
    def plottomap(self,data):
        
        
        coords_data = self.dataConst(data)
        
        
        mymap = pygmaps.maps(coords_data[0][0], coords_data[0][1], 6)
        
        
        for i, point in enumerate(coords_data):
            mymap.addpoint(point[0], point[1], "#FF0000")
        
        mymap.addpath(coords_data, '#0000FF')
        
        mymap.draw('./mymap.draw.html')
        url = './mymap.draw.html'
        
        self.showMap(url)
    
    def UTMtoLatLon(self, utmData):
        utm_list = utmData
        latlon_list = []
        for i in range(len(utm_list)-1):
        
            (lat, lon) = utm.to_latlon(utm_list[i][0], utm_list[i][1], 52, 'M')
            
            latlon_list.append((lat,lon))
        
        return latlon_list
    
     
    def showMap(self, url):
        
        self.web.load(QtCore.QUrl(url))
        
        self.web.show()