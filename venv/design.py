# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(472, 475)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnSendText = QtWidgets.QPushButton(self.centralwidget)
        self.btnSendText.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnSendText.setObjectName("btnSendText")
        self.horizontalLayout.addWidget(self.btnSendText)
        self.btnSendPicture = QtWidgets.QPushButton(self.centralwidget)
        self.btnSendPicture.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnSendPicture.setObjectName("btnSendPicture")
        self.horizontalLayout.addWidget(self.btnSendPicture)
        self.btnExit = QtWidgets.QPushButton(self.centralwidget)
        self.btnExit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnExit.setObjectName("btnExit")
        self.horizontalLayout.addWidget(self.btnExit)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 0, 1, 1)
        self.picView = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.picView.sizePolicy().hasHeightForWidth())
        self.picView.setSizePolicy(sizePolicy)
        self.picView.setMinimumSize(QtCore.QSize(100, 30))
        self.picView.setMaximumSize(QtCore.QSize(800, 600))
        self.picView.setBaseSize(QtCore.QSize(0, 50))
        self.picView.setFocusPolicy(QtCore.Qt.NoFocus)
        self.picView.setObjectName("picView")
        self.gridLayout.addWidget(self.picView, 0, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setMinimumSize(QtCore.QSize(50, 10))
        self.textEdit.setMaximumSize(QtCore.QSize(3000, 50))
        self.textEdit.setBaseSize(QtCore.QSize(0, 30))
        self.textEdit.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 2, 0, 1, 1)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy)
        self.textBrowser.setMinimumSize(QtCore.QSize(50, 10))
        self.textBrowser.setMaximumSize(QtCore.QSize(3000, 16777215))
        self.textBrowser.setBaseSize(QtCore.QSize(0, 30))
        self.textBrowser.setFocusPolicy(QtCore.Qt.NoFocus)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout.addWidget(self.textBrowser, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SergMessenger"))
        self.btnSendText.setText(_translate("MainWindow", "Send Text"))
        self.btnSendPicture.setText(_translate("MainWindow", "Send Picture"))
        self.btnExit.setText(_translate("MainWindow", "Exit"))

