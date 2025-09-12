from PySide6.QtWidgets import QWidget, QDialog, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QRadioButton, QButtonGroup, QHBoxLayout, QSizePolicy, QTreeWidgetItem
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import QCoreApplication, Qt, QTimer
from start_page.league_view_teams import LeagueViewTeams

from Styles.stylesheets import StyleSheets
from update_dialog.update_lineup import UpdateLineupDialog
from update_dialog.update_positions import UpdatePositionsDialog
import random

class UpdateAdminDialog(QDialog):
    def __init__(self, league, selected, leaderboard, lv_teams, stack, undo, message, parent=None):
        super().__init__(parent)
        self.league = league
        self.selected = selected
        self.leaderboard = leaderboard
        self.lv_teams = lv_teams
        self.leaderboard_AVG = []
        self.stack = stack
        self.undo = undo
        self.message = message
        self.setWindowTitle("Update Management")
        self.resize(400, 300)
        self.styles = StyleSheets()
        self.setStyleSheet(self.styles.main_styles)
        
        # Widgets
        self.input_label = QLabel("Enter value:")
        self.input_label.setAlignment(Qt.AlignCenter)
        self.input = QLineEdit()
        self.input.setAlignment(Qt.AlignCenter)

        # ----- Submit Button ----- #
        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedWidth(100)
        self.submit_button.clicked.connect(self.update_stats)

        # ----- Undo Button ----- #
        self.undo_button = QPushButton("Undo")
        self.undo_button.setFixedWidth(100)
        self.undo_button.clicked.connect(self.undo_stat)

        # -------- Buttons Layout ----- # 
        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.addWidget(self.submit_button, alignment=Qt.AlignCenter)
        self.buttons_layout.addWidget(self.undo_button, alignment=Qt.AlignCenter)

        self.form_layout = QVBoxLayout()
        self.form_layout.addWidget(self.input_label)
        self.form_layout.addWidget(self.input)

        self.form_widget = QWidget()
        self.form_widget.setLayout(self.form_layout)
        self.form_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

                            # ----------------------------------------------------------------------------------------------------- # 

        # Right side: Radio Buttons in a group
        self.radio_group = QButtonGroup(self)
        self.radio_buttons = []

        options = ["default"]

        options = ["manager", "lineup", "positions", "max roster"]

        radio_buttons_layout = QVBoxLayout()
        radio_buttons_layout.setAlignment(Qt.AlignTop)

        for i in range(len(options)):
            radio = QRadioButton(f"{options[i]}")
            radio.toggled.connect(self.render_input_form)
            self.radio_group.addButton(radio, i)
            self.radio_buttons.append(radio)
            radio_buttons_layout.addWidget(radio)

        # Container widget for the radio buttons (optional)
        radio_buttons_widget = QWidget()
        radio_buttons_widget.setLayout(radio_buttons_layout)

                                # ---------------------------------------------------------------------------------------------------------------------#

        # Horizontal layout: form on the left, radios on the right
        self.content_layout = QHBoxLayout()
        self.content_layout.addStretch()
        self.content_layout.addWidget(self.form_widget)
        # hide on render
        self.form_widget.hide()
        self.content_layout.addSpacing(40)  # spacing between form and radios
        self.content_layout.addWidget(radio_buttons_widget)
        self.content_layout.addStretch()

         # ----- Main Layout ----- #
        self.main_layout = QVBoxLayout()
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.content_layout)
        self.main_layout.addSpacing(20)
        self.main_layout.addLayout(self.buttons_layout)

        self.setLayout(self.main_layout)

    def get_team_stat(self):
        # radio button selection 
        selection = self.radio_group.checkedButton().text()
        return selection
    
    def render_input_form(self):
        text = self.radio_group.checkedButton().text()
        if text == "lineup" or text == "positions":
            self.form_widget.hide()
        elif text == "max roster":
            rost_int = QIntValidator(1, 50)
            self.form_widget.show()
            self.input.setValidator(rost_int)
        else:
            self.form_widget.show()
        
           
    def set_new_stat_team(self, stat, input, team):
        val = None
        match stat:
            case 'manager':
                team.set_manager(input)
                return True
            case 'lineup':
                print('lineup selected')
            case 'positions':
                print("positions selected")
            case 'max_roster':
                try: 
                    val = int(input)
                except:
                    self.message.show_message("Roster value must be an integer!")
                    #show_message(self, "Roster value must be an integer!")
                    return False
                team.set_max_roster(val)
                return True
                

    def update_lineup_handler(self):
        ##print('lineup handler called')
        dialog = UpdateLineupDialog(self.league, self.selected, self.leaderboard, self.lv_teams, self.stack, self.undo, self.message, parent=self)
        dialog.exec()
    
    def update_positions_handler(self):
        ##print('positions handler called')
        dialog = UpdatePositionsDialog(self.league, self.selected, self.leaderboard, self.lv_teams, self.stack, self.undo, self.message, parent=self)
        dialog.exec()
    
    def update_stats(self):
        stat = None
        input = None
        team, num = self.selected
        try:
            stat = self.get_team_stat()
            ##print('stat before if:', stat)
            
            # if stat is lineup, exec lineup dialog pop up
            if stat == 'lineup':
                ##print('lineup selected')
                self.update_lineup_handler()
                return
            
            if stat == 'positions':
                ##print('positions selected')
                self.update_positions_handler()
                return

            input = self.input.text()

            if not stat or not input:
                raise ValueError("Must select stat and enter value.")
            
        except:
            ##print('Exception', e)
            #QMessageBox.warning(self, "Error", f"{stat} update not successful.")
            self.message.show_message(f"{team} update not successful.")
            return

        team, avg = self.selected
        find_team = self.league.find_team(team)

        ##print('team before:', find_team)

        # node - stack
        # new_node = NodeStack(obj, team, stat, prev, func, flag, player=None)
        if stat == 'max roster':
            stat = 'max_roster'

        self.stack.add_node(find_team, team, stat, getattr(find_team, stat), self.set_new_stat_team, 'team')
        
        ##print('stat - update stats:', stat)
        self.set_new_stat_team(stat, input, find_team)

        self.message.show_message(f'Team {stat} successfully updated!')
        #msg = show_message(self, f'Team {stat} successfully updated!')
        #msg.exec()

        self.input.clear()

        ##print('stack after:', self.stack)
        ##print('team after:', find_team)
    
    def undo_stat(self):
        self.undo.undo_exp()

    