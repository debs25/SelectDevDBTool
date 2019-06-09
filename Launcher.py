# DebS 

from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
import DBConn as Con 
import TableList as tableNameList
import ColumnFilter as columnFilter
import QResult as resTable



class MainUI(object):
    isConnected = False
    filterdata ={}
    def connectDB(self):
        if self.isConnected is False:
            self.con = Con.DB(self.editHost.text(),self.editPort.text(),self.editSID.text(),self.editUser.text(),self.editPassword.text())
            self.con.Connect()
        else:
            self.con.Close()
        self.isConnected = not self.isConnected
        editfields = [self.editHost,self.editPassword,self.editPort,self.editSID,self.editUser]
        if self.isConnected is True:
            self.btnConnect.setText("Disconnect")
            self.pushSearch.setEnabled(True)
            for edit in editfields:
                edit.setEnabled(False)
        else:
            self.pushSearch.setEnabled(False)
            self.btnConnect.setText("Connect")
            for edit in editfields:
                edit.setEnabled(True)
           
    def Search(self):
        if self.isConnected is True:
            searchstr = self.lineEditSearch.text()
            owner = self.editUser.text()
            
            resdiag = tableNameList.TableList()
            self.colui = QtWidgets.QWidget()
            resdiag.setupUi(self.colui)
            if self.checkBoxAsColumn.isChecked() is True:
                info="Showing all Tables with column "+searchstr
                resdiag.setupdata(self.con.TablesWithColumnName(owner,searchstr),info,self)
            else:
                info="Showing all Tables with containing "+searchstr
                resdiag.setupdata(self.con.TablesSearch(owner,searchstr),info,self)
                
            self.colui.show()
            self.colDlg.append(self.colui)
        
         
    def TableItemClicked(self,item):
        if self.isConnected is True:
            tablename = item.text()
            data = self.con.GetAllColumnsForTable(tablename)
            if len(data) >0:
                coldiag = columnFilter.ColumnFilter()
                self.descui = QtWidgets.QWidget()
                coldiag.setupUi(self.descui)
                coldiag.setupdata(data,tablename,self)
                self.descui.show()
                self.tblDlg.append(self.descui)
            
    def Text(self, text):
        print('text:column filter ')

    def Data(self, tablename, sqlcond, table):
        query = 'select * from '
        query+=tablename 
        query+= ' '
        rowCount = table.rowCount()
        condlist = []
        for row in range(rowCount):
            colname = table.item(row, 0).text()
            colvalue = table.cellWidget(row,3).currentText()
            coltype  = table.item(row, 1).text()
            if colvalue != "-select-":
                if "VARCHAR" not in coltype: 
                     condlist.append(" "+colname+" = "+colvalue+" ")
                else :
                    condlist.append(" "+colname+" = '"+colvalue+"' ")
               # print(colname+':'+colvalue)
        if len(condlist) > 0:
            query += " where"
        for i in range(len(condlist)):
            if i > 0:
                query+= sqlcond
            query += condlist[i]
            
        #query +=" ;" #lol does not take ; wasted  day :-)
        print(query)
        data = self.con.Query(query)
        print(data)
        diag = resTable.QResultDlg()
        self.resUI = QtWidgets.QWidget()
        diag.setupUi(self.resUI)
        # add data
        diag.setupdata(data,tablename,self)

        self.resUI.show()
        self.colResUI.append(self.resUI)

        
 

    def ShowRes(self, data):
        print(self,data)

    def SelectQuery(self,data):
        print(data)
        
    def UniqueValues(self, column,table)->[str]:
       # print(column)
        #print(table)
        return self.con.GetDistValue(column,table)

    def setupUi(self, DBGGUMain):
        DBGGUMain.setObjectName("DBGGUMain")
        DBGGUMain.resize(1306, 170)
        DBGGUMain.setFixedSize(1306, 170) 
        DBGGUMain.statusBar().setSizeGripEnabled(False) 
        self.colDlg = []
        self.tblDlg = []
        self.colResUI = []
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(DBGGUMain.sizePolicy().hasHeightForWidth())
        DBGGUMain.setSizePolicy(sizePolicy)
        DBGGUMain.setStatusTip("")
        self.centralwidget = QtWidgets.QWidget(DBGGUMain)
        self.centralwidget.setObjectName("centralwidget")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(0, 40, 1301, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.lineEditSearch = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditSearch.setGeometry(QtCore.QRect(23, 73, 251, 22))
        self.lineEditSearch.setObjectName("lineEditSearch")
        self.checkBoxAsColumn = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxAsColumn.setGeometry(QtCore.QRect(100, 100, 84, 20))
        self.checkBoxAsColumn.setObjectName("checkBoxAsColumn")
        self.checkBoxFullString = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxFullString.setGeometry(QtCore.QRect(23, 102, 63, 20))
        self.checkBoxFullString.setObjectName("checkBoxFullString")
        self.pushSearch = QtWidgets.QPushButton(self.centralwidget)
        self.pushSearch.setGeometry(QtCore.QRect(290, 70, 93, 28))
        self.pushSearch.setObjectName("pushSearch")
        self.checkTextFileption = QtWidgets.QCheckBox(self.centralwidget)
        self.checkTextFileption.setGeometry(QtCore.QRect(1140, 110, 131, 20))
        self.checkTextFileption.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkTextFileption.setObjectName("checkTextFileption")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(9, 10, 1036, 30))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)
        self.editHost = QtWidgets.QLineEdit(self.layoutWidget)
        self.editHost.setToolTipDuration(1)
        self.editHost.setObjectName("editHost")
        self.gridLayout.addWidget(self.editHost, 0, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 2, 1, 1)
        self.editPort = QtWidgets.QLineEdit(self.layoutWidget)
        self.editPort.setToolTipDuration(1)
        self.editPort.setObjectName("editPort")
        self.gridLayout.addWidget(self.editPort, 0, 3, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 4, 1, 1)
        self.editSID = QtWidgets.QLineEdit(self.layoutWidget)
        self.editSID.setToolTipDuration(1)
        self.editSID.setObjectName("editSID")
        self.gridLayout.addWidget(self.editSID, 0, 5, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 6, 1, 1)
        self.editUser = QtWidgets.QLineEdit(self.layoutWidget)
        self.editUser.setObjectName("editUser")
        self.gridLayout.addWidget(self.editUser, 0, 7, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 8, 1, 1)
        self.editPassword = QtWidgets.QLineEdit(self.layoutWidget)
        self.editPassword.setObjectName("editPassword")
        self.gridLayout.addWidget(self.editPassword, 0, 9, 1, 1)
        self.btnConnect = QtWidgets.QPushButton(self.layoutWidget)
        self.btnConnect.setObjectName("btnConnect")
        self.gridLayout.addWidget(self.btnConnect, 0, 10, 1, 1)
        self.pushButtonClipboard = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonClipboard.setGeometry(QtCore.QRect(1180, 10, 93, 28))
        self.pushButtonClipboard.setObjectName("pushButtonClipboard")
        DBGGUMain.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(DBGGUMain)
        self.statusbar.setObjectName("statusbar")
        DBGGUMain.setStatusBar(self.statusbar)

        #read a config file 

        self.editHost.setText("localhost")
        self.editPassword.setText("go")
        self.editPort.setText("1521")
        self.editSID.setText("O12CR201")
        self.editUser.setText("go")

        self.lineEditSearch.setText("MFGSKU")

        self.pushSearch.setEnabled(False)
        #connect to buttons 
        
        self.btnConnect.clicked.connect(lambda:self.connectDB())
        self.pushSearch.clicked.connect(lambda:self.Search())

        self.retranslateUi(DBGGUMain)
        QtCore.QMetaObject.connectSlotsByName(DBGGUMain)

    def retranslateUi(self, DBGGUMain):
        _translate = QtCore.QCoreApplication.translate
        DBGGUMain.setWindowTitle(_translate("DBGGUMain", "pyDB"))
        self.lineEditSearch.setPlaceholderText(_translate("DBGGUMain", "Search with Table / Column"))
        self.checkBoxAsColumn.setText(_translate("DBGGUMain", "Is Column"))
        self.checkBoxFullString.setText(_translate("DBGGUMain", "Partial"))
        self.pushSearch.setText(_translate("DBGGUMain", "Search"))
        self.checkTextFileption.setText(_translate("DBGGUMain", "Single Text File"))
        self.label_5.setText(_translate("DBGGUMain", "Host"))
        self.editHost.setToolTip(_translate("DBGGUMain", "Enter Host"))
        self.editHost.setPlaceholderText(_translate("DBGGUMain", "host / ip"))
        self.label_6.setText(_translate("DBGGUMain", "Port"))
        self.editPort.setToolTip(_translate("DBGGUMain", "Enter Port"))
        self.editPort.setPlaceholderText(_translate("DBGGUMain", "DB Port"))
        self.label.setText(_translate("DBGGUMain", "SID"))
        self.editSID.setToolTip(_translate("DBGGUMain", "Enter SID"))
        self.editSID.setPlaceholderText(_translate("DBGGUMain", "Enter SID"))
        self.label_2.setText(_translate("DBGGUMain", "User Name"))
        self.editUser.setToolTip(_translate("DBGGUMain", "Username"))
        self.editUser.setPlaceholderText(_translate("DBGGUMain", "User Name"))
        self.label_3.setText(_translate("DBGGUMain", "Password"))
        self.editPassword.setToolTip(_translate("DBGGUMain", "Password"))
        self.editPassword.setPlaceholderText(_translate("DBGGUMain", "Password"))
        self.btnConnect.setText(_translate("DBGGUMain", "Connect"))
        self.pushButtonClipboard.setText(_translate("DBGGUMain", "Clipboard"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DBGGUMain = QtWidgets.QMainWindow()
    ui = MainUI()
    ui.setupUi(DBGGUMain)
    DBGGUMain.show()
    sys.exit(app.exec_())

