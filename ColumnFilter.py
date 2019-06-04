# DebS 

from PyQt5 import QtCore, QtGui, QtWidgets
import Launcher

class ColumnFilter(object):

    def setupdata(self,data,info,obj):
        self.label.setText("Table: "+info)
         #get header list -- hardcoded
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(4)
        header = ["Column Name","Data Type", "Len","Filter Data"]
        self.tableWidget.setHorizontalHeaderLabels(header)
        rowcount = 0
        for row in data:
            itemcount = 0
            for item in row.values():
                self.tableWidget.setItem(rowcount,itemcount,QtWidgets.QTableWidgetItem(str(item)))
                self.tableWidget.item(rowcount,itemcount).setFlags(QtCore.Qt.ItemIsSelectable)
                itemcount = itemcount+1
            self.tableWidget.setItem(rowcount,itemcount,QtWidgets.QTableWidgetItem(""))
            #combobox at 4th row 
            self.comboBox = QtWidgets.QComboBox()
            comboitems = obj.UniqueValues(row["Column Name"],info)
            self.comboBox.addItem("-select-")
            self.comboBox.addItems(comboitems)
            self.tableWidget.setCellWidget(rowcount, itemcount, self.comboBox)
            self.tableWidget.item(rowcount,itemcount).setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsUserCheckable)
            self.dict[row["Column Name"]] = self.comboBox
            rowcount=rowcount+1 
        self.tableWidget.itemDoubleClicked.connect(obj.SelectQuery)

    def Text(self):
        pass
    
    def Display(self):
        pass

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(556, 505)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 201, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.toolButton_2 = QtWidgets.QToolButton(Form)
        self.toolButton_2.setGeometry(QtCore.QRect(430, 10, 51, 22))
        self.toolButton_2.setObjectName("toolButton_2")
        self.toolButton = QtWidgets.QToolButton(Form)
        self.toolButton.setGeometry(QtCore.QRect(490, 10, 51, 22))
        self.toolButton.setObjectName("toolButton")
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setGeometry(QtCore.QRect(10, 50, 531, 441))
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)

        self.dict = {}
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Table: None"))
        self.toolButton_2.setText(_translate("Form", "txt"))
        self.toolButton.setText(_translate("Form", "Data"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = ColumnFilter()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

