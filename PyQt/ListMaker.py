# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 15:01:21 2021

Practice with Qt's model/viewer/controller or model/viewer paradigm, with a
simple list maker.

Losely following along with:
https://www.pythonguis.com/tutorials/modelview-architecture/

"Model" - holds the data structure which the app is working with.
"View" - any representation of information as shown to the user, whether
graphical or tables. Multiple views of the same data model are allowed.
"Controller" - accepts input from the user, transforming it into commands that
transform the model/view.

@author: Joe Raso
"""

from PyQt5.QtWidgets import QApplication, QWidget, QListView, QVBoxLayout, \
     QHBoxLayout, QPushButton, QLineEdit
    
from PyQt5.QtCore import QAbstractListModel, Qt

app = QApplication([])

# List/table/tree - like objects should be suclassed from their abstract
# counterparts (these are in C++ only, so can't be instantiated directly)
class myListModel(QAbstractListModel):
    def __init__(self, *args, initial_list=None, **kwargs):
        # Initiate the superclass
        super().__init__(*args, **kwargs)
        # Put any initial list provided into a list to store
        self.items = initial_list or []
        
    # The abstract list class requires two methods:
    def rowCount(self, index): # return the number of rows
        return len(self.items)
    def data(self, index, role): # to retrieve data
        # This must return the data at index (1D in the case of a list)
        # 'role' refers to Qt data type being requested, which may include
        # DisplayRole, DecorationRole, EditRole, ToolTipRole, StatusTipRole,
        # WhatsThisRole, SizeHintRole.
    
        # DisplayRole is what retrieves entry for the GUI to dislay.
        # Note that the index passed is actually a QModelIndex object
        if role == Qt.DisplayRole:
            return self.items[index.row()]

class ListMaker:
    def __init__(self, initial_list=None):
        """A little list maker. It interfaces with the myListModel model,
        containing the viewer, and acting as controller."""
        
        # Initialize the view plug in
        self.view = QListView()
        self.model = myListModel(initial_list=initial_list)
        self.view.setModel(self.model)
        
        # Initialize the entry field (connect it to add entries on 'enter')
        self.add_field = QLineEdit()
        self.add_field.returnPressed.connect(self.add_entry)
        
        # Initialize the add button
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.add_entry)
        
        # Initialize the delete button
        self.del_button = QPushButton("Delete")
        self.del_button.clicked.connect(self.del_entry)
        
        # Set up the window
        layout_outer = QVBoxLayout()
        layout_outer.addWidget(self.view)
        layout_outer.addWidget(self.add_field)
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.add_button)
        layout_buttons.addWidget(self.del_button)
        button_widget = QWidget()
        button_widget.setLayout(layout_buttons)
        layout_outer.addWidget(button_widget)
        self.window = QWidget()
        self.window.setLayout(layout_outer)
        
    def add_entry(self):
        """Controller function to add the string in add_field to the list."""
        # First, add whatever is in the add_field to the list:
        self.model.items.append(self.add_field.text())
        # Then force the view to refresh
        self.model.layoutChanged.emit()
        # Then reset to add_field
        self.add_field.setText("")
        
    def del_entry(self):
        """Controler function to delete the selected entry."""
        # First, retrieve the list of indexes of the selected entries
        selected = self.view.selectedIndexes()
        # this will be empty if nothing is selected, so...
        if selected:
            # There will be multiple items if multiple are selected,
            # For simplicity, we'll just remove the first
            del self.model.items[selected[0].row()]
            # Then force the view to refresh
            self.model.layoutChanged.emit()

TD = ListMaker(initial_list=["Sample Entry"])
TD.window.show()
app.exec()