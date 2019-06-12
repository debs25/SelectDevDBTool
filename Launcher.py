# DebS 
#https://github.com/debs25/SelectDevDBTool

from PyQt5 import QtCore, QtGui, QtWidgets
from datetime import datetime
import DBConn as Con 
import TableList as tableNameList
import ColumnFilter as columnFilter
import QResult as resTable

class TextHandler:
    loggerFile = None
    def addFile(self):
        self.loggerFile = open("Data/DBDev_"+TextHandler.GetFileName()+".log","w") 
        self.loggerFile.write("This is Python Learning Project. Created by deb S. \n")
        self.loggerFile.write("Created at: "+TextHandler.GetTime())
        self.loggerFile.flush()

    @classmethod
    def GetFileName(cls)->str:
        curtime = f'{datetime.now():%Y%m%d%H%M%S}'
        return curtime

    @classmethod
    def GetTime(cls)->str:
        curtime = f'{datetime.now():%Y-%m-%d %H:%M:%S%z}'
        #curtime+='\n'
        return curtime

    def AddList(self, list):
        #self.loggerFile.write(TextHandler.GetTime()+'\n')
        self.loggerFile.writelines(map(lambda s:'\t'+ s + '\n', list))
        self.loggerFile.flush()

    def AddLine(self, line, underline):
        self.loggerFile.write('['+TextHandler.GetTime()+'] ')
        self.loggerFile.write(line+'\n')
        if underline :
            self.loggerFile.write('-'*(len(line)+20))
            self.loggerFile.write('\n')
        self.loggerFile.flush()
    
    def CBList(self,line,list):
        self.AddLine(line,True)
        self.AddList(list)

    def AddDict(self,dictlist):

        if len(dictlist) == 0:
            self.loggerFile.write("No Data found in output.\n")
        else:
            rowcount = 0
            namestr =""
            for header in dictlist[0].keys():
                namestr+='{:20s}'.format('\t'+header+' ')
            self.loggerFile.write(namestr+'\n')
            self.loggerFile.write('-' * len(namestr)+'\n')
            self.loggerFile.flush()
            table =[]
            for row in dictlist:
                itemcount = 0
                rowstr =""
                for item in row.values():
                    rowstr +='{:20s}'.format( str(item)+' ')
                    itemcount = itemcount+1
                table.append(rowstr)
                rowcount=rowcount+1 
            self.loggerFile.writelines(map(lambda s:'\t'+ s + '\n', table))      
        self.loggerFile.flush()

    def CBDict(self,line,dict):
        self.AddLine(line,True)
        self.AddDict(dict)

    def DontSave(self):
        pass

    def Close(self):
        if not self.loggerFile.closed():
            self.loggerFile.close()


class MainUI(object):
    writer = None
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
            self.writer.AddLine('Connected to '+self.con.Version(),False)
        else:
            self.pushSearch.setEnabled(False)
            self.btnConnect.setText("Connect")
            for edit in editfields:
                edit.setEnabled(True)
            self.writer.AddLine('DB Disconnected',False)

    def Search(self):
        if self.isConnected is True:
            searchstr = self.lineEditSearch.text()
            owner = self.editUser.text()
            
            
            if self.checkBoxAsColumn.isChecked() is True:
                resdiag = tableNameList.TableList()
                self.colui = QtWidgets.QWidget()
                resdiag.setupUi(self.colui)
                info="Showing all Tables with column Name: "+searchstr
                resdiag.setupdata(self.con.TablesWithColumnName(owner,searchstr),info,self,self.writer)
                self.colui.setWindowTitle(searchstr+':Containing Tables')
                self.colui.show()
                self.colDlg.append(self.colui)
            elif self.checkBoxFullString.isChecked() is True:
                tablelist = self.con.TablesSearch(owner,'')
                tData = []
                query = ''
                for table in tablelist:
                    columns = self.con.GetAllColumns(table)
                    for column in columns:
                        query = 'select * from '+ table+ ' where upper('+column['COLUMN_NAME']+')  like  upper(\'%'+searchstr+'%\') '
                        data = self.con.Query(query)
                        if len(data) > 0:
                            tDict = {}
                            tDict["Table Name"]=table
                            tDict["Column"]=column['COLUMN_NAME']
                            tDict["Records Found"]=len(data)
                            tData.append(tDict)

                diag = resTable.QResultDlg()
                self.resUI = QtWidgets.QWidget()
                diag.setupUi(self.resUI)
                # add data
                diag.setupdata(tData,'',self,query,self.writer)
                self.resUI.setWindowTitle('Tables with data:'+searchstr)
                self.resUI.show()
                self.colResUI.append(self.resUI)
                                
            else:
                resdiag = tableNameList.TableList()
                self.colui = QtWidgets.QWidget()
                resdiag.setupUi(self.colui)
                info="Showing all Tables with containing : "+searchstr
                resdiag.setupdata(self.con.TablesSearch(owner,searchstr),info,self,self.writer)
                self.colui.setWindowTitle(searchstr+':Tables Search')
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
                coldiag.setupdata(data,tablename,self,self.writer)
                self.descui.setWindowTitle(tablename+':Desc')
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

        if len(condlist) > 0:
            query += " where"
        for i in range(len(condlist)):
            if i > 0:
                query+= sqlcond
            query += condlist[i]
            
        #query +=" ;" #lol does not take ; wasted  day :-)
        data = self.con.Query(query)
        diag = resTable.QResultDlg()
        self.resUI = QtWidgets.QWidget()
        diag.setupUi(self.resUI)
        # add data
        diag.setupdata(data,tablename,self,query,self.writer)
        self.resUI.setWindowTitle(tablename+':Data')
        self.resUI.show()
        self.colResUI.append(self.resUI)



        
    def UniqueValues(self, column,table)->[str]:
        return self.con.GetDistValue(column,table)

    def setupUi(self, DBGGUMain):
        DBGGUMain.setObjectName("DBGGUMain")
        DBGGUMain.resize(1306, 170)
        DBGGUMain.setFixedSize(1306, 170) 
        DBGGUMain.statusBar().setSizeGripEnabled(False) 
        self.colDlg = []
        self.tblDlg = []
        self.colResUI = []
        self.writer = TextHandler()
        self.writer.addFile()
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

        #read a config file maybe 

        self.editHost.setText("localhost")
        self.editPassword.setText("debs")
        self.editPort.setText("1521")
        self.editSID.setText("O12CR201")
        self.editUser.setText("debs")
        self.lineEditSearch.setText("job")


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
        self.checkBoxAsColumn.setText(_translate("DBGGUMain", "Column"))
        self.checkBoxFullString.setText(_translate("DBGGUMain", "Data"))
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

