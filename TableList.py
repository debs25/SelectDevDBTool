# DebS 

from PyQt5 import QtCore, QtGui, QtWidgets
import Launcher

class TableList(object):

    def setupdata(self,data,info,obj):
        for item in data:
            self.listWidget.addItem(item)
         #connection 
        self.listWidget.itemDoubleClicked.connect(obj.TableItemClicked)
        self.textBrowser.setText("Found "+str(len(data))+". "+info)


    def setupUi(self, Columns):
        Columns.setObjectName("Columns")
        Columns.resize(282, 619)
        self.listWidget = QtWidgets.QListWidget(Columns)
        self.listWidget.setGeometry(QtCore.QRect(10, 70, 261, 541))
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setObjectName("listWidget")
        self.toolButton = QtWidgets.QToolButton(Columns)
        self.toolButton.setGeometry(QtCore.QRect(220, 40, 51, 22))
        self.toolButton.setObjectName("toolButton")
        self.toolButton_2 = QtWidgets.QToolButton(Columns)
        self.toolButton_2.setGeometry(QtCore.QRect(220, 10, 51, 22))
        self.toolButton_2.setObjectName("toolButton_2")
        self.textBrowser = QtWidgets.QTextBrowser(Columns)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 201, 51))
        self.textBrowser.setObjectName("textBrowser")

       


        self.retranslateUi(Columns)
        QtCore.QMetaObject.connectSlotsByName(Columns)

    def retranslateUi(self, Columns):
        _translate = QtCore.QCoreApplication.translate
        Columns.setWindowTitle(_translate("Columns", "Form"))
        self.toolButton.setText(_translate("Columns", "clear"))
        self.toolButton_2.setText(_translate("Columns", "txt"))
        self.textBrowser.setPlaceholderText(_translate("Columns", "Showing Result for : None"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Columns = QtWidgets.QWidget()
    ui = TableList()
    ui.setupUi(Columns)
    Columns.show()
    sys.exit(app.exec_())

