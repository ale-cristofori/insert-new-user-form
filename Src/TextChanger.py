import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from UiComponents import TextChanger_Ui


class TextChanger:
    """
    This is just a test for a simple interface (dialog), created for training.
    The user inserts some text in a text box and clicks on a button,
    the text is reported to a label on the same dialog window.
    """
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        text_dialog = QtWidgets.QDialog()
        self.text_changer = TextChanger_Ui.Ui_Dialog()
        self.text_changer.setupUi(text_dialog)
        self.text_changer.cancelPushButton.clicked.connect(self.change_text)
        text_dialog.show()
        sys.exit(app.exec_())

    def change_text(self):
        print("button clicked")
        line_text = self.text_changer.textLineEdit.text()
        label_text = self.text_changer.textLabel
        if line_text is not "":
            label_text.setText(line_text)
        else:
            try:
                no_text_alert = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, " ",
                                                      "Invalid Text Entry", QtWidgets.QMessageBox.Ok)
                no_text_alert.exec_()
            except Exception as e:
                print(e.args)

TextChanger()

