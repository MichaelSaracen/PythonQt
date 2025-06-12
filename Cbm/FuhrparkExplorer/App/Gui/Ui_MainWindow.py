# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QMenuBar,
    QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.actionBrand = QAction(MainWindow)
        self.actionBrand.setObjectName(u"actionBrand")
        self.actionModel = QAction(MainWindow)
        self.actionModel.setObjectName(u"actionModel")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 33))
        self.menu_Menu = QMenu(self.menubar)
        self.menu_Menu.setObjectName(u"menu_Menu")
        self.menu_Bearbeiten = QMenu(self.menubar)
        self.menu_Bearbeiten.setObjectName(u"menu_Bearbeiten")
        self.menu_Einf_gen = QMenu(self.menu_Bearbeiten)
        self.menu_Einf_gen.setObjectName(u"menu_Einf_gen")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_Menu.menuAction())
        self.menubar.addAction(self.menu_Bearbeiten.menuAction())
        self.menu_Bearbeiten.addAction(self.menu_Einf_gen.menuAction())
        self.menu_Einf_gen.addAction(self.actionBrand)
        self.menu_Einf_gen.addAction(self.actionModel)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionBrand.setText(QCoreApplication.translate("MainWindow", u"Marke", None))
        self.actionModel.setText(QCoreApplication.translate("MainWindow", u"Modell", None))
        self.menu_Menu.setTitle(QCoreApplication.translate("MainWindow", u"&Datei", None))
        self.menu_Bearbeiten.setTitle(QCoreApplication.translate("MainWindow", u"&Bearbeiten", None))
        self.menu_Einf_gen.setTitle(QCoreApplication.translate("MainWindow", u"&Einf\u00fcgen", None))
    # retranslateUi

