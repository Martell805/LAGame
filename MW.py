# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MW.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(254, 147)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 251, 102))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.choose_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.choose_btn.setObjectName("choose_btn")
        self.gridLayout.addWidget(self.choose_btn, 1, 0, 1, 1)
        self.start_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.start_btn.setObjectName("start_btn")
        self.gridLayout.addWidget(self.start_btn, 2, 0, 1, 1)
        self.level_btn = QtWidgets.QLabel(self.gridLayoutWidget)
        self.level_btn.setObjectName("level_btn")
        self.gridLayout.addWidget(self.level_btn, 0, 0, 1, 1)
        self.shub_btn = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.shub_btn.setObjectName("shub_btn")
        self.gridLayout.addWidget(self.shub_btn, 3, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 254, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Game"))
        self.choose_btn.setText(_translate("MainWindow", "Выбрать"))
        self.start_btn.setText(_translate("MainWindow", "Запустить выбранный уровень"))
        self.level_btn.setText(_translate("MainWindow", "Выберите уровень:"))
        self.shub_btn.setText(_translate("MainWindow", "Запустить случайную игру"))
