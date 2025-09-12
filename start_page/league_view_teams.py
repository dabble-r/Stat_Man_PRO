# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'league_view.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QVBoxLayout, QLabel, QListWidget,
    QListWidgetItem, QSizePolicy, QWidget, QTreeWidget, QPushButton, QDialog, QHeaderView, QTreeWidgetItem)
from add_team.new_team_w_ui import Ui_NewTeam
from stat_dialog.stat_dialog_ui import Ui_StatDialog
import random


class LeagueViewTeams(QWidget):
    def __init__(self, league, styles, stack, file_dir, message, parent=None):
        super().__init__()
        self.setObjectName("league view teams - bottom")
        self.leaderboard_AVG = []
        self.selected_WL = None # only teams from WL tree widget, for stat dialog
        self.selected_AVG = None # only teams from AVG tree widget, for stat dialog
        self.league = league
        self.styles = styles
        self.stack = stack
        self.file_dir = file_dir
        self.message = message
        self.parent = parent
        
        # Bottom layout containing two tree widgets
        self.bottom_layout = QHBoxLayout()

        self.label_1 = QLabel("Teams W-L")
        self.label_1.setAlignment(Qt.AlignCenter)
        self.tree1_bottom = QTreeWidget()

        self.label_2 = QLabel("Teams AVG")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.tree2_bottom = QTreeWidget()

        self.tree1_bottom.setColumnCount(2)
        self.tree1_bottom.setHeaderLabels(["Team", "W - L"])
        self.tree1_bottom.header().setDefaultAlignment(Qt.AlignCenter)
        self.tree1_bottom.setObjectName("teams - tree 1 - bottom")
        self.tree1_bottom.setIconSize(QSize(35,35))

        self.tree2_bottom.setObjectName("teams - tree 2 - bottom")
        self.tree2_bottom.setColumnCount(2)
        self.tree2_bottom.setHeaderLabels(["Team", "AVG"])
        self.tree2_bottom.header().setDefaultAlignment(Qt.AlignCenter)
        self.tree2_bottom.setIconSize(QSize(35,35))

        header1 = self.tree1_bottom.header()
        header2 = self.tree2_bottom.header()
        # Set resize mode to stretch to make columns equally wide
        header1.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        header2.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.v_layout_wl = QVBoxLayout()
        self.v_layout_wl.addWidget(self.label_1)
        self.v_layout_wl.addWidget(self.tree1_bottom)

        self.v_layout_avg = QVBoxLayout()
        self.v_layout_avg.addWidget(self.label_2)
        self.v_layout_avg.addWidget(self.tree2_bottom)

        self.bottom_layout.addLayout(self.v_layout_wl)
        self.bottom_layout.addLayout(self.v_layout_avg)
        #self.bottom_layout.addWidget(self.tree1_bottom)
        #self.bottom_layout.addWidget(self.tree2_bottom)

        # new team UI
        self.new_team_ui = Ui_NewTeam(self.tree1_bottom, self.tree2_bottom, self.league, self.file_dir, self.styles, self.message, self)
        self.new_team_widget = QDialog(self)
        #self.new_team_widget.setStyleSheet(self.styles.main_styles)

        '''# Stat button to the right of second tree widget at the bottom
        self.btn_stat = QPushButton("Stat")
        self.bottom_layout.addWidget(self.btn_stat)
        self.btn_stat.clicked.connect(self.setup_stat_ui)
        self.stat_ui = Ui_StatDialog()
        self.stat_widget = QDialog(self)'''

    def new_team_setup(self):
        ##print("add new team")
        self.new_team_ui.setupUi(self.new_team_widget)
        self.new_team_widget.setWindowTitle("Add New Team")
        self.new_team_widget.setModal(True)
        self.new_team_widget.exec()
    
    def refresh_league_view_wl(self, target):
        count = self.tree1_bottom.topLevelItemCount()
        name_target = target.name
        wl_avg_upd = target.get_wl_avg()
        i = 0
        while i < count:
            item = self.tree1_bottom.topLevelItem(i)
            # wl view
            team = item.text(0)
            wl_avg = item.text(1)
            if team == name_target:
                ###print("team match:", team, wl_avg)
                item.setText(1, wl_avg_upd)
                item.setIcon(0, target.logo)
            i += 1

    def refresh_league_view_avg(self, target):
        count = self.tree2_bottom.topLevelItemCount()
        name_target = target.name
        bat_avg_upd = target.get_bat_avg()
        i = 0
        while i < count:
            item = self.tree2_bottom.topLevelItem(i)
            # wl view
            team = item.text(0)
            bat_avg = item.text(1)
            if team == name_target:
                ###print("team match:", team, wl_avg)
                item.setText(1, bat_avg_upd)
            i += 1
    
    def remove_league_view_wl(self, target):
        count = self.tree1_bottom.topLevelItemCount()
        name_target = target.name 
        i = 0 
        while i < count:
            item = self.tree1_bottom.topLevelItem(i)
            team = item.text(0)
            if team == name_target:
                self.tree1_bottom.takeTopLevelItem(i)
                return
            i += 1
    
    def remove_league_view_avg(self, target):
        count = self.tree2_bottom.topLevelItemCount()
        name_target = target.name 
        i = 0 
        while i < count:
            item = self.tree2_bottom.topLevelItem(i)
            team = item.text(0)
            if team == name_target:
                self.tree2_bottom.takeTopLevelItem(i)
                return
            i += 1
        

    
    