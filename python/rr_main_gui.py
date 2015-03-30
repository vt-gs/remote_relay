#!/usr/bin/env python

from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt
import numpy as np

import sys
from Relay_QCheckBox import *

class MainWindow(QtGui.QWidget):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(775, 250)
        self.setWindowTitle('Remote Relay Control')
        self.setContentsMargins(0,0,0,0)
        self.spdt_cb = []   #list to hold spdt relay check boxes
        self.dpdt_cb = []   #list to hold dpdt relay check boxes

        self.initUI()
        self.darken()
        self.setFocus()

    def initUI(self):
        self.initFrames()
        self.initSPDTCheckBoxes()
        self.initDPDTCheckBoxes()
        self.initADC()
        self.initButtons()
        

    def initADC(self):
        field_name  = [ 'ADC1:', 'ADC2:', 'ADC3:', 'ADC4:', 'ADC5:', 'ADC6:', 'ADC7:', 'ADC8:']
        field_value = [ '0.00V', '0.00V', '0.00V', '0.00V', '0.00V', '0.00V', '0.00V', '0.00V' ]

        self.adc_field_labels_qlabels = []        #List containing Static field Qlabels, do not change
        self.adc_field_values_qlabels = []       #List containing the value of the field, updated per packet

        vbox = QtGui.QVBoxLayout()

        for i in range(len(field_name)):
            hbox = QtGui.QHBoxLayout()
            self.adc_field_labels_qlabels.append(QtGui.QLabel(field_name[i]))
            self.adc_field_labels_qlabels[i].setAlignment(QtCore.Qt.AlignLeft)
            self.adc_field_values_qlabels.append(QtGui.QLabel(field_value[i]))
            self.adc_field_values_qlabels[i].setAlignment(QtCore.Qt.AlignLeft)
            hbox.addWidget(self.adc_field_labels_qlabels[i])
            hbox.addWidget(self.adc_field_values_qlabels[i])
            vbox.addLayout(hbox)


        self.adc_fr.setLayout(vbox)

    def initADC_old(self):
        field_name  = [ 'ADC1:', 'ADC2:', 'ADC3:', 'ADC4:', 'ADC5:', 'ADC6:', 'ADC7:', 'ADC8:']
        field_value = [ '0.00V', '0.00V', '0.00V', '0.00V', '0.00V', '0.00V', '0.00V', '0.00V' ]

        self.adc_field_labels_qlabels = []        #List containing Static field Qlabels, do not change
        self.adc_field_values_qlabels = []       #List containing the value of the field, updated per packet

        hbox = QtGui.QHBoxLayout()

        for i in range(len(field_name)):
            self.adc_field_labels_qlabels.append(QtGui.QLabel(field_name[i]))
            self.adc_field_labels_qlabels[i].setAlignment(QtCore.Qt.AlignLeft)
            self.adc_field_values_qlabels.append(QtGui.QLabel(field_value[i]))
            self.adc_field_values_qlabels[i].setAlignment(QtCore.Qt.AlignLeft)
            hbox.addWidget(self.adc_field_labels_qlabels[i])
            hbox.addWidget(self.adc_field_values_qlabels[i])

        self.adc_fr.setLayout(hbox)


    def initButtons(self):
        ipAddrTextBox = QtGui.QLineEdit()
        ipAddrTextBox.setText("192.168.42.11")
        ipAddrTextBox.setEchoMode(QtGui.QLineEdit.Normal)
        ipAddrTextBox.setStyleSheet("QLabel {font-size: 16px;\
                                        font-weight:bold; \
                                        text-decoration:underline; \
                                        background-color: rgb(255,255,255); \
                                        color:rgb(0,0,0) ; }")
        ipAddrTextBox.setMaxLength(15)

        updateButton = QtGui.QPushButton("Update")
        resetButton = QtGui.QPushButton("Reset")
        readRelayButton = QtGui.QPushButton("Read Relay")
        readVoltButton = QtGui.QPushButton("Read ADCs")
        readStatusButton = QtGui.QPushButton("Read Status")
        connectButton = QtGui.QPushButton("Connect")

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(updateButton)
        hbox1.addWidget(resetButton)
        hbox1.addWidget(readRelayButton)
        hbox1.addWidget(readVoltButton)
        hbox1.addWidget(readStatusButton)
        hbox1.addWidget(connectButton)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(ipAddrTextBox)
        vbox.addLayout(hbox1)

        self.button_fr.setLayout(vbox)
        

    def initSPDTCheckBoxes(self):
        hbox1 = QtGui.QHBoxLayout()
        for i in range(8):
            cb = Relay_QCheckBox(i+1, 'SPDT'+str(i+1), 0)
            hbox1.addWidget(cb)
        hbox2 = QtGui.QHBoxLayout()
        for i in range(8):
            cb = Relay_QCheckBox(i+1+8, 'SPDT'+str(i+1+8), 0)
            hbox2.addWidget(cb)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.spdt_fr.setLayout(vbox)
    
    def initDPDTCheckBoxes(self):
        hbox1 = QtGui.QHBoxLayout()
        for i in range(8):
            cb = Relay_QCheckBox(i+1, 'DPDT'+str(i+1), 1)
            hbox1.addWidget(cb)
        hbox2 = QtGui.QHBoxLayout()
        for i in range(8):
            cb = Relay_QCheckBox(i+1+8, 'DPDT'+str(i+1+8), 1)
            hbox2.addWidget(cb)
        
        vbox = QtGui.QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        

        self.dpdt_fr.setLayout(vbox)

    def initFrames(self):
        self.spdt_fr = QtGui.QFrame(self)
        self.spdt_fr.setFrameShape(QtGui.QFrame.StyledPanel)
        #self.top.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        #self.top.setLineWidth(3)

        self.dpdt_fr = QtGui.QFrame(self)
        self.dpdt_fr.setFrameShape(QtGui.QFrame.StyledPanel)

        self.adc_fr = QtGui.QFrame(self)
        self.adc_fr.setFrameShape(QtGui.QFrame.StyledPanel)

        self.button_fr = QtGui.QFrame(self)
        self.button_fr.setFrameShape(QtGui.QFrame.StyledPanel)

        

        vbox = QtGui.QVBoxLayout()
        hbox = QtGui.QHBoxLayout()

        vbox.addWidget(self.spdt_fr)
        vbox.addWidget(self.dpdt_fr)
        #vbox.addWidget(self.adc_fr)
        vbox.addWidget(self.button_fr)
        
        hbox.addLayout(vbox)
        hbox.addWidget(self.adc_fr)

        self.setLayout(hbox)



    def initFrames_old(self):
        self.spdt_fr = QtGui.QFrame(self)
        self.spdt_fr.setFrameShape(QtGui.QFrame.StyledPanel)
        #self.top.setFrameStyle(QtGui.QFrame.Panel | QtGui.QFrame.Raised)
        #self.top.setLineWidth(3)

        self.dpdt_fr = QtGui.QFrame(self)
        self.dpdt_fr.setFrameShape(QtGui.QFrame.StyledPanel)

        self.adc_fr = QtGui.QFrame(self)
        self.adc_fr.setFrameShape(QtGui.QFrame.StyledPanel)

        self.button_fr = QtGui.QFrame(self)
        self.button_fr.setFrameShape(QtGui.QFrame.StyledPanel)

        

        vbox = QtGui.QVBoxLayout()
        #hbox = QtGui.QHBoxLayout()

        vbox.addWidget(self.spdt_fr)
        vbox.addWidget(self.dpdt_fr)
        vbox.addWidget(self.adc_fr)
        vbox.addWidget(self.button_fr)
        
        #hbox.addLayout(vbox)
        #hbox.addWidget(self.right)

        self.setLayout(vbox)

    

    def darken(self):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background,QtCore.Qt.black)
        palette.setColor(QtGui.QPalette.WindowText,QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Text,QtCore.Qt.white)
        self.setPalette(palette)







