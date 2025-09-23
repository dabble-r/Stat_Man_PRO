# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'leader_league.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QListWidget, QListWidgetItem,
    QSizePolicy, QWidget, QTreeWidget, QPushButton, QVBoxLayout, QHBoxLayout, QDialog, QHeaderView, QMessageBox, QGroupBox)
from stat_dialog.stat_dialog_ui import Ui_StatDialog
from start_page.leaderboard_ui import Leaderboard
from add_player.new_player_ui import Ui_NewPlayer
from add_team.new_team_w_ui import Ui_NewTeam
from start_page.league_view_teams import LeagueViewTeams
from stat_dialog.stat_dialog_ui import Ui_StatDialog
from remove.remove import RemoveDialog

from Save.save_dialog_ui import SaveDialog
from Load.load_dialog_ui import Load
from Files.file_dialog import FileDialog
import random


class LeagueViewPlayers(QWidget):
    def __init__(self, league_view, selected, league, styles, undo, file_dir, message, parent=None):
        super().__init__()
        self.setObjectName("league view players - top")
        self.selected = selected
        self.styles = styles
        #self.setStyleSheet(self.styles.modern_styles)
        self.undo = undo
        self.file_dir = file_dir
        self.db_path = f"{self.file_dir}/DB"
        self.csv_path = None
        self.message = message
        self.parent = parent

        self.label_1 = QLabel("Players")
        self.label_1.setAlignment(Qt.AlignCenter)
        self.tree1_top = QTreeWidget()

        self.label_2 = QLabel("Leaderboard")
        self.label_2.setAlignment(Qt.AlignCenter)
        self.tree2_top = QTreeWidget()

        self.tree1_top.setObjectName("players - tree1 - top")
        self.tree2_top.setObjectName("players - tree2 - top")

        self.selected_players = None 
        self.selected_leaderboard = None #self.tree2_top.currentItem() # only players leaderboard view
        self.league = league

        self.leaderboard = Leaderboard(self.tree2_top, self.league, parent=self)

        self.league_view_teams = league_view

        #self.new_team_ui = Ui_NewTeam(self.league_view_teams.tree1_bottom, self.league_view_teams.tree2_bottom, self.league, self.file_dir, self.styles, self.message, parent=self.parent)
        #self.new_team_widget = QDialog(self.parent)
        #self.new_team_widget.setStyleSheet(self.styles.modern_styles)

        self.tree1_top.setColumnCount(3)
        self.tree1_top.setHeaderLabels(["Player", "Team", "Number"])
        self.tree1_top.header().setDefaultAlignment(Qt.AlignCenter)

        header1 = self.tree1_top.header()
        header1.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # new player UI 
        # initialize new dialog for each add player click
        #self.new_player_ui = Ui_NewPlayer(self.tree1_top, self.leaderboard, self.league)
        #self.new_player_widget = QDialog(self)
        #self.new_player_widget.setStyleSheet(self.styles.main_styles)

        # Top layout containing two tree widgets
        self.top_layout = QHBoxLayout()

        self.v_layout_players = QVBoxLayout()
        self.v_layout_players.addWidget(self.label_1)
        self.v_layout_players.addWidget(self.tree1_top)

        self.v_layout_leaderboard = QVBoxLayout()
        self.v_layout_leaderboard.addWidget(self.label_2)
        self.v_layout_leaderboard.addWidget(self.tree2_top)

        self.top_layout.addLayout(self.v_layout_players)
        self.top_layout.addLayout(self.v_layout_leaderboard)
        #self.top_layout.addWidget(self.tree1_top)
        #self.top_layout.addWidget(self.tree2_top)

        # Buttons to the right of second tree widget at the top
        self.button_group = QGroupBox("Add", self)
        #self.button_group.setGeometry(QRect(1,1,25,75))

        # button layout at top
        self.button_layout_top = QVBoxLayout()

        self.btn_add_player = QPushButton("Add Player")
        self.btn_add_team = QPushButton("Add Team")
        self.btn_save = QPushButton("Save")
        self.btn_load = QPushButton("Load")
        

        self.btn_add_player.clicked.connect(self.new_player_handler)
        self.btn_add_team.clicked.connect(self.new_team_handler)
        self.btn_load.clicked.connect(self.load_csv)
        self.btn_save.clicked.connect(self.save_csv)

        self.button_layout_top.addWidget(self.btn_add_player)
        self.button_layout_top.addWidget(self.btn_add_team)
        self.button_layout_top.addWidget(self.btn_save)
        self.button_layout_top.addWidget(self.btn_load)

        # add button layout to group box 
        self.button_group.setLayout(self.button_layout_top)

        # use layouts from league view players individually to customize main view
        #self.top_layout.addWidget(self.button_group)
    
    # deprecated
    
    def open_new_player_dialog(self):
        self.new_player_widget = QDialog(self.parent)
        self.ui = Ui_NewPlayer(self.tree1_top, self.leaderboard, self.league, self.file_dir, self.message, parent=self.new_player_widget)
        self.ui.setupUi(self.new_player_widget)

        

        self.new_player_widget.setWindowTitle("Add New Player")
        #self.new_player_widget.setModal(True)
        self.new_player_widget.exec()

    def new_player_handler(self):
        if self.league.get_count() == 0:
            ##print("No teams in league!")
            #QMessageBox.warning(self, "Input Error", "Must create a team before adding players.")
            self.message.show_message("Must create a team before adding players.")
            return
        
        # create new player dialog for each 
        self.open_new_player_dialog()
    
    def new_team_handler(self):
        ##print("new team handler")
        self.new_team_ui = Ui_NewTeam(self.league_view_teams.tree1_bottom, self.league_view_teams.tree2_bottom, self.league, self.file_dir, self.styles, self.message, parent=self.parent)
        self.new_team_widget = QDialog(self.parent)
        #self.new_team_widget.setStyleSheet(self.styles.modern_styles)
        
        self.new_team_ui.setupUi(self.new_team_widget)
        self.new_team_widget.setWindowTitle("Add New Team")
        self.new_team_widget.setModal(True)
        
        self.new_team_widget.exec()
    
    def remove_league_view(self, target):
        count = self.tree1_top.topLevelItemCount()
        player = target.name
        i = 0 
        while i < count:
            item = self.tree1_top.topLevelItem(i)
            name = item.text(0)
            if name == player:
                self.tree1_top.takeTopLevelItem(i)
                return
            i += 1

    def remove_leaderboard(self):
        pass

    def save_csv(self):
        print('saving to csv to local device')
        self.save_widget = QDialog(self.parent)
        self.save_widget.setWindowTitle("Save Progress")
        self.save_widget.setModal(True)

        # Just instantiate and call setupUi once
        self.save_ui = SaveDialog(self.league, self.message, self.file_dir, self.parent)
        #self.save_ui.setupUi(self.save_widget)

        self.save_ui.exec()

        
    def load_csv(self):
        print('loading csv to DB')
        '''self.load_widget = QDialog(self.parent)
        self.load_widget.setWindowTitle("Load Progress")
        self.load_widget.setModal(True)
        # Just instantiate and call setupUi once
        self.load_ui = Ui_LoadDialog(self.league, self.message, self.file_dir, self.load_widget)
        self.load_ui.setupUi(self.load_widget)
        self.load_widget.exec()'''
        file = FileDialog(self.message, parent=self.parent, flag="load")
        db_path, csv_path = file.open_dual_file_dialog()

        load = Load(self.league, self.message, self.file_dir, db_path=db_path, csv_path=csv_path, parent=self)
        load.load_master()

    def get_rand(self):
        rand = random.randint(1, 1000)
        return rand


   


    
    


