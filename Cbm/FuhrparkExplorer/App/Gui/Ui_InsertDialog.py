# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'InsertDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

class Ui_InsertDialog(object):
    def setupUi(self, InsertDialog):
        if not InsertDialog.objectName():
            InsertDialog.setObjectName(u"InsertDialog")
        InsertDialog.resize(351, 159)
        self.verticalLayout = QVBoxLayout(InsertDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.labelTitle = QLabel(InsertDialog)
        self.labelTitle.setObjectName(u"labelTitle")

        self.verticalLayout.addWidget(self.labelTitle)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.labelName = QLabel(InsertDialog)
        self.labelName.setObjectName(u"labelName")

        self.horizontalLayout.addWidget(self.labelName)

        self.lineEdit = QLineEdit(InsertDialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.buttonSave = QPushButton(InsertDialog)
        self.buttonSave.setObjectName(u"buttonSave")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonSave.sizePolicy().hasHeightForWidth())
        self.buttonSave.setSizePolicy(sizePolicy)
        self.buttonSave.setMinimumSize(QSize(0, 34))
        self.buttonSave.setMaximumSize(QSize(16777215, 34))

        self.horizontalLayout_2.addWidget(self.buttonSave)

        self.buttonQuit = QPushButton(InsertDialog)
        self.buttonQuit.setObjectName(u"buttonQuit")
        self.buttonQuit.setMinimumSize(QSize(0, 34))
        self.buttonQuit.setMaximumSize(QSize(16777215, 34))

        self.horizontalLayout_2.addWidget(self.buttonQuit)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalLayout.setStretch(1, 1)

        self.retranslateUi(InsertDialog)
        self.buttonQuit.clicked.connect(InsertDialog.close)

        QMetaObject.connectSlotsByName(InsertDialog)
    # setupUi

    def retranslateUi(self, InsertDialog):
        InsertDialog.setWindowTitle(QCoreApplication.translate("InsertDialog", u"Form", None))
        self.labelTitle.setText(QCoreApplication.translate("InsertDialog", u"Title", None))
        self.labelName.setText(QCoreApplication.translate("InsertDialog", u"Name:", None))
        self.buttonSave.setText(QCoreApplication.translate("InsertDialog", u"Speichern", None))
        self.buttonQuit.setText(QCoreApplication.translate("InsertDialog", u"Abbrechen", None))
    # retranslateUi

