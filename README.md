## SelectDevDBTool - Simple DB Tool with oracle (cx_oracle) & pyQt5
making simple db application for windows as python ongoing learning 
windoes based - super simple tool for developers. Written in python 3. , cx_oracle & pyqt5
### Usages 
#### 1. Find Database Tables who's name is like '%TABLE_NAME%' (uncheck 'Data', uncheck 'Column')
#### 2. Find All Database Tables which has columne named 'COLUMN_NAME' (uncheck 'Data', check 'Column')
#### 3. Search any value through out the tables (check 'Data', uncheck 'Column')
#### 4. Get Table Columns , Data Type, Unique Data inside Combobox , select (no write) any value to filter.
#### 5. View Filtered Data in multiple table in multiple window. Close Any window anytime.
#### 6. All search, table description can be saved with a button click for later usages.
#### 7. Find out how qtpy5 tableWidget, listWidget, combobox used to make this app - suggest better ways 

###### unorganized code , but app works - will clearn , modify soon 

Guide :
install cx_oracle, pyQt5.
### run launcher.py. 

### set host, port, sid, user name and password(already set in code for my setup) and then connect. To get data I used data from here https://download.oracle.com/oll/tutorials/DBXETutorial/html/module2/les02_load_data_sql.htm

![Launcher](https://user-images.githubusercontent.com/16148918/59210376-18ab1d00-8bcb-11e9-8e73-ea3672a0e736.PNG)

### search with a table name (any CasE)

![search tables with name](https://user-images.githubusercontent.com/16148918/59210381-1943b380-8bcb-11e9-8a5e-ecd6e596928d.PNG)

### Or with column name - will show all the tables have that column

![search tables with the column](https://user-images.githubusercontent.com/16148918/59210382-1943b380-8bcb-11e9-8efa-4e55f184a95e.PNG)

### All Columns of the selected table with type & info and all distinct data as dropdown - to filter (sql 'AND' will be applied )

![get all comuns on table name double click](https://user-images.githubusercontent.com/16148918/59210375-18ab1d00-8bcb-11e9-9bde-35f22431c924.PNG)

### filter as you want :)

![filter as you want](https://user-images.githubusercontent.com/16148918/59210374-18128680-8bcb-11e9-8c1a-a4f63c86b687.PNG)

### filter any tables

![filter any tables](https://user-images.githubusercontent.com/16148918/59210383-19dc4a00-8bcb-11e9-91f2-3ccb5f9bd63e.PNG)

### multiple window - lots of lots of serach, filter - so lots of windows

![multiple window](https://user-images.githubusercontent.com/16148918/59210378-18ab1d00-8bcb-11e9-85f4-4f2c71bc072e.PNG)

### Got lost - clock txt button - all your serach , query & data will be saved in a text. Each time you open this tool , it will create a file in Data directory. 

![save your research in table jungle](https://user-images.githubusercontent.com/16148918/59210379-1943b380-8bcb-11e9-802f-63af255015b2.PNG)


### 10. What next? will should try to integrate NLP , dont like  query langauage :-( 