class MainWindow_old(QtGui.QWidget):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.resize(600, 500)
        self.setWindowTitle('Remote Relay Control')
        self.initUI()
        self.darken()

    def initUI(self):
        self.initFrames()
        self.initCheckBoxes()
        
        

    def initCheckBoxes(self):
        vbox1 = QtGui.QVBoxLayout()
        spdt_label = QtGui.QLabel('SPDT')
        spdt_label.setStyleSheet("QLabel {  font-size: 16px;\
                                            font-weight:bold; \
                                            text-decoration:underline; \
                                            background-color: rgb(0,0,0); \
                                            color:rgb(255,255,255) ; }")
        spdt_label.setAlignment(QtCore.Qt.AlignCenter)
        vbox1.addWidget(spdt_label)
        for i in range(16):
            cb = Relay_QCheckBox(i+1, 'SPDT'+str(i+1), 0)
            vbox1.addWidget(cb)

        vbox2 = QtGui.QVBoxLayout()
        dpdt_label = QtGui.QLabel('DPDT')
        dpdt_label.setStyleSheet("QLabel {  font-size: 16px;\
                                            font-weight:bold; \
                                            text-decoration:underline; \
                                            background-color: rgb(0,0,0); \
                                            color:rgb(255,255,255) ; }")
        dpdt_label.setAlignment(QtCore.Qt.AlignCenter)
        vbox2.addWidget(dpdt_label)
        for i in range(16):
            cb = Relay_QCheckBox(i+1, 'DPDT'+str(i+1), 1)
            vbox2.addWidget(cb)

        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        self.left.setLayout(hbox)

    def initFrames(self):
        self.left = QtGui.QFrame()
        self.left.setFrameShape(QtGui.QFrame.StyledPanel)
        #self.left.setFixedSize(100, 100)
        self.mid = QtGui.QFrame()
        self.mid.setFrameShape(QtGui.QFrame.StyledPanel)
        self.right = QtGui.QFrame()
        self.right.setFrameShape(QtGui.QFrame.StyledPanel)
        self.bottom = QtGui.QFrame()
        self.bottom.setFrameShape(QtGui.QFrame.StyledPanel)
        #self.right.setFixedSize(100,100)
        #self.main_tab.grid.addWidget(self.left ,0,0)
        #self.main_tab.grid.addWidget(self.right,0,1)
        hbox = QtGui.QHBoxLayout()
        vbox = QtGui.QVBoxLayout()
        #hbox.addStretch(1)
        hbox.addWidget(self.left)
        hbox.addWidget(self.mid)
        hbox.addWidget(self.right)

        vbox.addLayout(hbox)
        vbox.addWidget(self.bottom)

        self.setLayout(vbox)

    

    def darken(self):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background,QtCore.Qt.black)
        palette.setColor(QtGui.QPalette.WindowText,QtCore.Qt.white)
        palette.setColor(QtGui.QPalette.Text,QtCore.Qt.white)
        self.setPalette(palette)
