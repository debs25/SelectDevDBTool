#Debs

from PyQt5 import QtCore, QtGui, QtWidgets

class QResultDlg(object):
    
    def setupdata(self,data,tname,obj,qstr,writer):
        #self.label.setText("Table: "+tname)
        self.tableWidget.setRowCount(len(data))
        
        if len(data) > 0:
            self.tableWidget.setColumnCount(len(data[0]))
            self.tableWidget.setHorizontalHeaderLabels(data[0].keys())
            
        rowcount = 0
        for row in data:
            itemcount = 0
            for item in row.values():
                self.tableWidget.setItem(rowcount,itemcount,QtWidgets.QTableWidgetItem(str(item)))
                self.tableWidget.item(rowcount,itemcount).setFlags(QtCore.Qt.ItemIsSelectable)
                itemcount = itemcount+1
            rowcount=rowcount+1 
                    
        self.toolButton.clicked.connect(lambda:writer.CBDict('Query: '+qstr, data))



    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1300, 330)
        Form.setFixedSize(1300, 330) 
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 70, 1271, 251))
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.textBrowser = QtWidgets.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(10, 10, 381, 51))
        self.textBrowser.setObjectName("textBrowser")
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(990, 20, 261, 24))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox_auto = QtWidgets.QCheckBox(self.widget)
        self.checkBox_auto.setAutoFillBackground(False)
        self.checkBox_auto.setChecked(True)
        self.checkBox_auto.setObjectName("checkBox_auto")
        self.gridLayout.addWidget(self.checkBox_auto, 0, 0, 1, 1)
        self.checkBox_all = QtWidgets.QCheckBox(self.widget)
        self.checkBox_all.setObjectName("checkBox_all")
        self.gridLayout.addWidget(self.checkBox_all, 0, 1, 1, 1)
        self.toolButton_delete = QtWidgets.QToolButton(self.widget)
        self.toolButton_delete.setObjectName("toolButton_delete")
        self.gridLayout.addWidget(self.toolButton_delete, 0, 2, 1, 1)
        self.toolButton = QtWidgets.QToolButton(self.widget)
        self.toolButton.setObjectName("toolButton")
        self.gridLayout.addWidget(self.toolButton, 0, 3, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.textBrowser.setPlaceholderText(_translate("Form", "Showing Result for : None"))
        self.checkBox_auto.setText(_translate("Form", "Auto text"))
        self.checkBox_all.setText(_translate("Form", "Select All"))
        self.toolButton_delete.setText(_translate("Form", "Delete"))
        self.toolButton.setText(_translate("Form", "txt"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = QResultDlg()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

