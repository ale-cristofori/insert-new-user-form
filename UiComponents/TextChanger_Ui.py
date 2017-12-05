# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\WinPython-64bit-3.4.4.5Qt5\QtUiFiles\Test_1.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(350, 150)
        Dialog.setMaximumSize(QtCore.QSize(350, 150))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.textLineEdit = QtWidgets.QLineEdit(Dialog)
        self.textLineEdit.setInputMask("")
        self.textLineEdit.setText("")
        self.textLineEdit.setObjectName("textLineEdit")
        self.verticalLayout.addWidget(self.textLineEdit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.boldRadioButton = QtWidgets.QRadioButton(Dialog)
        self.boldRadioButton.setObjectName("boldRadioButton")
        self.horizontalLayout_2.addWidget(self.boldRadioButton)
        self.italicRadioButton = QtWidgets.QRadioButton(Dialog)
        self.italicRadioButton.setObjectName("italicRadioButton")
        self.horizontalLayout_2.addWidget(self.italicRadioButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.cancelPushButton = QtWidgets.QPushButton(Dialog)
        self.cancelPushButton.setObjectName("cancelPushButton")
        self.horizontalLayout.addWidget(self.cancelPushButton)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 1, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.textLabel = QtWidgets.QLabel(Dialog)
        self.textLabel.setObjectName("textLabel")
        self.horizontalLayout_3.addWidget(self.textLabel)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 1, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Text Changer", "Text Changer"))
        self.textLineEdit.setPlaceholderText(_translate("Dialog", "insert text here"))
        self.boldRadioButton.setText(_translate("Dialog", "Bold"))
        self.italicRadioButton.setText(_translate("Dialog", "Italic"))
        self.cancelPushButton.setText(_translate("Dialog", "Change"))
        self.textLabel.setText(_translate("Dialog", "Text should appear here"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

