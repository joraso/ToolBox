# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 10:02:50 2021

CSViewer - a very simple window for opening and viewing/editing csv files.

This is a work in progress, and currently supports:
- Opening csv files, and creating emply tables
- Editing data and column names
- Inserting new columns/rows.

Features that still need to be added to complete the project:
- Ability to move/rearrange rows and columns
- Ability to save tables to csv

The new Qt elements experimented with here are:
- QTables
- File dialogs
- QTabWidget
- QMainWindow
- QToolBar

@author: Joe Raso
"""

import pandas as pd
from PyQt5 import QtWidgets, QtCore#, QtGui

app = QtWidgets.QApplication([])

# Just the most basic implementation for now.
# See: https://doc.qt.io/qtforpython-5/PySide2/QtCore/QAbstractTableModel.html
class csvmodel(QtCore.QAbstractTableModel):
    def __init__(self, *args, fpath=None, **kwargs):
        super().__init__(*args, **kwargs)
        if fpath: self.csv = pd.read_csv(fpath)
        else: self.csv = pd.DataFrame()
    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # Wierdly, DisplayRole only supports strings
            return str(self.csv.iloc[index.row(), index.column()])
    def rowCount(self, index):
        return len(self.csv)
    def columnCount(self, index):
        return len(self.csv.columns)
        
    # "Well-behaved" models should also implement:
    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        # Horizontal headers are the columns (section [int] is the index):
        if orientation == QtCore.Qt.Horizontal and \
            role == QtCore.Qt.DisplayRole:
            return self.csv.columns[section]
        # In every other case, let's return the parent call
        return super().headerData(section, orientation, role)
        
    # For the data to be resizeable, we need to implement the following:
    def insertRow(self, row, count):
        """Inserts (count) rows into the table after (row)."""
        # Mandatory begin statement.
        self.beginInsertRows(QtCore.QModelIndex(), row, row + count)
        # On the Pandas end, we're doing this by generating a blank dataframe
        # and concatenating it into the original
        insert = pd.DataFrame(index=range(count), columns=self.csv.columns)
        newcsv = pd.concat([self.csv[:row], insert, self.csv[row:]])
        newcsv.reset_index()
        self.csv = newcsv
        self.endInsertRows() # Mandatory end statement
    def insertColumn(self, column, count):
        """Inserts (1) column into the table after (column)."""
        # Mandatory begin statement. Note the double refence to column and
        # the lack of refence to count (it's a dummy argument currently).
        self.beginInsertColumns(QtCore.QModelIndex(), column, column)
        # On the Pandas end, we do this by concatentation, as in insertRow
        insert = pd.Series(index=self.csv.index, dtype=float)
        newcsv = pd.concat([self.csv[self.csv.columns[:column]], insert,
                            self.csv[self.csv.columns[column:]]], axis=1)
        self.csv = newcsv
        self.endInsertColumns() # Mandatory end statement
        
    # These are not standard subclassing functions, but I'm implementing them
    # here to put values into the underlying DataFrame
    def editItem(self, index, value):
        self.csv.iloc[index.row(), index.column()] = value
        self.layoutChanged.emit() # Emit a layout change signal
    def editHeader(self, index, value):
        newname = {self.csv.columns[index.column()]:value}
        self.csv.rename(columns=newname, inplace=True)
        self.layoutChanged.emit() # Emit a layout change signal
    
class CSViewer(QtWidgets.QMainWindow):
    def __init__(self, *args, file=None, **kwargs):
        # This is the proper way of setting up the main window.
        super().__init__(*args, **kwargs)
        self.setWindowTitle("CSViewer")
        self.setGeometry(100,100,500,500)
        self.setCentralWidget(self.tabSpace())
        self.addToolBar(self.topBar())
        # The file kwarg is here for convienience of testing:
        if file: self.newTab(file)
        
    def tabSpace(self):
        """Generates the central tabbed veiwing space."""
        self.tabs = QtWidgets.QTabWidget()
        # Configure the tabs to be closable
        self.tabs.setTabsClosable(True)
        # The slot fot tab closure is here:
        self.tabs.tabCloseRequested.connect(self.closeTab)
        return self.tabs
        
    def inputEntrySpace(self):
        """Generates and sets up the input field."""        
        self.field = QtWidgets.QLineEdit()
        # tie 'enter' on the input field to pushing the value
        self.field.returnPressed.connect(self.pushValue)
        # We'll use a string to keep track of where the entered value should
        # be pushed to (ie. items or header):
        self.inputFocus = None
        return self.field
        
    def topBar(self):
        """Generates the tool bar of buttons at the top of the window."""
        # Trying out QToolBar with actions:
        self.bar = QtWidgets.QToolBar()
        # Toolbars typically contain QActions, which can be specified to
        # addAction in a variety of ways. Note that in the docs, the final
        # 'Functor' object should be the functional action called.
        self.openButton = self.bar.addAction("Open", self.openTab)
        self.newButton = self.bar.addAction("New", self.newTab)
        self.addRowButton = self.bar.addAction("+Row", self.addRow)
        self.addColButton = self.bar.addAction("+Col", self.addColumn)
        # Toolbars also allow for Widgets like the input entry field
        self.bar.addWidget(self.inputEntrySpace())
        # We'll use a simple 
        return self.bar
        
    def newTab(self, fpath=None):
        """Opens a new tab. If no file path is specified, defaults to an empty
        tab."""
        model = csvmodel(fpath=fpath)
        view = QtWidgets.QTableView()
        view.setModel(model)
        # Set up what happens when a cell is clicked:      
        view.clicked.connect(self.displaySelected)
        # Set up what happens when a column header is clicked:
        view.horizontalHeader().sectionClicked.connect(self.displayColumnName)
        # We want to name the tab, so we'll strip the file name from the end
        # of the file path. If this is a blank tab, then we call it 'untitled'.
        fname = "untitled" if not fpath else fpath.split('/')[-1]
        self.tabs.addTab(view, fname)        
        
    def openTab(self):
        """Select a file, and open it in a new tab."""
        # This is the simplest way to invoke a file dialog. It's possible to 
        # set filters and such, but it requires a more complex approach. Note
        # this function returns a tuple of (abs_path, file_types).
        fpath_tuple = QtWidgets.QFileDialog.getOpenFileName()
        # If the user presses cancel, empty strings get returned, and we only
        # want to open a tab if the user selected a file, so:
        if fpath_tuple[0]:
            self.newTab(fpath=fpath_tuple[0])
        
    def closeTab(self, currentIndex):
        """Closes a tab."""
        # uses the currentIndex arg to identify which tab is being closed.
        self.tabs.removeTab(currentIndex)
        
    def displaySelected(self):
        """Displays the selected cell on the input field."""
        # First we have to find the current tab,
        tab = self.tabs.currentWidget()
        # then get the index of the selected cell, and the value contained
        ind = tab.selectionModel().currentIndex()
        value = tab.model().data(ind, QtCore.Qt.DisplayRole)
        # and then push it to the display field.
        self.field.setText(value)
        
    def displayColumnName(self):
        """Displays the column name in the input field."""
        # Get the tab and the selected header index:
        tab = self.tabs.currentWidget()
        ind = tab.horizontalHeader().currentIndex().column()
        value = str(tab.model().headerData(ind, QtCore.Qt.Horizontal))
        self.field.setText(value)
        
    def pushValue(self):
        """Deposits the entered value from the input filed into the selected
        cell, or into the header is a full columnis selected."""
        # As before, find the tab.
        tab = self.tabs.currentWidget()
        # Check if a full column is selected. If so, we are editing the header
        if tab.selectionModel().selectedColumns():
            ind = tab.horizontalHeader().currentIndex()
            # grab the value from the input bar and push it to the csv model.
            value = self.field.text()
            tab.model().editHeader(ind, value)
        else:
            # Else we are editing a cell
            ind = tab.selectionModel().currentIndex()
            # grab the value from the input bar and push it to the csv model.
            value = self.field.text()
            tab.model().editItem(ind, value)
            # Move to the next row down
            nex = tab.model().index(ind.row()+1, ind.column())
            tab.selectionModel().setCurrentIndex(nex,
                QtCore.QItemSelectionModel.ClearAndSelect)
            self.displaySelected()
        
    def addRow(self):
        """Adds a row at/before the selected row of the selected cell."""
        # As before, find the tab, and selected cell row.
        tab = self.tabs.currentWidget()
        row = tab.selectionModel().currentIndex().row()
        # Call insert row on the model
        tab.model().insertRow(row, 1)
        tab.model().layoutChanged.emit()
        # Highlight/select the newly inserted row. Note that because it was
        # inserted above the selected cell, 'row' now refers to the new row.
        tab.selectRow(row)
        
    def addColumn(self):
        """Adds a column at/before the selected column of the selected cell."""
        # As in addRow:
        tab = self.tabs.currentWidget()
        col = tab.selectionModel().currentIndex().column()
        tab.model().insertColumn(col, 1)
        tab.model().layoutChanged.emit()
        tab.selectColumn(col)
        
if __name__ == '__main__':
    
    win = CSViewer(file="Aesop.csv")
    win.show(); app.exec()
#    csv = pd.read_csv("Aesop.csv")