from PySide6.QtWidgets import QWidget, QDialog, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QRadioButton, QButtonGroup, QHBoxLayout, QSizePolicy, QTreeWidgetItem
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import QCoreApplication, Qt, QTimer, QRect
from start_page.league_view_teams import LeagueViewTeams

from update_dialog.update_offense import UpdateOffenseDialog
from update_dialog.update_pitching import UpdatePitchingDialog
from update_dialog.update_admin import UpdateAdminDialog
from update_dialog.update_team_stats import UpdateTeamStatsDialog
from Files.file_dialog import FileDialog
from Files.image import Icon, PixMap
import random

class UpdateDialog(QDialog):
    def __init__(self, league, selected, leaderboard, lv_teams, stack, undo, file_dir, styles, message, parent=None):
        super().__init__(parent)
        self.league = league
        self.selected = selected
        self.leaderboard = leaderboard
        self.lv_teams = lv_teams
        self.leaderboard_AVG = []
        self.stack = stack
        self.undo = undo
        self.file_dir = file_dir
        self.styles = styles
        self.message = message
        self.parent = parent
        self.setObjectName("Update Dialog")

        # Widgets
        self.int_label = QLabel("Enter value:")
        self.int_label.setAlignment(Qt.AlignCenter)
        self.int_input = QLineEdit()
        self.int_input.setValidator(QIntValidator())
        self.int_input.setAlignment(Qt.AlignCenter)

        # player stat buttons
        # stat category 
        self.offense_button = QPushButton("Offense")
        #self.offense_button.setFixedWidth(150)
        self.offense_button.clicked.connect(self.update_offense_handler)

        self.pitching_button = QPushButton("Pitching")
        #self.pitching_button.setFixedWidth(150)
        self.pitching_button.clicked.connect(self.update_pitching_handler)

        # team admin buttons 
        # stat category 
        self.admin_button = QPushButton("Management")
        self.admin_button.setFixedWidth(250) 
        self.admin_button.clicked.connect(self.update_admin_handler)

        # team stats buttons 
        # stat category 
        self.team_stats_button = QPushButton("Stats")
        self.team_stats_button.setFixedWidth(100) 
        self.team_stats_button.clicked.connect(self.update_team_stats_handler)

        # team stats buttons 
        # logo category 
        self.upload_button = QPushButton("Upload")
        self.upload_button.setFixedWidth(100) 
        self.upload_button.clicked.connect(self.upload_handler)

        form_layout = QVBoxLayout()
        form_layout.addWidget(self.int_label)
        form_layout.addWidget(self.int_input)

        form_widget = QWidget()
        form_widget.setLayout(form_layout)
        form_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                            # -----------------------------------------------------------------------------------------------------# 

        # ----- Main Layout -----
        main_layout = QVBoxLayout()
        main_layout.addStretch()
        main_layout.addSpacing(20)

        self.resize(400, 300)

        if len(self.selected) == 2:
            self.setWindowTitle("Update Team")

            main_layout.addWidget(self.admin_button, alignment=Qt.AlignCenter)
            main_layout.addWidget(self.team_stats_button, alignment=Qt.AlignCenter)
            main_layout.addWidget(self.upload_button, alignment=Qt.AlignCenter)

            self.setLayout(main_layout)

        else:
            self.setWindowTitle("Update Player")

            main_layout.addWidget(self.offense_button, alignment=Qt.AlignCenter)
            main_layout.addWidget(self.pitching_button, alignment=Qt.AlignCenter)
            main_layout.addWidget(self.upload_button, alignment=Qt.AlignCenter)

            self.setLayout(main_layout)

    def update_offense_handler(self):
        dialog = UpdateOffenseDialog(self.league, self.selected, self.leaderboard, self.lv_teams, self.stack, self.undo, self.styles, self.message, parent=self)
        dialog.setStyleSheet("QDialog { border: 2px solid black; }")
        dialog.exec()
    
    def update_pitching_handler(self):
        player, team, avg = self.selected
        find_team = self.league.find_team(team)
        find_player = find_team.get_player(player)
        if "pitcher" not in find_player.positions:
            self.message.show_message("Player has no pitching position.")
            #QMessageBox.warning(self, "Input Error", "Player has no pitching position.")
        else:
            dialog = UpdatePitchingDialog(self.league, self.selected, self.leaderboard, self.lv_teams, self.stack, self.undo, self.message, parent=self)
            dialog.exec()
    
    def update_admin_handler(self):
        dialog = UpdateAdminDialog(self.league, self.selected, self.leaderboard, self.lv_teams, self.stack, self.undo, self.message, parent=self)
        dialog.exec()

    def update_team_stats_handler(self):
        dialog = UpdateTeamStatsDialog(self.league, self.selected, self.leaderboard, self.lv_teams, self.stack, self.undo, self.message, self.styles, parent=self)
        dialog.exec()
    
    def upload_dialog(self):
        ##print("upload")
        # open window to select file 
        # set a file path to file selected 
        # call Icon method to create icon 
        # set team icon to icon object 
        # set icon to stat and update dialogs ? 
        dialog = FileDialog(self.message, self)
        dialog.open_file_dialog()
        file_path = dialog.get_file_path()
        ##print('file path:', file_path)
        icon = self.get_icon(file_path)
        # test func 
        if len(self.selected) == 2:
            self.change_logo(icon)
        return icon, file_path

    def get_icon(self, file_path):
        icon = Icon(file_path)
        ret_icon = icon.create_icon()
        return ret_icon
    
    def upload_handler(self):
        icon = None

        if len(self.selected) == 2:
            team, avg = self.selected
            try:
                icon, file_path = self.upload_dialog()
                find_team = self.league.find_team(team)
                find_team.logo = file_path  
                #print(icon, file_path)
                #print('team logo: ', find_team.logo)
                self.message.show_message("Team logo successfully updated!")
            
            except Exception as e:
                #print(f'error: new team logo not created!\n{e}')
                self.message.show_message(f"Error uploading logo!")

        elif len(self.selected) == 3: 
            player, team, avg = self.selected
        
            try:
                icon, file_path = self.upload_dialog()
                find_team = self.league.find_team(team)
                find_player = find_team.get_player(player)
                find_player.image = file_path  
                #print(icon, file_path)
                #print('team logo: ', find_team.logo)
                self.message.show_message("Player image successfully updated!")
            
            except Exception as e:
                #print(f'error: new team logo not created!\n{e}')
                self.message.show_message(f"Error uploading image!")
        
        return
    
    def change_logo(self, new_logo):
        # iterate thru stack of widget items 
        # match item name 
        # delete item from widget 
        # replace item with updated item and new logo
        team, num = self.selected

        curr_1 = self.lv_teams.tree1_bottom.currentItem()
        curr_2 = self.lv_teams.tree2_bottom.currentItem()
        ##print('curr 1 selected', curr_1)
        ##print('curr 2 selected', curr_2)
        
        if curr_1:
            curr_1.setIcon(0, new_logo)
            team = curr_1.text(0)
            self.refresh_other(self.lv_teams.tree2_bottom, team, new_logo)
        elif curr_2:
            curr_2.setIcon(0, new_logo)
            team = curr_2.text(0)
            self.refresh_other(self.lv_teams.tree1_bottom, team, new_logo)
        
    def refresh_other(self, widget, team, logo):
        # itereate through widget 
        # find matching team name 
        # set icon to new logo
        for i in range(widget.topLevelItemCount()):
            item = widget.topLevelItem(i)
            name = item.text(0)
            if name == team:
                item.setIcon(0, logo)
            
                        #----------------------------------------------------------------------------------------------------------------#
    
    