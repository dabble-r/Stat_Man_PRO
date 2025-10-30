# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_layout_treeWidgets_buttons.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################


# create main horizontal layout
# left column layout
# right column layout 
# left colume layout 
    # horizontal top (2 tree widgets)
    # horizontal bottom (2 tree widgets)
    # vertiacl layout of both layouts
# right column layout 
    # top vertical layout
    # top buttons group 
    # bottom vertical layout  
    # bottom buttons group 
    # vertical layout of both layouts
# main horizontal layout 
    # both left and right layouts

# self set layout to main horiztonal layout 

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QTreeWidget, QMainWindow
)
from PySide6.QtCore import QRect


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window - Test")
        self.resize(800, 600)
        self.setupUi()

    def setupUi(self):
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # Create TreeWidgets
        tree1 = QTreeWidget()
        tree2 = QTreeWidget()
        tree3 = QTreeWidget()
        tree4 = QTreeWidget()

        # Create Buttons
        btn1 = QPushButton("Add Player")
        btn2 = QPushButton("Add Team")
        btn3 = QPushButton("Save")
        btn4 = QPushButton("Stat")
        btn5 = QPushButton("Remove")
        btn6 = QPushButton("Refresh")
        btn7 = QPushButton("Update")

        # Top and bottom tree layouts
        horizontal_top = QHBoxLayout()
        horizontal_top.addWidget(tree1)
        horizontal_top.addWidget(tree2)

        horizontal_bottom = QHBoxLayout()
        horizontal_bottom.addWidget(tree3)
        horizontal_bottom.addWidget(tree4)

        # Left column with all tree views
        left_column = QVBoxLayout()
        left_column.addLayout(horizontal_top)
        left_column.addLayout(horizontal_bottom)

        # Top button group
        group_top = QGroupBox("Top Controls")
        group_top_layout = QVBoxLayout()
        group_top_layout.addWidget(btn1)
        group_top_layout.addWidget(btn2)
        group_top_layout.addWidget(btn3)
        group_top.setLayout(group_top_layout)

        # Bottom button group
        group_bottom = QGroupBox("Bottom Controls")
        group_bottom_layout = QVBoxLayout()
        group_bottom_layout.addWidget(btn4)
        group_bottom_layout.addWidget(btn5)
        group_bottom_layout.addWidget(btn6)
        group_bottom_layout.addWidget(btn7)
        group_bottom.setLayout(group_bottom_layout)

        # Buttons column
        right_column = QVBoxLayout()
        right_column.addWidget(group_top)
        right_column.addWidget(group_bottom)

        # Main layout
        main_layout = QHBoxLayout()
        main_layout.addLayout(left_column)
        main_layout.addLayout(right_column)
        self.centralwidget.setLayout(main_layout)


# Example usage
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()